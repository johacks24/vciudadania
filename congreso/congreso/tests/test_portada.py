"""Tests sin red de la portada y el índice de la legislatura (C.1)."""

import json
from pathlib import Path

from congreso.exportar_portada import (
    N_ESTATICOS,
    generar_indice,
    generar_portada,
    votaciones_recientes,
)
from congreso.exportar_sqlite import exportar

FIX = Path(__file__).parent / "fixtures"


def _registro() -> dict:
    return json.loads((FIX / "votacion010.json").read_text(encoding="utf-8"))


def _base_con_dos(tmp_path: Path) -> Path:
    """Una nominal de la sesión 202 (30/9/2026) y un suplicatorio de la 89 (22/1/2025)."""
    nominal = _registro()
    secreto = _registro()
    secreto["informacion"]["sesion"] = 89
    secreto["informacion"]["numeroVotacion"] = 5
    secreto["informacion"]["fecha"] = "22/1/2025"
    secreto["votaciones"] = []
    raw = tmp_path / "raw"
    for rel, reg in (
        ("Sesion202/20260930/Votacion010", nominal),
        ("Sesion89/20250122/Votacion005", secreto),
    ):
        d = raw / rel
        d.mkdir(parents=True)
        (d / "VOT_prueba.json").write_text(json.dumps(reg), encoding="utf-8")
    destino = tmp_path / "congreso.sqlite"
    exportar(sorted(raw.rglob("VOT_*.json")), destino, "XV")
    return destino


def _sinteticos(n: int) -> list[dict]:
    return [
        {
            "id": f"Leg1-{i:03d}", "sesion": 1, "numero": i, "fecha": "1/1/2026",
            "titulo": f"Votación número {i}", "si": i, "no": 0, "abst": 0, "novota": 0,
            "sin_individual": False, "ficha": f"votacion/Leg1-{i:03d}.html",
        }
        for i in range(1, n + 1)
    ]


def test_orden_de_recientes_primero(tmp_path):
    """La fecha de la fuente (D/M/YYYY) no es ordenable como texto: se parsea."""
    vots = votaciones_recientes(_base_con_dos(tmp_path), "XV")
    assert [v["id"] for v in vots] == ["Leg202-010", "Leg89-005"]  # 2026 antes que 2025
    assert vots[1]["sin_individual"] is True
    assert vots[0]["ficha"] == "votacion/Leg202-010.html"
    assert (vots[0]["si"], vots[0]["no"], vots[0]["abst"], vots[0]["novota"]) == (34, 312, 0, 4)


def test_indice_json_el_orden_es_la_cronologia(tmp_path):
    """El contrato del índice: el orden del array ES la cronología (el cliente no ordena)."""
    vots = votaciones_recientes(_base_con_dos(tmp_path), "XV")
    destino = generar_indice(vots, tmp_path / "indice.json", "XV")
    j = json.loads(destino.read_text(encoding="utf-8"))
    assert j["legislatura"] == "XV"
    assert [v["id"] for v in j["votaciones"]] == ["Leg202-010", "Leg89-005"]
    assert set(j["votaciones"][0]) >= {"id", "fecha", "titulo", "si", "no", "abst", "ficha", "sin_individual"}


def test_portada_primeros_sin_javascript(tmp_path):
    """Los primeros N van en el HTML: la página lista sin ejecutar nada."""
    vots = votaciones_recientes(_base_con_dos(tmp_path), "XV")
    destino = generar_portada(vots, tmp_path / "portada.html", "XV")
    pagina = destino.read_text(encoding="utf-8")
    assert "30/9/2026" in pagina and "22/1/2025" in pagina  # las dos fechas, estáticas
    assert 'href="votacion/Leg202-010.html"' in pagina
    assert "votación no nominal (solo totales)" in pagina
    assert "2 votaciones del Pleno" in pagina
    assert "indice.json" in pagina and "IntersectionObserver" in pagina  # scroll infinito


def test_portada_solo_pinta_los_primeros_n_estaticos(tmp_path):
    """Con más de N votaciones, el HTML estático lleva N; el resto lo carga el scroll."""
    destino = generar_portada(_sinteticos(N_ESTATICOS + 10), tmp_path / "portada.html", "XV")
    pagina = destino.read_text(encoding="utf-8")
    assert f"Votación número {N_ESTATICOS}" in pagina
    assert f"Votación número {N_ESTATICOS + 1}" not in pagina
    assert f"ESTATICOS = {N_ESTATICOS}" in pagina  # el cliente arranca tras los estáticos


def test_portada_escapa_el_html_de_la_fuente(tmp_path):
    vots = _sinteticos(1)
    vots[0]["titulo"] = '<script>x</script> & "comillas"'
    destino = generar_portada(vots, tmp_path / "portada.html", "XV")
    pagina = destino.read_text(encoding="utf-8")
    assert "<script>x" not in pagina
    assert "&lt;script&gt;x&lt;/script&gt;" in pagina
    assert "&quot;comillas&quot;" in pagina
