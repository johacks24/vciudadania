"""Tests sin red de las fichas por votación (C.4): waffle, tabla, fuente y temas.

La base de pruebas (de test_temas) guarda la votación 010 de la sesión 202 en su
ruta real (raw/LegXV/Sesion202/…/VOT_20260930153609.json) para que la fuente_url
sea la oficial, y el suplicatorio de la 89 sin voto individual.
"""

import json
import re
from pathlib import Path

from congreso.exportar_ficha import GRUPOS, _waffle, generar_fichas
from congreso.exportar_sqlite import exportar_temas
from congreso.tests.test_temas import _base

FIX = Path(__file__).parent / "fixtures"


def _leer(tmp_path: Path, fichero: str) -> str:
    return (tmp_path / "data" / "web" / fichero).read_text(encoding="utf-8")


def test_waffle_estructura_de_unidades():
    """Celda por diputado, color de grupo, secciones por sentido con su número."""
    votos = (
        [{"diputado": f"Diputada {i}", "grupo": "GS", "voto": "Sí"} for i in range(2)]
        + [{"diputado": "Diputado 3", "grupo": "GS", "voto": "No"}]
        + [{"diputado": f"Diputado {i}", "grupo": "GP", "voto": "No"} for i in (4, 5)]
    )
    svg = _waffle(votos)
    assert svg.count("<rect ") == 5
    assert ">Sí 2<" in svg and ">No 3<" in svg and ">Abstención 0<" in svg and ">No vota 0<" in svg
    assert svg.count(f'fill="{GRUPOS["GS"][2]}"') == 3  # 2 Sí + 1 No del GS
    assert svg.count(f'fill="{GRUPOS["GP"][2]}"') == 2
    # detalle a demanda: el nombre del diputado está, pero fuera de las celdas no hay texto
    assert "Diputada 0 (GS): Sí" in svg


def test_ficha_nominal_con_waffle_y_tabla(tmp_path):
    bd = _base(tmp_path)
    exportar_temas([("Leg202-010", "igualdad")], bd)
    n = generar_fichas(bd, tmp_path / "data" / "web" / "votacion", "XV")
    assert n == 2

    pagina = _leer(tmp_path, "votacion/Leg202-010.html")
    assert pagina.count("<rect ") == 350  # una celda por diputado
    assert ">Sí 34<" in pagina and ">No 312<" in pagina  # cabeceras con el recuento oficial
    assert "Más No que Sí." in pagina  # honesto: no dice «Rechazada»
    assert "Sesión 202" in pagina and "votación nº 10" in pagina
    # leyenda: chip + sigla + nombre oficial, en el orden de bloques
    assert "PP — Grupo Parlamentario Popular en el Congreso" in pagina
    assert "PSOE — Grupo Parlamentario Socialista" in pagina
    assert pagina.count("<tr><td>") == 9  # los 9 grupos de la votación
    # el primer voto individual del fixture, con su detalle a demanda
    primero = json.loads((FIX / "votacion010.json").read_text(encoding="utf-8"))["votaciones"][0]
    assert f"{primero['diputado']} ({primero['grupo']}): {primero['voto']}" in pagina
    # fuente oficial: URL completa con ordinal y sesión (lección 4x4 nº 7)
    assert 'href="https://www.congreso.es/webpublica/opendata/votaciones/Leg15/Sesion202/20260930/Votacion010/VOT_20260930153609.json"' in pagina
    # tema visible y atribución
    assert "Tema:" in pagina and "igualdad" in pagina and "CC BY 4.0" in pagina
    # navegación de vuelta
    assert '<a href="../">← Todas las votaciones</a>' in pagina


def test_ficha_sin_voto_individual_solo_totales(tmp_path):
    bd = _base(tmp_path)
    generar_fichas(bd, tmp_path / "data" / "web" / "votacion", "XV")
    pagina = _leer(tmp_path, "votacion/Leg89-005.html")
    assert "<svg" not in pagina  # sin waffle: no hay voto individual publicado
    assert "Votación no nominal" in pagina and "solo se publican los totales oficiales" in pagina
    assert "Sin voto por grupo" in pagina
    # y también con su fuente oficial (sesión con relleno a 3 dígitos)
    assert "/Leg15/Sesion089/20250122/Votacion005/VOT_20250122154430.json" in pagina


def test_fichas_se_regeneran_completas(tmp_path):
    """Re-ejecutar no deja fichas huérfanas de votaciones que ya no están."""
    bd = _base(tmp_path)
    destino = tmp_path / "data" / "web" / "votacion"
    assert generar_fichas(bd, destino, "XV") == 2
    huerfana = destino / "Leg99-999.html"
    huerfana.write_text("vieja", encoding="utf-8")
    assert generar_fichas(bd, destino, "XV") == 2
    assert not huerfana.exists()
    assert len(list(destino.glob("*.html"))) == 2
