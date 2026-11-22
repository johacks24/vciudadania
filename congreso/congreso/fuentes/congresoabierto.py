"""Fuente secundaria: CongresoAbierto (congresoabierto.org), código MIT + datos CC BY 4.0.

ADR-0005, punto 3: sus datos derivados se usan como fuente secundaria CON
atribución y validación nuestra, jamás sin contrastar. Aquí: la asignación de
tema por votación (columna `temas` de su CSV público), que alimenta el filtro por
tema del recorrido 2. El contraste es el cruce por `url_votacion` (la URL oficial
del JSON de cada votación) contra nuestra tabla `votaciones`: con la XV cerrada,
2.175 filas suyas cruzan con las 2.175 nuestras (verificado el 23/11/2026).

Cita exigida por la licencia (CC BY 4.0): Congreso Abierto (congresoabierto.org),
a partir de datos oficiales del Congreso de los Diputados.
"""

from __future__ import annotations

import csv
from pathlib import Path

import httpx

URL_CSV = "https://congresoabierto.org/datos/csv/votaciones.csv"
CITA = "Congreso Abierto (congresoabierto.org), a partir de datos oficiales del Congreso de los Diputados"


def descargar_csv(destino: Path) -> Path:
    """Descarga idempotente del CSV de votaciones (inmutable en data/raw)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        r = httpx.get(URL_CSV, timeout=60, follow_redirects=True)
        r.raise_for_status()
        destino.write_bytes(r.content)
    return destino


def cargar_temas(fichero: Path) -> dict[str, list[str]]:
    """{url_votacion: [tema, …]} desde su CSV (columna `temas`, separada por « | »).

    Valores reales verificados el 23/11/2026 sobre la XV completa: 2.175 filas,
    todas con tema, separador « | » (299 votaciones con varios temas; p. ej., el
    suplicatorio de la sesión 89: «justicia | instituciones») y **15 temas**
    distintos, del más frecuente al menos: otros (749), transporte, economía,
    justicia, trabajo, sanidad, instituciones, igualdad, territorio, vivienda…
    La asignación es por expediente con reglas por palabras documentadas en su
    metodología.
    """
    with fichero.open(encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    temas: dict[str, list[str]] = {}
    for r in filas:
        lista = [t.strip() for t in r.get("temas", "").split("|") if t.strip()]
        if lista:
            temas[r["url_votacion"]] = lista
    return temas
