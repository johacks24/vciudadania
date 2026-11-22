"""Tests sin red del cliente: índice de días, URL→sesión/fecha y días sin JSON.

Fixtures: recortes reales de congreso.es del 22/11/2026 (ver cabecera de cada uno).
"""

from pathlib import Path

import pytest

from congreso.fuentes import congreso_es

FIX = Path(__file__).parent / "fixtures"


class _Respuesta:
    """Mínima respuesta HTTPx para tests sin red."""

    def __init__(self, texto: str) -> None:
        self.text = texto

    def raise_for_status(self) -> None:
        pass


def test_dias_votaciones_indice_real(monkeypatch):
    """El índice de la XV trae los 147 días (19/09/2023 → 02/10/2026), únicos y ordenados."""
    html = (FIX / "indice_opendata.html").read_text(encoding="utf-8")
    monkeypatch.setattr(congreso_es.httpx, "get", lambda *a, **k: _Respuesta(html))
    dias = congreso_es.dias_votaciones("XV")
    assert len(dias) == 147
    assert dias[0] == "20230919"
    assert dias[-1] == "20261002"
    assert len(set(dias)) == len(dias)
    assert dias == sorted(dias)


def test_dias_sin_indice_lanza(monkeypatch):
    """Si el Congreso cambia el formato de la página, falla explícito, no silencioso."""
    monkeypatch.setattr(congreso_es.httpx, "get", lambda *a, **k: _Respuesta("<html></html>"))
    with pytest.raises(ValueError):
        congreso_es.dias_votaciones("XV")


def test_sesion_y_fecha_de_url():
    """La URL oficial ya contiene sesión y fecha: no hace falta conocerlas antes."""
    url = (
        "https://www.congreso.es/webpublica/opendata/votaciones/"
        "Leg15/Sesion202/20260930/Votacion010/VOT_20260930153609.json"
    )
    assert congreso_es.sesion_y_fecha_de_url(url) == (202, "20260930")


def test_ruta_cruda_desde_la_propia_url(tmp_path):
    """URL → ruta inmutable: la ingesta de legislatura archiva igual que la del lote 00."""
    url = (
        "https://www.congreso.es/webpublica/opendata/votaciones/"
        "Leg15/Sesion202/20260930/Votacion010/VOT_20260930153609.json"
    )
    sesion, fecha = congreso_es.sesion_y_fecha_de_url(url)
    destino = congreso_es.ruta_cruda(tmp_path, "XV", sesion, fecha, url)
    assert destino == (
        tmp_path / "data" / "raw" / "LegXV" / "Sesion202" / "20260930"
        / "Votacion010" / "VOT_20260930153609.json"
    )


def test_dia_llamamiento_sin_json(monkeypatch):
    """La sesión 203 (2 votaciones públicas por llamamiento) no publica JSON: categoría, no error."""
    html = (FIX / "dia_llamamiento.html").read_text(encoding="utf-8")
    monkeypatch.setattr(congreso_es.httpx, "get", lambda *a, **k: _Respuesta(html))
    assert congreso_es.urls_votaciones("02/10/2026", "XV") == []
