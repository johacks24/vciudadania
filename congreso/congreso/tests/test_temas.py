"""Tests sin red de la importación de temas (C.3): fuente secundaria CongresoAbierto.

El fixture `congresoabierto_temas.csv` son 2 filas reales de su CSV (23/11/2026):
la votación 010 de la sesión 202 (un tema) y el suplicatorio de la sesión 89
(varios temas, separador « | »).
"""

import json
import sqlite3
import types
from pathlib import Path

import congreso.cli as cli
from congreso.exportar_portada import generar_portada, temas_con_cuenta, votaciones_recientes
from congreso.exportar_sqlite import exportar, exportar_temas
from congreso.fuentes import congresoabierto

FIX = Path(__file__).parent / "fixtures"

URL_202 = ("https://www.congreso.es/webpublica/opendata/votaciones/"
           "Leg15/Sesion202/20260930/Votacion010/VOT_20260930153609.json")
URL_89 = ("https://www.congreso.es/webpublica/opendata/votaciones/"
          "Leg15/Sesion089/20250122/Votacion005/VOT_20250122154430.json")


def _registro() -> dict:
    return json.loads((FIX / "votacion010.json").read_text(encoding="utf-8"))


def _base(tmp_path: Path) -> Path:
    """Base con las 2 votaciones en sus rutas reales de almacenamiento (LegXV/…)."""
    nominal = _registro()
    secreto = _registro()
    secreto["informacion"]["sesion"] = 89
    secreto["informacion"]["numeroVotacion"] = 5
    secreto["informacion"]["fecha"] = "22/1/2025"
    secreto["votaciones"] = []
    raw = tmp_path / "raw" / "LegXV"
    for rel, reg, nombre in (
        ("Sesion202/20260930/Votacion010", nominal, "VOT_20260930153609.json"),
        ("Sesion89/20250122/Votacion005", secreto, "VOT_20250122154430.json"),
    ):
        d = raw / rel
        d.mkdir(parents=True)
        (d / nombre).write_text(json.dumps(reg), encoding="utf-8")
    bd = tmp_path / "data" / "processed" / "congreso.sqlite"
    exportar(sorted(raw.rglob("VOT_*.json")), bd, "XV")
    return bd


def test_cargar_temas_con_separador_real():
    temas = congresoabierto.cargar_temas(FIX / "congresoabierto_temas.csv")
    assert len(temas) == 2
    assert temas[URL_202] == ["igualdad"]
    assert temas[URL_89] == ["justicia", "instituciones"]  # « | », no coma


def test_cmd_temas_cruza_por_fuente_url_y_escribe(tmp_path, monkeypatch, capsys):
    """El cruce usa las URL oficiales (con ordinal y sesión a 3 dígitos) como llave."""
    bd = _base(tmp_path)
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    csv_dir = tmp_path / "data" / "raw" / "congresoabierto"
    csv_dir.mkdir(parents=True)
    (csv_dir / "votaciones.csv").write_text(
        (FIX / "congresoabierto_temas.csv").read_text(encoding="utf-8"), encoding="utf-8"
    )  # ya descargado: descargar_csv no pide red
    assert cli.cmd_temas(types.SimpleNamespace(legislatura="XV")) == 0
    con = sqlite3.connect(bd)
    filas = con.execute("SELECT votacion_id, tema FROM temas_votacion ORDER BY tema").fetchall()
    con.close()
    assert filas == [
        ("Leg202-010", "igualdad"),
        ("Leg89-005", "instituciones"),
        ("Leg89-005", "justicia"),
    ]


def test_temas_en_indice_y_portada(tmp_path):
    """El índice lleva los temas por votación; la portada, el desplegable con cuentas."""
    bd = _base(tmp_path)
    exportar_temas(
        [("Leg202-010", "igualdad"), ("Leg89-005", "justicia"), ("Leg89-005", "instituciones")], bd
    )
    vots = votaciones_recientes(bd, "XV")
    por_id = {v["id"]: v for v in vots}
    assert por_id["Leg202-010"]["temas"] == ["igualdad"]
    assert por_id["Leg89-005"]["temas"] == ["instituciones", "justicia"]  # ordenadas
    temas = temas_con_cuenta(bd, "XV")
    assert temas == [("igualdad", 1), ("instituciones", 1), ("justicia", 1)]  # n desc, luego alfabético
    pagina = generar_portada(vots, tmp_path / "portada.html", "XV", temas).read_text(encoding="utf-8")
    assert '<select id="tema">' in pagina
    assert '<option value="igualdad">igualdad (1)</option>' in pagina
    assert "v.temas.indexOf" in pagina  # el filtro de tema en el cliente
    assert congresoabierto.CITA in pagina and "CC BY 4.0" in pagina  # atribución en el pie


def test_portada_sin_temas_degrada_sin_romperse(tmp_path):
    """Sin tabla de temas, la portada funciona con «Todos» como única opción."""
    bd = _base(tmp_path)
    vots = votaciones_recientes(bd, "XV")
    assert all(v["temas"] == [] for v in vots)
    pagina = generar_portada(vots, tmp_path / "portada.html", "XV", None).read_text(encoding="utf-8")
    assert '<select id="tema">' in pagina
    assert '<option value="todos">Todos</option>' in pagina
    assert 'value="igualdad"' not in pagina
