"""Tests sin red del dataset descargable (D.1): JSON + CSV con su cita (recorrido 4)."""

import csv
import json
from pathlib import Path

from congreso.exportar_datos import CITA_NUESTRA, LICENCIA, generar_datos
from congreso.exportar_portada import generar_portada, votaciones_recientes
from congreso.exportar_sqlite import exportar_temas
from congreso.tests.test_temas import _base


def test_json_autodescriptivo_con_cita(tmp_path):
    bd = _base(tmp_path)
    exportar_temas(
        [("Leg202-010", "igualdad"), ("Leg89-005", "justicia"), ("Leg89-005", "instituciones")], bd
    )
    vots = votaciones_recientes(bd, "XV")
    j, _ = generar_datos(vots, tmp_path / "datos", "XV")
    datos = json.loads(j.read_text(encoding="utf-8"))
    assert datos["legislatura"] == "XV" and datos["n"] == 2
    assert datos["cita"] == CITA_NUESTRA
    assert "CC BY-SA 4.0" in datos["licencia"] and "Congreso Abierto" in datos["licencia"]
    assert datos["fuente"] == "https://www.congreso.es/es/opendata"
    por_id = {v["id"]: v for v in datos["votaciones"]}
    assert por_id["Leg89-005"]["temas"] == ["instituciones", "justicia"]
    # cada dato lleva su enlace oficial (trazabilidad dentro del propio dataset)
    assert por_id["Leg202-010"]["fuente"] == (
        "https://www.congreso.es/webpublica/opendata/votaciones/"
        "Leg15/Sesion202/20260930/Votacion010/VOT_20260930153609.json"
    )


def test_csv_una_fila_por_votacion_con_su_fuente(tmp_path):
    bd = _base(tmp_path)
    exportar_temas([("Leg202-010", "igualdad")], bd)
    vots = votaciones_recientes(bd, "XV")
    _, c = generar_datos(vots, tmp_path / "datos", "XV")
    with c.open(encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    assert len(filas) == 2
    nominal = [r for r in filas if r["id"] == "Leg202-010"][0]
    secreta = [r for r in filas if r["id"] == "Leg89-005"][0]
    assert nominal["voto_individual"] == "si"
    assert nominal["temas"] == "igualdad"  # separador « | » como el de la fuente
    assert nominal["fuente"].startswith("https://www.congreso.es/webpublica/opendata/votaciones/Leg15/")
    assert secreta["voto_individual"] == "no"  # suplicatorio: categoría visible en el dato
    assert secreta["fuente"].endswith("/Leg15/Sesion089/20250122/Votacion005/VOT_20250122154430.json")
    # el título con comas sobrevive al CSV (quoting del módulo csv)
    assert nominal["titulo"] == vots[0]["titulo"] or nominal["titulo"] == [v for v in vots if v["id"] == "Leg202-010"][0]["titulo"]


def test_portada_enlaza_el_dataset_con_su_cita(tmp_path):
    bd = _base(tmp_path)
    vots = votaciones_recientes(bd, "XV")
    pagina = generar_portada(vots, tmp_path / "portada.html", "XV", None).read_text(encoding="utf-8")
    assert "Descarga los datos" in pagina
    # dirección de diseño (23/11/2026): la descarga va ANTES de la lista — con scroll
    # infinito de 2.175 elementos, al final de la página no se ve.
    assert pagina.index('<section class="descarga">') < pagina.index('<ol id="lista">')
    assert 'href="datos/votaciones.csv"' in pagina and 'href="datos/votaciones.json"' in pagina
    assert CITA_NUESTRA in pagina and "CC BY-SA 4.0" in pagina
    assert "CC BY 4.0" in pagina  # la de los temas
    assert "2 votaciones" in pagina  # el tamaño del dataset, en contexto
