"""Cliente de la fuente primaria: datos abiertos del Congreso de los Diputados.

Notas verificadas (docs/lotes/20261110_fundamentos-y-spike/notas.md):
- La página de opendata bloquea peticiones sin user-agent de navegador (403).
- La página ?targetDate=DD/MM/YYYY&targetLegislatura=XV lista los JSON de la sesión.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

from ..modelo import RegistroVotacion

BASE = "https://www.congreso.es"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

RE_JSON = re.compile(r"webpublica/opendata/votaciones/[^\"']+\.json")


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
