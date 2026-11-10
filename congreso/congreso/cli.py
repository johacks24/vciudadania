"""CLI: congreso ingesta | validar | exportar"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .exportar_ficha import generar as generar_ficha
from .exportar_sqlite import exportar as exportar_sqlite
from .fuentes.congreso_es import descargar, ruta_cruda, urls_votaciones, cargar_registro

RAIZ = Path(__file__).resolve().parents[2]  # raíz del repo
LOG = logging.getLogger("congreso")


def _configurar_log(raiz: Path) -> None:
    """Log combinado a data/proceso.log + stderr (capa de conciencia, regla 4x4)."""
    LOG.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    for h in (
        logging.FileHandler(raiz / "data" / "proceso.log", encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ):
        h.setFormatter(fmt)
        LOG.addHandler(h)


def _fecha_dma(fecha_iso: str) -> str:
    """2026-09-30 → 30/09/2026 (formato que espera la página del Congreso)."""
    a, m, d = fecha_iso.split("-")
    return f"{d}/{m}/{a}"


def _fecha_compacta(fecha_iso: str) -> str:
    return fecha_iso.replace("-", "")


def _ficheros_crudos(raiz: Path, legislatura: str, sesion: int, fecha_iso: str) -> list[Path]:
    base = raiz / "data" / "raw" / f"Leg{legislatura}" / f"Sesion{sesion}" / _fecha_compacta(fecha_iso)
    return sorted(base.rglob("VOT_*.json"))


def cmd_ingesta(args: argparse.Namespace) -> int:
    raiz = RAIZ
    urls = urls_votaciones(_fecha_dma(args.fecha), args.legislatura)
    LOG.info("Enumeración: %d votaciones encontradas para %s (Leg%s)", len(urls), args.fecha, args.legislatura)
    if not urls:
        LOG.error("No se encontraron votaciones: revisa fecha y legislatura.")
        return 1
    for url in urls:
        destino = ruta_cruda(raiz, args.legislatura, args.sesion, _fecha_compacta(args.fecha), url)
        descargar(url, destino)
        LOG.info("Descargado %s", destino.relative_to(raiz))
    LOG.info("Ingesta completa: %d ficheros en data/raw (inmutables).", len(urls))
    return 0


def cmd_validar(args: argparse.Namespace) -> int:
    ficheros = _ficheros_crudos(RAIZ, args.legislatura, args.sesion, args.fecha)
    if not ficheros:
        LOG.error("No hay datos descargados: ejecuta primero `make ingesta`.")
        return 1
    fallos, sin_individuales = 0, 0
    print(f"{'votación':<12}{'Sí':>5}{'No':>5}{'Abst':>6}{'NoVota':>8}  estado")
    for f in ficheros:
        reg = cargar_registro(f)
        d = reg.validar()
        t = reg.totales
        estado = "OK" if not d else "DESCUADRE: " + "; ".join(d)
        if reg.sin_voto_individual:
            sin_individuales += 1
            estado = "OK (sin voto individual publicado)"
        elif d:
            fallos += 1
        print(f"{reg.id:<12}{t.afavor:>5}{t.en_contra:>5}{t.abstenciones:>6}{t.no_votan:>8}  {estado}")
    total = len(ficheros)
    print(
        f"\n{total} votaciones: {total - fallos - sin_individuales} validadas con detalle "
        f"individual, {sin_individuales} no nominales, {fallos} con descuadre."
    )
    if fallos:
        LOG.error("Validación FALLIDA: %d votaciones con descuadre. Publicación bloqueada.", fallos)
        return 1
    LOG.info("Validación 100%% correcta contra los totales oficiales.")
    return 0


def cmd_exportar(args: argparse.Namespace) -> int:
    ficheros = _ficheros_crudos(RAIZ, args.legislatura, args.sesion, args.fecha)
    if not ficheros:
        LOG.error("No hay datos descargados: ejecuta primero `make ingesta`.")
        return 1
    informe = exportar_sqlite(ficheros, RAIZ / "data" / "processed" / "congreso.sqlite", args.legislatura)
    malas = [i for i, ok in informe if not ok]
    LOG.info("SQLite: %d votaciones (%d con descuadre marcado).", len(informe), len(malas))
    ficha = generar_ficha(ficheros, RAIZ / "web" / "index.html", args.legislatura)
    LOG.info("Ficha generada: %s", ficha.relative_to(RAIZ))
    return 0


def main() -> None:
    p = argparse.ArgumentParser(prog="congreso", description="Ingesta y validación de votaciones del Congreso")
    sub = p.add_subparsers(dest="cmd", required=True)
    for nombre, fn in (("ingesta", cmd_ingesta), ("validar", cmd_validar), ("exportar", cmd_exportar)):
        s = sub.add_parser(nombre)
        s.add_argument("--legislatura", default="XV")
        s.add_argument("--sesion", type=int, required=True)
        s.add_argument("--fecha", required=True, help="formato AAAA-MM-DD")
        s.set_defaults(fn=fn)
    args = p.parse_args()
    RAIZ.joinpath("data").mkdir(exist_ok=True)
    _configurar_log(RAIZ)
    sys.exit(args.fn(args))
