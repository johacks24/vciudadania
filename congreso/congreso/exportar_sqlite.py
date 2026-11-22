"""Exportación a SQLite (data/processed/congreso.sqlite)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .modelo import Diputado, RegistroVotacion

ESQUEMA = """
CREATE TABLE IF NOT EXISTS votaciones (
  id TEXT PRIMARY KEY,
  legislatura TEXT NOT NULL,
  sesion INTEGER NOT NULL,
  numero INTEGER NOT NULL,
  fecha TEXT NOT NULL,
  titulo TEXT NOT NULL,
  texto_expediente TEXT NOT NULL,
  asentimiento TEXT NOT NULL,
  presentes INTEGER NOT NULL,
  afavor INTEGER NOT NULL,
  en_contra INTEGER NOT NULL,
  abstenciones INTEGER NOT NULL,
  no_votan INTEGER NOT NULL,
  sin_voto_individual INTEGER NOT NULL,
  fuente_url TEXT NOT NULL,
  validada INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS votos (
  votacion_id TEXT NOT NULL REFERENCES votaciones(id),
  asiento TEXT NOT NULL,
  diputado TEXT NOT NULL,
  grupo TEXT NOT NULL,
  voto TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resumen_grupos (
  votacion_id TEXT NOT NULL REFERENCES votaciones(id),
  grupo TEXT NOT NULL,
  si INTEGER NOT NULL, no INTEGER NOT NULL,
  abstencion INTEGER NOT NULL, no_vota INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS diputados (
  legislatura TEXT NOT NULL,
  nombre TEXT NOT NULL,
  circunscripcion TEXT NOT NULL,
  formacion TEXT NOT NULL,
  grupo TEXT NOT NULL,
  fecha_alta TEXT NOT NULL,
  fecha_condicion_plena TEXT NOT NULL,
  fecha_alta_grupo TEXT NOT NULL,
  fecha_baja TEXT NOT NULL,
  fecha_baja_grupo TEXT NOT NULL,
  biografia TEXT NOT NULL,
  PRIMARY KEY (legislatura, nombre)
);
CREATE TABLE IF NOT EXISTS temas_votacion (
  votacion_id TEXT NOT NULL REFERENCES votaciones(id),
  tema TEXT NOT NULL,
  PRIMARY KEY (votacion_id, tema)
);
CREATE INDEX IF NOT EXISTS idx_votos_votacion ON votos(votacion_id);
CREATE INDEX IF NOT EXISTS idx_votaciones_fecha ON votaciones(fecha);
CREATE INDEX IF NOT EXISTS idx_diputados_grupo ON diputados(grupo);
CREATE INDEX IF NOT EXISTS idx_temas_tema ON temas_votacion(tema);
"""


def exportar(ficheros: list[Path], destino: Path, legislatura: str) -> list[tuple[str, bool]]:
    """Escribe la BD. Devuelve [(id, validada_ok)] para el informe.

    Reconstrucción limpia: borra votaciones/votos/resumen_grupos antes de escribir,
    para que la base siempre refleje exactamente el alcance exportado (una sesión o
    toda la legislatura), sin restos de exportaciones anteriores.
    """
    destino.parent.mkdir(parents=True, exist_ok=True)
    bd = sqlite3.connect(destino)
    bd.executescript(ESQUEMA)
    bd.execute("DELETE FROM votos")
    bd.execute("DELETE FROM resumen_grupos")
    bd.execute("DELETE FROM votaciones")
    informe: list[tuple[str, bool]] = []
    for f in ficheros:
        from .fuentes.congreso_es import cargar_registro

        reg = cargar_registro(f)
        ok = not reg.validar()
        t, i = reg.totales, reg.informacion
        bd.execute(
            "INSERT OR REPLACE INTO votaciones VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                reg.id, legislatura, i.sesion, i.numero_votacion, i.fecha, i.titulo,
                i.texto_expediente, t.asentimiento, t.presentes, t.afavor, t.en_contra,
                t.abstenciones, t.no_votan, int(reg.sin_voto_individual), reg.fuente_url, int(ok),
            ),
        )
        for v in reg.votaciones:
            bd.execute(
                "INSERT INTO votos VALUES (?,?,?,?,?)",
                (reg.id, v.asiento, v.diputado, v.grupo, v.voto),
            )
        for g in reg.resumen_por_grupo():
            bd.execute(
                "INSERT INTO resumen_grupos VALUES (?,?,?,?,?,?)",
                (reg.id, g["grupo"], g["Sí"], g["No"], g["Abstención"], g["No vota"] + g["otro"]),
            )
        informe.append((reg.id, ok))
    bd.commit()
    bd.close()
    return informe


def exportar_diputados(diputados: list[Diputado], destino: Path, legislatura: str) -> int:
    """Escribe la tabla diputados de esa legislatura (idempotente: solo la suya)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    bd = sqlite3.connect(destino)
    bd.executescript(ESQUEMA)
    bd.execute("DELETE FROM diputados WHERE legislatura = ?", (legislatura,))
    bd.executemany(
        "INSERT INTO diputados VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (
            (
                d.legislatura, d.nombre, d.circunscripcion, d.formacion, d.grupo,
                d.fecha_alta, d.fecha_condicion_plena, d.fecha_alta_grupo,
                d.fecha_baja, d.fecha_baja_grupo, d.biografia,
            )
            for d in diputados
        ),
    )
    bd.commit()
    bd.close()
    return len(diputados)


def exportar_temas(pares: list[tuple[str, str]], destino: Path) -> int:
    """Escribe temas_votacion (pares (id de votación, tema)): reconstrucción completa.

    Fuente secundaria con atribución (ADR-0005.3): la asignación de temas es de
    CongresoAbierto (CC BY 4.0); el cruce contra nuestras votaciones se hace en el
    CLI antes de llegar aquí.
    """
    destino.parent.mkdir(parents=True, exist_ok=True)
    bd = sqlite3.connect(destino)
    bd.executescript(ESQUEMA)
    bd.execute("DELETE FROM temas_votacion")
    bd.executemany("INSERT OR IGNORE INTO temas_votacion VALUES (?,?)", pares)
    bd.commit()
    bd.close()
    return len(pares)
