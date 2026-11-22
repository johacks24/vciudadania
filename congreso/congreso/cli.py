"""CLI: congreso ingesta (un día o toda la legislatura) | validar | exportar"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

from .exportar_ficha import generar as generar_ficha
from .exportar_sqlite import exportar as exportar_sqlite
from .fuentes.congreso_es import (
    cargar_registro,
    descargar,
    dias_votaciones,
    ruta_cruda,
    sesion_y_fecha_de_url,
    urls_votaciones,
)

RAIZ = Path(__file__).resolve().parents[2]  # raíz del repo
LOG = logging.getLogger("congreso")
PAUSA = 0.5  # pausa educada entre descargas (quevotan usa 0,5 s)


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


def _fecha_compacta(fecha_iso: str) -> str:
    return fecha_iso.replace("-", "")


def _ficheros_crudos(raiz: Path, legislatura: str, sesion: int, fecha_iso: str) -> list[Path]:
    base = raiz / "data" / "raw" / f"Leg{legislatura}" / f"Sesion{sesion}" / _fecha_compacta(fecha_iso)
    return sorted(base.rglob("VOT_*.json"))


def cmd_ingesta(args: argparse.Namespace) -> int:
    raiz = RAIZ
    if args.fecha:
        dias = [_fecha_compacta(args.fecha)]
    else:
        dias = dias_votaciones(args.legislatura)
        LOG.info("Enumeración: %d días con votaciones en Leg%s", len(dias), args.legislatura)
    nuevos = 0
    for dia in dias:
        fecha_dma = f"{dia[6:8]}/{dia[4:6]}/{dia[0:4]}"
        urls = urls_votaciones(fecha_dma, args.legislatura)
        LOG.info("Día %s: %d votaciones con JSON publicado", dia, len(urls))
        if not urls:
            if args.fecha:
                LOG.error(
                    "0 votaciones con JSON para %s: ¿fecha correcta? Un día con solo "
                    "votaciones públicas por llamamiento no publica JSON (p. ej. sesión 203).",
                    args.fecha,
                )
                return 1
            continue  # en modo legislatura, día sin JSON es una categoría, no un error
        for url in urls:
            sesion, fecha_url = sesion_y_fecha_de_url(url)
            destino = ruta_cruda(raiz, args.legislatura, sesion, fecha_url, url)
            if destino.exists():
                continue  # data/raw es inmutable e idempotente: no se re-descarga
            descargar(url, destino)
            nuevos += 1
            LOG.info("Descargado %s", destino.relative_to(raiz))
            time.sleep(PAUSA)
    LOG.info(
        "Ingesta completa (%s): %d ficheros nuevos en data/raw (inmutables).",
        args.fecha or f"Leg{args.legislatura}", nuevos,
    )
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

    s = sub.add_parser("ingesta", help="descargar votaciones: un día (--fecha) o toda la legislatura")
    s.add_argument("--legislatura", default="XV")
    s.add_argument("--fecha", default=None, help="formato AAAA-MM-DD; sin ella, toda la legislatura")
    s.set_defaults(fn=cmd_ingesta)

    for nombre, fn in (("validar", cmd_validar), ("exportar", cmd_exportar)):
        s = sub.add_parser(nombre)
        s.add_argument("--legislatura", default="XV")
        s.add_argument("--sesion", type=int, required=True)
        s.add_argument("--fecha", required=True, help="formato AAAA-MM-DD")
        s.set_defaults(fn=fn)

    args = p.parse_args()
    RAIZ.joinpath("data").mkdir(exist_ok=True)
    _configurar_log(RAIZ)
    sys.exit(args.fn(args))
