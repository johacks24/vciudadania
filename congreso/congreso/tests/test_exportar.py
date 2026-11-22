"""Tests sin red de la exportación en modo legislatura: tablas completas y consistencia."""

import json
import sqlite3
import types
from pathlib import Path

import congreso.cli as cli
from congreso.tests.test_diputados import _escribir_exportadores

FIX = Path(__file__).parent / "fixtures"


def _args(**extra):
    base = {"legislatura": "XV", "sesion": None, "fecha": None}
    base.update(extra)
    return types.SimpleNamespace(**base)


def _escribir_votacion(base: Path, rel: str, registro: dict) -> None:
    d = base / "data" / "raw" / "LegXV" / rel
    d.mkdir(parents=True, exist_ok=True)
    (d / "VOT_prueba.json").write_text(json.dumps(registro), encoding="utf-8")


def _registro() -> dict:
    return json.loads((FIX / "votacion010.json").read_text(encoding="utf-8"))


def _escribir_xv(base: Path) -> None:
    """Una votación nominal (sesión 202) y una sin voto individual (sesión 89)."""
    nominal = _registro()
    _escribir_votacion(base, "Sesion202/20260930/Votacion010", nominal)
    secreto = _registro()
    secreto["informacion"]["numeroVotacion"] = 5  # como el suplicatorio real de la sesión 89
    secreto["votaciones"] = []
    _escribir_votacion(base, "Sesion89/20250122/Votacion005", secreto)


def _consultar(bd_path: Path) -> dict[str, int]:
    bd = sqlite3.connect(bd_path)
    out = {
        t: bd.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("votaciones", "votos", "resumen_grupos", "diputados")
    }
    out["sin_individual"] = bd.execute(
        "SELECT COUNT(*) FROM votaciones WHERE sin_voto_individual = 1"
    ).fetchone()[0]
    bd.close()
    return out


def test_exportar_legislatura_completa(tmp_path, monkeypatch):
    """Las cuatro tablas de la legislatura en una sola base."""
    _escribir_xv(tmp_path)
    _escribir_exportadores(tmp_path)
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    assert cli.cmd_exportar(_args()) == 0
    c = _consultar(tmp_path / "data" / "processed" / "congreso.sqlite")
    assert c["votaciones"] == 2
    assert c["sin_individual"] == 1  # el suplicatorio de la sesión 89
    assert c["votos"] == 350  # solo la nominal (la secreta no publica individuales)
    assert c["resumen_grupos"] == 9  # los 9 grupos de la votación 010
    assert c["diputados"] == 4


def test_exportar_legislatura_sin_diputados_falla_rapido(tmp_path, monkeypatch):
    """Sin exportadores de diputados: código 1 y la base existente queda intacta."""
    _escribir_xv(tmp_path)
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    # una exportación de sesión primero (crea la base con lo suyo)
    assert cli.cmd_exportar(_args(sesion=202, fecha="2026-09-30")) == 0
    antes = _consultar(tmp_path / "data" / "processed" / "congreso.sqlite")
    # la de legislatura sin exportadores de diputados: falla antes de escribir nada
    assert cli.cmd_exportar(_args()) == 1
    assert _consultar(tmp_path / "data" / "processed" / "congreso.sqlite") == antes


def test_reconstruccion_limpia_entre_modos(tmp_path, monkeypatch):
    """Después de una sesión, la base no guarda votaciones huérfanas de la legislatura."""
    _escribir_xv(tmp_path)
    _escribir_exportadores(tmp_path)
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    assert cli.cmd_exportar(_args()) == 0  # legislatura: 2 votaciones
    assert cli.cmd_exportar(_args(sesion=202, fecha="2026-09-30")) == 0  # sesión: 1
    c = _consultar(tmp_path / "data" / "processed" / "congreso.sqlite")
    assert c["votaciones"] == 1  # la de la sesión 89 no sobrevive huérfana
    assert c["votos"] == 350
    assert c["diputados"] == 4  # la tabla de diputados no se toca en modo sesión


def test_exportar_legislatura_es_idempotente(tmp_path, monkeypatch):
    _escribir_xv(tmp_path)
    _escribir_exportadores(tmp_path)
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    assert cli.cmd_exportar(_args()) == 0
    primera = _consultar(tmp_path / "data" / "processed" / "congreso.sqlite")
    assert cli.cmd_exportar(_args()) == 0
    assert _consultar(tmp_path / "data" / "processed" / "congreso.sqlite") == primera
