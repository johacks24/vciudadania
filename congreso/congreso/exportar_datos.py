"""Dataset descargable de la legislatura (web/datos/): JSON + CSV con su cita.

Recorrido 4: «Descargo el dataset completo con su cita». El dataset es el de las
**votaciones** (una por fila: qué se votó, totales oficiales, temas y enlace a su
registro oficial); el de votos individuales por diputado es territorio de la
apuesta «API pública v1», no de este lote.

Decisiones (docs/lotes/20261110_pleno-xv-navegable/notas.md):
- el JSON es autodescriptivo: legislatura, cita, licencias y fuente van DENTRO;
- cada fila del CSV lleva el enlace a su registro oficial: el dato se cita a sí
  mismo (regla de trazabilidad del proyecto);
- sin fecha de generación: la XV es un corpus cerrado y los artefactos son
  deterministas — regenerar no cambia nada; el versionado es el del repositorio.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

CITA_NUESTRA = "vCiudadania (vciudadania), a partir de los datos abiertos del Congreso de los Diputados"
LICENCIA = (
    "Contenidos elaborados: CC BY-SA 4.0 · Temas: Congreso Abierto "
    "(congresoabierto.org), a partir de datos oficiales del Congreso de los Diputados · CC BY 4.0"
)

COLUMNAS = [
    "id", "fecha", "sesion", "numero", "titulo", "expediente", "temas",
    "si", "no", "abst", "novota", "voto_individual", "fuente",
]


def generar_datos(vots: list[dict], destino_dir: Path, legislatura: str) -> tuple[Path, Path]:
    """Escribe web/datos/votaciones.json y votaciones.csv. Devuelve (json, csv)."""
    destino_dir.mkdir(parents=True, exist_ok=True)
    json_path = destino_dir / "votaciones.json"
    csv_path = destino_dir / "votaciones.csv"
    json_path.write_text(
        json.dumps(
            {
                "legislatura": legislatura,
                "n": len(vots),
                "cita": CITA_NUESTRA,
                "licencia": LICENCIA,
                "fuente": "https://www.congreso.es/es/opendata",
                "votaciones": vots,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLUMNAS)
        for v in vots:
            w.writerow(
                [
                    v["id"], v["fecha"], v["sesion"], v["numero"], v["titulo"],
                    v["expediente"], " | ".join(v["temas"]),
                    v["si"], v["no"], v["abst"], v["novota"],
                    "no" if v["sin_individual"] else "si",
                    v["fuente"],
                ]
            )
    return json_path, csv_path
