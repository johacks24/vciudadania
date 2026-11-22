"""Tests sin red de la validación en modo legislatura: resumen, categorías y duplicadas."""

import json
import types
from pathlib import Path

import congreso.cli as cli

FIX = Path(__file__).parent / "fixtures"


def _args(**extra):
    base = {"legislatura": "XV", "sesion": None, "fecha": None}
    base.update(extra)
    return types.SimpleNamespace(**base)


def _escribir(base: Path, rel: str, registro: dict) -> None:
    d = base / "data" / "raw" / "LegXV" / rel
    d.mkdir(parents=True, exist_ok=True)
    (d / "VOT_prueba.json").write_text(json.dumps(registro), encoding="utf-8")


def _registro() -> dict:
    return json.loads((FIX / "votacion010.json").read_text(encoding="utf-8"))


def test_resumen_legislatura_con_categorias(tmp_path, monkeypatch, capsys):
    """Modo legislatura: 1 nominal OK + 1 sin voto individual → resumen correcto y código 0."""
    ok = _registro()
    secreto = _registro()
    secreto["informacion"]["numeroVotacion"] = 21  # como el suplicatorio real de la sesión 202
    secreto["votaciones"] = []
    _escribir(tmp_path, "Sesion202/20260930/Votacion010", ok)
    _escribir(tmp_path, "Sesion202/20260930/Votacion021", secreto)
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    assert cli.cmd_validar(_args()) == 0
    salida = capsys.readouterr().out
    assert "2 votaciones: 1 validadas con detalle individual, 1 no nominales" in salida
    assert "0 con descuadre, 0 duplicadas" in salida


def test_duplicada_bloquea_sin_contar_dos_veces(tmp_path, monkeypatch, capsys):
    """El mismo id en dos ficheros → 1 duplicada, código 1, y no inflan los descuadres."""
    _escribir(tmp_path, "Sesion202/20260930/Votacion010", _registro())
    _escribir(tmp_path, "Sesion202/20260931/Votacion010", _registro())  # mismo id: la fuente listó dos
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    assert cli.cmd_validar(_args()) == 1
    salida = capsys.readouterr().out
    assert "1 duplicadas" in salida
    assert "0 con descuadre" in salida
    assert "id duplicado" in salida


def test_descuadre_en_modo_legislatura(tmp_path, monkeypatch, capsys):
    """Modo legislatura imprime solo los problemas; un descuadre basta para código 1."""
    mal = _registro()
    mal["totales"]["afavor"] += 1
    _escribir(tmp_path, "Sesion202/20260930/Votacion010", mal)
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    assert cli.cmd_validar(_args()) == 1
    salida = capsys.readouterr().out
    assert "≠ oficial" in salida
    assert salida.count("≠") == 1  # solo el problema, sin tabla de 2.175 líneas


def test_sesion_y_fecha_van_juntas(tmp_path, monkeypatch):
    """`--sesion` sin `--fecha` (o al revés) avisa en vez de romperse (comando defensivo)."""
    monkeypatch.setattr(cli, "RAIZ", tmp_path)
    assert cli.cmd_validar(_args(sesion=202)) == 1
    assert cli.cmd_validar(_args(fecha="2026-09-30")) == 1
