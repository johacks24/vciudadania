"""Tests sin red de la tabla de diputados: esquema, carga, exportadores y SQLite."""

import json
import shutil
import sqlite3
from pathlib import Path

import pytest

from congreso.exportar_sqlite import exportar_diputados
from congreso.fuentes import congreso_es
from congreso.fuentes.congreso_es import cargar_diputados, urls_diputados
from congreso.modelo import Diputado

FIX = Path(__file__).parent / "fixtures"


class _Respuesta:
    def __init__(self, texto: str) -> None:
        self.text = texto

    def raise_for_status(self) -> None:
        pass


def _escribir_exportadores(base: Path) -> None:
    """data/raw/LegXV/diputados/ con los fixtures reales (activos + bajas)."""
    d = base / "data" / "raw" / "LegXV" / "diputados"
    d.mkdir(parents=True)
    for f in ("diputados_activos.json", "diputados_bajas.json"):
        origen = FIX / f
        destino = d / ("DiputadosActivos__20261122050006.json" if "activos" in f else "DiputadosDeBaja__20261122050008.json")
        # el fixture lleva una cabecera de comentario: el JSON empieza en el primer [
        texto = origen.read_text(encoding="utf-8")
        destino.write_text(texto[texto.index("[") :], encoding="utf-8")


def _diputados_fixture() -> list[Diputado]:
    out = []
    for f in ("diputados_activos.json", "diputados_bajas.json"):
        texto = (FIX / f).read_text(encoding="utf-8")
        for datos in json.loads(texto[texto.index("[") :]):
            out.append(Diputado.model_validate({**datos, "legislatura": "XV"}))
    return out


def test_parseo_fixture_real():
    """Campos con alias oficiales; activos sin fecha de baja; cambio de grupo de Belarra."""
    dip = {d.nombre: d for d in _diputados_fixture()}
    abascal = dip["Abascal Conde, Santiago"]
    assert (abascal.circunscripcion, abascal.formacion, abascal.grupo) == (
        "Madrid", "VOX", "Grupo Parlamentario VOX"
    )
    assert abascal.fecha_baja == ""  # activo: el exportador no trae FECHABAJA
    belarra = dip["Belarra Urteaga, Ione"]
    assert belarra.grupo == "Grupo Parlamentario Mixto"
    assert belarra.fecha_alta_grupo == "05/12/2023"  # cambio de grupo, no constitución
    abades = dip["Abades Martínez, Cristina"]
    assert abades.fecha_baja == "06/10/2026"  # disolución


def test_cargar_diputados_desde_raw(tmp_path):
    _escribir_exportadores(tmp_path)
    diputados = cargar_diputados(tmp_path, "XV")
    assert len(diputados) == 4
    assert {d.legislatura for d in diputados} == {"XV"}
    assert len({d.nombre for d in diputados}) == 4  # clave natural sin duplicados


def test_cargar_diputados_rechaza_duplicado(tmp_path):
    _escribir_exportadores(tmp_path)
    mala = tmp_path / "data" / "raw" / "LegXV" / "diputados" / "DiputadosDeBaja__20261122050008.json"
    datos = json.loads(mala.read_text(encoding="utf-8"))
    datos[0]["NOMBRE"] = "Abascal Conde, Santiago"  # ya existe en activos
    mala.write_text(json.dumps(datos), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicado"):
        cargar_diputados(tmp_path, "XV")


def test_cargar_toma_el_ultimo_exportador(tmp_path):
    """Los exportadores rotan a diario: de cada clase, el de mayor marca temporal."""
    _escribir_exportadores(tmp_path)
    d = tmp_path / "data" / "raw" / "LegXV" / "diputados"
    solo_abascal = json.dumps(
        [{"NOMBRE": "Abascal Conde, Santiago", "CIRCUNSCRIPCION": "Madrid",
          "FORMACIONELECTORAL": "VOX", "FECHAALTA": "16/08/2023",
          "GRUPOPARLAMENTARIO": "Grupo Parlamentario VOX",
          "FECHAALTAENGRUPOPARLAMENTARIO": "18/08/2023"}]
    )
    (d / "DiputadosActivos__20261123050000.json").write_text(solo_abascal, encoding="utf-8")
    nombres = {x.nombre for x in cargar_diputados(tmp_path, "XV")}
    assert "Abascal Conde, Santiago" in nombres
    assert "Belarra Urteaga, Ione" not in nombres  # solo estaba en el exportador viejo


def test_urls_diputados_filtra_los_de_la_legislatura_actual(monkeypatch):
    """De la página del opendata solo Activos + DeBaja, pese al ruido (históricos, global…).

    Aserta las URLs completas: una aserción de subcadenas dio por buena una URL rota
    (lección 4x4 nº 6).
    """
    html = (FIX / "opendata_diputados.html").read_text(encoding="utf-8")
    monkeypatch.setattr(congreso_es.httpx, "get", lambda *a, **k: _Respuesta(html))
    assert urls_diputados() == [
        "https://www.congreso.es/webpublica/opendata/diputados/DiputadosActivos__20261122050006.json",
        "https://www.congreso.es/webpublica/opendata/diputados/DiputadosDeBaja__20261122050008.json",
    ]


def test_exportar_diputados_sqlite(tmp_path):
    """Tabla por legislatura: idempotente y sin borrar las demás legislaturas."""
    bd_path = tmp_path / "congreso.sqlite"
    diputados = _diputados_fixture()
    assert exportar_diputados(diputados, bd_path, "XV") == 4
    assert exportar_diputados(diputados, bd_path, "XV") == 4  # idempotente
    uno_xiv = Diputado.model_validate(
        {"NOMBRE": "Prueba, Diputada", "CIRCUNSCRIPCION": "Madrid", "FORMACIONELECTORAL": "PP",
         "FECHAALTA": "01/01/2020", "GRUPOPARLAMENTARIO": "Grupo Parlamentario Popular en el Congreso",
         "legislatura": "XIV"}
    )
    exportar_diputados([uno_xiv], bd_path, "XIV")
    bd = sqlite3.connect(bd_path)
    total, por_leg = bd.execute(
        "SELECT COUNT(*), COUNT(DISTINCT legislatura) FROM diputados"
    ).fetchone()
    assert (total, por_leg) == (5, 2)  # la XIV no borró la XV
    grupo_belarra = bd.execute(
        "SELECT grupo FROM diputados WHERE nombre = 'Belarra Urteaga, Ione'"
    ).fetchone()[0]
    bd.close()
    assert grupo_belarra == "Grupo Parlamentario Mixto"
