"""Cliente de la fuente primaria: datos abiertos del Congreso de los Diputados.

Notas verificadas (lote 00: docs/lotes/20261110_fundamentos-y-spike/notas.md;
lote 01: docs/lotes/20261110_pleno-xv-navegable/notas.md):
- La página de opendata bloquea peticiones sin user-agent de navegador (403).
- La página ?targetDate=DD/MM/YYYY&targetLegislatura=XV lista los JSON de ese día.
- El índice (solo targetLegislatura) publica `var diasVotaciones = [20230919, …]`
  (enteros): todos los días con votaciones de la legislatura. Verificado el
  22/11/2026: XV = 147 días (19/09/2023 → 02/10/2026); XIV = 170.
- Los días con solo votaciones públicas por llamamiento no publican JSON por
  votación (sí un ZIP por sesión): la sesión 203 (02/10/2026) es el caso real.
- Diputados: congreso.es/es/opendata/diputados publica exportadores con marca
  temporal diaria (DiputadosActivos__AAAAMMDDHHMMSS.json, DiputadosDeBaja__…):
  «legislatura actual» al momento de la descarga. La XV (disuelta) aún era la
  actual el 22/11/2026: 137 activos + 275 de baja = 412.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

from ..modelo import Diputado, RegistroVotacion

BASE = "https://www.congreso.es"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

RE_JSON = re.compile(r"webpublica/opendata/votaciones/[^\"']+\.json")
RE_DIAS = re.compile(r"var\s+diasVotaciones\s*=\s*(\[[^\]]*\])")


def pagina_indice(legislatura: str = "XV") -> str:
    """HTML del índice de la legislatura (calendario completo, sin fecha)."""
    r = httpx.get(
        f"{BASE}/es/opendata/votaciones",
        params={"targetLegislatura": legislatura},
        headers={"User-Agent": UA},
        timeout=30,
        follow_redirects=True,
    )
    r.raise_for_status()
    return r.text


def dias_votaciones(legislatura: str = "XV") -> list[str]:
    """Fechas compactas (YYYYMMDD) de todos los días con votaciones de la legislatura."""
    m = RE_DIAS.search(pagina_indice(legislatura))
    if not m:
        raise ValueError("índice sin diasVotaciones: formato de la página cambiado")
    return sorted({f"{d:08d}" for d in json.loads(m.group(1))})


def sesion_y_fecha_de_url(url: str) -> tuple[int, str]:
    """Sesión y fecha compacta extraídas de la propia URL oficial:
    …/opendata/votaciones/Leg15/Sesion202/20260930/Votacion010/VOT_….json
    (así no hay que conocer la sesión antes de descargar el fichero).
    """
    partes = url.split("opendata/votaciones/")[-1].split("/")
    return int(partes[1].removeprefix("Sesion")), partes[2]


def pagina_votaciones(fecha_dma: str, legislatura: str = "XV") -> str:
    """HTML de la página de votaciones para una fecha (DD/MM/AAAA)."""
    url = f"{BASE}/es/opendata/votaciones"
    r = httpx.get(
        url,
        params={"targetDate": fecha_dma, "targetLegislatura": legislatura},
        headers={"User-Agent": UA},
        timeout=30,
        follow_redirects=True,
    )
    r.raise_for_status()
    return r.text


def urls_votaciones(fecha_dma: str, legislatura: str = "XV") -> list[str]:
    """URLs absolutas de los JSON de votación de esa fecha."""
    html = pagina_votaciones(fecha_dma, legislatura)
    return sorted({f"{BASE}/{m}" for m in RE_JSON.findall(html)})


def descargar(url: str, destino: Path) -> Path:
    """Descarga idempotente a data/raw (inmutable: si existe, no se re-descarga)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        r = httpx.get(url, headers={"User-Agent": UA}, timeout=30, follow_redirects=True)
        r.raise_for_status()
        destino.write_bytes(r.content)
    return destino


def ruta_cruda(raiz: Path, legislatura: str, sesion: int, fecha_compacta: str, url: str) -> Path:
    """data/raw/Leg15/Sesion202/20260930/Votacion010/VOT_....json (estructura del Congreso)."""
    partes = url.split("opendata/votaciones/")[-1].split("/")
    return raiz / "data" / "raw" / f"Leg{legislatura}" / f"Sesion{sesion}" / fecha_compacta / Path(*partes[-2:])


def cargar_registro(fichero: Path) -> RegistroVotacion:
    datos = json.loads(fichero.read_text(encoding="utf-8"))
    reg = RegistroVotacion.model_validate(datos)
    reg.fuente_url = url_desde_ruta(fichero)
    return reg


def url_desde_ruta(fichero: Path) -> str:
    """Reconstruye la URL oficial desde la ruta relativa en data/raw."""
    rel = Path(*fichero.parts[fichero.parts.index("raw") + 1 :]) if "raw" in fichero.parts else fichero
    return f"{BASE}/webpublica/opendata/votaciones/{rel.as_posix()}"


RE_DIPUTADOS = re.compile(r"webpublica/opendata/diputados/Diputados(?:Activos|DeBaja)__\d+\.json")


def urls_diputados() -> list[str]:
    """URLs de los exportadores de diputados de la legislatura actual (Activos + DeBaja).

    La página publica todos los exportadores con marca temporal diaria; la regex
    descarta los históricos por legislatura (odsDiputadosNN), el global (Diput__) y
    el de diputadas de todas las legislaturas (Diputadas__).
    """
    r = httpx.get(
        f"{BASE}/es/opendata/diputados",
        headers={"User-Agent": UA},
        timeout=30,
        follow_redirects=True,
    )
    r.raise_for_status()
    return sorted({f"{BASE}/{m}" for m in RE_DIPUTADOS.findall(r.text)})


def ruta_diputados(raiz: Path, legislatura: str, url: str) -> Path:
    """data/raw/LegXV/diputados/DiputadosActivos__AAAAMMDDHHMMSS.json (inmutable)."""
    return raiz / "data" / "raw" / f"Leg{legislatura}" / "diputados" / url.rsplit("/", 1)[-1]


def cargar_diputados(raiz: Path, legislatura: str) -> list[Diputado]:
    """Los diputados de la legislatura desde data/raw (activos + bajas), validados.

    De cada clase (Activos, DeBaja) toma el fichero con mayor marca temporal: los
    exportadores rotan a diario y data/raw es inmutable, así que puede haber más de
    uno. Falla con nombres duplicados (clave natural verificada única en la XV).
    """
    base = raiz / "data" / "raw" / f"Leg{legislatura}" / "diputados"
    diputados: list[Diputado] = []
    vistos: set[str] = set()
    for clase in ("DiputadosActivos__*", "DiputadosDeBaja__*"):
        ficheros = sorted(base.glob(clase))
        if not ficheros:
            raise ValueError(f"falta el exportador {clase} en {base}: ejecuta `make diputados`")
        for datos in json.loads(ficheros[-1].read_text(encoding="utf-8")):
            d = Diputado.model_validate({**datos, "legislatura": legislatura})
            if d.nombre in vistos:
                raise ValueError(f"diputado duplicado en la Leg{legislatura}: {d.nombre}")
            vistos.add(d.nombre)
            diputados.append(d)
    return diputados
