"""CLI: congreso ingesta (un día o toda la legislatura) | validar | exportar"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

from .exportar_ficha import generar as generar_ficha
from .exportar_sqlite import exportar as exportar_sqlite
from .exportar_sqlite import exportar_diputados
from .fuentes.congreso_es import (
    cargar_diputados,
    cargar_registro,
    descargar,
    dias_votaciones,
    ruta_cruda,
    ruta_diputados,
    sesion_y_fecha_de_url,
    urls_diputados,
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


def _ficheros_crudos_legislatura(raiz: Path, legislatura: str) -> list[Path]:
    """Todos los VOT_*.json descargados de la legislatura (cualquier sesión y fecha)."""
    return sorted((raiz / "data" / "raw" / f"Leg{legislatura}").rglob("VOT_*.json"))


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
        time.sleep(PAUSA)  # la página del día también es una petición: pausa educada
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
    if bool(args.sesion) != bool(args.fecha):
        LOG.error("--sesion y --fecha van juntas: ambas (una sesión) o ninguna (toda la legislatura).")
        return 1
    if args.sesion:
        ficheros = _ficheros_crudos(RAIZ, args.legislatura, args.sesion, args.fecha)
    else:
        ficheros = _ficheros_crudos_legislatura(RAIZ, args.legislatura)
    if not ficheros:
        LOG.error("No hay datos descargados: ejecuta primero `make ingesta`.")
        return 1
    detallado = bool(args.sesion)  # una sesión: tabla por votación; legislatura: solo problemas
    fallos, sin_individuales, duplicadas = 0, 0, 0
    vistas: set[str] = set()
    if detallado:
        print(f"{'votación':<12}{'Sí':>5}{'No':>5}{'Abst':>6}{'NoVota':>8}  estado")
    for f in ficheros:
        reg = cargar_registro(f)
        descuadres = list(reg.validar())
        duplicada = reg.id in vistas
        if duplicada:
            duplicadas += 1
        vistas.add(reg.id)
        if reg.sin_voto_individual:
            sin_individuales += 1
        elif descuadres:
            fallos += 1
        problemas = descuadres + (["id duplicado: la fuente listó esta votación dos veces"] if duplicada else [])
        t = reg.totales
        estado = "; ".join(problemas) or (
            "OK (sin voto individual publicado)" if reg.sin_voto_individual else "OK"
        )
        if detallado or problemas:
            print(f"{reg.id:<12}{t.afavor:>5}{t.en_contra:>5}{t.abstenciones:>6}{t.no_votan:>8}  {estado}")
    total = len(ficheros)
    print(
        f"\n{total} votaciones: {total - fallos - sin_individuales} validadas con detalle "
        f"individual, {sin_individuales} no nominales, {fallos} con descuadre, {duplicadas} duplicadas."
    )
    if fallos or duplicadas:
        LOG.error("Validación FALLIDA: %d con descuadre, %d duplicadas. Publicación bloqueada.", fallos, duplicadas)
        return 1
    LOG.info("Validación 100%% correcta contra los totales oficiales (%d votaciones, Leg%s).", total, args.legislatura)
    return 0


def cmd_exportar(args: argparse.Namespace) -> int:
    if bool(args.sesion) != bool(args.fecha):
        LOG.error("--sesion y --fecha van juntas: ambas (una sesión) o ninguna (toda la legislatura).")
        return 1
    destino = RAIZ / "data" / "processed" / "congreso.sqlite"
    if args.sesion:
        ficheros = _ficheros_crudos(RAIZ, args.legislatura, args.sesion, args.fecha)
    else:
        ficheros = _ficheros_crudos_legislatura(RAIZ, args.legislatura)
    if not ficheros:
        LOG.error("No hay datos descargados: ejecuta primero `make ingesta`.")
        return 1
    diputados = None
    if not args.sesion:
        # La XV completa incluye la tabla de diputados: se carga ANTES de escribir nada
        # (si falta, falla rápido sin dejar una base a medias).
        try:
            diputados = cargar_diputados(RAIZ, args.legislatura)
        except ValueError as e:
            LOG.error("%s", e)
            return 1
    informe = exportar_sqlite(ficheros, destino, args.legislatura)
    malas = [i for i, ok in informe if not ok]
    LOG.info("SQLite: %d votaciones (%d con descuadre marcado).", len(informe), len(malas))
    if args.sesion:
        # La web completa de la XV (portada, buscador, ~2.190 fichas) llega en C;
        # en modo sesión se mantiene la ficha del lote 00.
        ficha = generar_ficha(ficheros, RAIZ / "web" / "index.html", args.legislatura)
        LOG.info("Ficha generada: %s", ficha.relative_to(RAIZ))
    else:
        n = exportar_diputados(diputados, destino, args.legislatura)
        LOG.info("SQLite Leg%s completa: %d votaciones + %d diputados.", args.legislatura, len(informe), n)
    return 0


def cmd_diputados(args: argparse.Namespace) -> int:
    """Descarga los exportadores (activos + bajas), carga la tabla y la escribe en SQLite."""
    for url in urls_diputados():
        destino = ruta_diputados(RAIZ, args.legislatura, url)
        if destino.exists():
            continue  # data/raw inmutable e idempotente
        descargar(url, destino)
        LOG.info("Descargado %s", destino.relative_to(RAIZ))
        time.sleep(PAUSA)
    diputados = cargar_diputados(RAIZ, args.legislatura)
    n = exportar_diputados(diputados, RAIZ / "data" / "processed" / "congreso.sqlite", args.legislatura)
    activos = sum(1 for d in diputados if not d.fecha_baja)
    print(
        f"\n{len(diputados)} diputados de la Leg{args.legislatura}: "
        f"{activos} activos, {len(diputados) - activos} con baja."
    )
    LOG.info(
        "Tabla diputados: %d registros (%d activos, %d con baja) en SQLite.",
        n, activos, len(diputados) - activos,
    )
    return 0


def main() -> None:
    p = argparse.ArgumentParser(prog="congreso", description="Ingesta y validación de votaciones del Congreso")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ingesta", help="descargar votaciones: un día (--fecha) o toda la legislatura")
    s.add_argument("--legislatura", default="XV")
    s.add_argument("--fecha", default=None, help="formato AAAA-MM-DD; sin ella, toda la legislatura")
    s.set_defaults(fn=cmd_ingesta)

    s = sub.add_parser("diputados", help="descargar y cargar la tabla de diputados (activos + bajas)")
    s.add_argument("--legislatura", default="XV")
    s.set_defaults(fn=cmd_diputados)

    s = sub.add_parser("validar", help="cuadrar recuentos contra totales oficiales: una sesión o toda la legislatura")
    s.add_argument("--legislatura", default="XV")
    s.add_argument("--sesion", type=int, default=None)
    s.add_argument("--fecha", default=None, help="formato AAAA-MM-DD")
    s.set_defaults(fn=cmd_validar)

    s = sub.add_parser("exportar", help="generar SQLite y ficha: una sesión o toda la legislatura")
    s.add_argument("--legislatura", default="XV")
    s.add_argument("--sesion", type=int, default=None)
    s.add_argument("--fecha", default=None, help="formato AAAA-MM-DD")
    s.set_defaults(fn=cmd_exportar)

    args = p.parse_args()
    RAIZ.joinpath("data").mkdir(exist_ok=True)
    _configurar_log(RAIZ)
    sys.exit(args.fn(args))
