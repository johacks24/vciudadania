"""Tests sin red: fixture real de la votación 010 de la sesión 202 (30/09/2026)."""

from pathlib import Path

from congreso.fuentes.congreso_es import cargar_registro
from congreso.modelo import RegistroVotacion

FIXTURE = Path(__file__).parent / "fixtures" / "votacion010.json"


def test_parseo_fixture_real():
    reg = RegistroVotacion.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    assert reg.informacion.sesion == 202
    assert reg.informacion.numero_votacion == 10
    assert len(reg.votaciones) == 350
    t = reg.totales
    assert (t.afavor, t.en_contra, t.abstenciones, t.no_votan) == (34, 312, 0, 4)
    assert t.presentes + t.no_votan == 350


def test_validacion_cuadra():
    reg = RegistroVotacion.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    assert reg.validar() == []


def test_recuento_por_grupo():
    reg = RegistroVotacion.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    grupos = {g["grupo"]: g for g in reg.resumen_por_grupo()}
    # Distribución real de la votación 010 (enmienda VOX a la totalidad, devolución):
    assert grupos["GP"]["No"] == 137
    assert grupos["GS"]["No"] == 120
    assert grupos["GVOX"]["Sí"] == 32
    assert grupos["GSUMAR"]["No"] == 24
    # Hubo 2 desviaciones de grupo (1 en GMx y 1 en GSUMAR votaron Sí):
    assert grupos["GMx"]["Sí"] == 1
    assert grupos["GSUMAR"]["Sí"] == 1
    # El PP no registró ninguna desviación en esta votación:
    assert grupos["GP"]["Sí"] == 0 and grupos["GP"]["Abstención"] == 0


def test_registro_sin_individuales_no_es_error():
    reg = RegistroVotacion.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    reg.votaciones = []
    assert reg.sin_voto_individual
    assert reg.validar() == []
