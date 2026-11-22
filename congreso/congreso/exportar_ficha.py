"""Generador de fichas web por votación (web/votacion/<id>.html) desde la base.

Escalado del lote 00 (recorrido 3: qué se votó → recuento → voto por grupo → fuente
oficial) con el recuento visual (waffle) decidido en la ADR-0007 y las reglas
operativas de docs/diseno.md:

- una celda por diputado con voto nominal; relleno = color del grupo (paleta
  ADR-0007, contraste ≥ 3:1 sobre blanco);
- el sentido del voto se lee por POSICIÓN (secciones Sí / No / Abstención / No vota,
  con su número en la cabecera): el color de la celda nunca codifica el voto;
- dentro de cada sección, bloques por grupo en orden fijo (nº de diputados del grupo
  en esa votación, descendente; Mixto al final), con separación visible;
- sin texto en las celdas: la sigla vive en la leyenda (chip + sigla + nombre) y el
  detalle por diputado aparece a demanda (`<title>` del rectángulo);
- SVG estático, sin JavaScript, y la tabla «voto por grupo» de debajo conserva todo
  el dato en texto (color redundante, nunca único);
- votaciones sin voto individual publicado (suplicatorios, llamamiento): sin waffle,
  solo totales con su nota (categoría, no error).

Como en el lote 00, los recuentos no se traducen a veredictos: «Más Sí que No» no
es «aprobada» cuando la mayoría exigida es cualificada.
"""

from __future__ import annotations

import html
import shutil
import sqlite3
from pathlib import Path

# Paleta y nombres oficiales (ADR-0007; contrastados con el exportador de diputados)
GRUPOS: dict[str, tuple[str, str, str]] = {
    "GP": ("PP", "Grupo Parlamentario Popular en el Congreso", "#1d84ce"),
    "GS": ("PSOE", "Grupo Parlamentario Socialista", "#e30613"),
    "GVOX": ("Vox", "Grupo Parlamentario VOX", "#4fa82e"),
    "GSUMAR": ("Sumar", "Grupo Parlamentario Plurinacional SUMAR", "#e51c55"),
    "GR": ("ERC", "Grupo Parlamentario Republicano", "#d08200"),
    "GJxCAT": ("Junts", "Grupo Parlamentario Junts per Catalunya", "#00a496"),
    "GEH Bildu": ("EH Bildu", "Grupo Parlamentario Euskal Herria Bildu", "#849c13"),
    "GV (EAJ-PNV)": ("PNV", "Grupo Parlamentario Vasco (EAJ-PNV)", "#2e7d32"),
    "GMx": ("Mixto", "Grupo Parlamentario Mixto", "#949494"),
}
NEUTRO = "#555555"  # grupo no catalogado (defensivo: no debería ocurrir en la XV)

SENTIDOS: list[tuple[str, str]] = [
    ("Sí", "#16a34a"), ("No", "#dc2626"), ("Abstención", "#9ca3af"), ("No vota", "#d1d5db"),
]

CELDA, HUECO, HUECO_GRUPO, ANCHO = 12, 2, 6, 336  # 24 columnas a 375 px

CSS = """
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 system-ui,sans-serif;color:#111;background:#fff}
main{max-width:720px;margin:0 auto;padding:24px 16px 64px}
.volver{font-size:14px;margin:0 0 12px}
.volver a{color:#2563eb;text-decoration:none}
h1{font-size:20px;line-height:1.35;margin:0 0 4px}
h2{font-size:16px;margin:24px 0 8px;color:#555;font-weight:600}
.lead{color:#555;margin:0 0 16px;font-size:14px}
.temas{font-size:13px;color:#555;margin:0 0 14px}
.temas b{color:#111;font-weight:600}
.pregunta{margin:0 0 8px}
.nums{font-size:14px;color:#555;margin:4px 0 12px}
.nums b{color:#111}
svg{display:block;margin:8px 0 4px;max-width:336px}
.leyenda{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;color:#555;margin:4px 0 8px}
.leyenda span{white-space:nowrap}
.leyenda i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:baseline}
.sin-individuales{font-size:13px;color:#555;background:#f9fafb;border-radius:8px;padding:8px 10px;margin:8px 0}
table{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0}
th,td{text-align:right;padding:4px 8px;border-bottom:1px solid #f0f0f0}
th:first-child,td:first-child{text-align:left}
.fuente{font-size:13px;margin-top:10px}
.fuente a{color:#2563eb}
footer{margin-top:40px;font-size:13px;color:#555;border-top:1px solid #e5e7eb;padding-top:16px}
footer a{color:#2563eb}
"""

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} — vCiudadania</title>
<style>{css}</style>
</head>
<body>
<main>
<p class="volver"><a href="../">← Todas las votaciones</a></p>
<h1>{titulo}</h1>
<p class="lead">Sesión {sesion} del Pleno · {fecha} · votación nº {numero} · Legislatura {legislatura}
· recuento validado contra los totales oficiales</p>
{temas}
<p class="pregunta">{pregunta}</p>
<h2>Recuento</h2>
<p class="nums"><b>{si}</b> Sí · <b>{no}</b> No · <b>{abst}</b> Abstención · <b>{novota}</b> No vota ·
{presentes} presentes — {sentencia} El acuerdo oficial es el del Diario de Sesiones.</p>
{waffle}
{leyenda}
<h2>Voto por grupo</h2>
{tabla}
<p class="fuente">Fuente oficial: <a href="{fuente}">registro de la votación (opendata del Congreso)</a></p>
<footer>
<p>Fuente: vCiudadania (vciudadania), a partir de los <a href="https://www.congreso.es/es/opendata">datos abiertos
del Congreso de los Diputados</a>. La valoración es tuya: no recomendamos el voto.
Método y límites: <a href="https://github.com/johacks24/vciudadania/blob/main/docs/metodo/metodo.md">docs/metodo/metodo.md</a>.</p>
{pie_temas}
</footer>
</main>
</body>
</html>"""


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _color(grupo: str) -> str:
    return GRUPOS.get(grupo, ("", "", NEUTRO))[2]


def _orden_grupos(votos: list[dict]) -> list[str]:
    """Orden fijo de la votación: nº de diputados del grupo, descendente; Mixto al final."""
    emitidos: dict[str, int] = {}
    for v in votos:
        emitidos[v["grupo"]] = emitidos.get(v["grupo"], 0) + 1
    return sorted(emitidos, key=lambda g: (g == "GMx", -emitidos[g], g))


def _waffle(votos: list[dict]) -> str:
    """El pleno en una cuadrícula: celda por diputado, color de grupo, voto por posición."""
    orden = _orden_grupos(votos)
    partes: list[str] = []
    y = 0
    for etiqueta, color in SENTIDOS:
        partes.append(
            f'<text x="0" y="{y + 11}" fill="{color}" font-family="system-ui" '
            f'font-size="11" font-weight="600">{_esc(etiqueta)} {sum(1 for v in votos if v["voto"] == etiqueta)}</text>'
        )
        y += 18
        celdas = 0
        x = 0
        for g in orden:
            bloque = [v for v in votos if v["grupo"] == g and v["voto"] == etiqueta]
            for v in bloque:
                if x + CELDA > ANCHO:
                    x = 0
                    y += CELDA + HUECO
                detalle = f'{v["diputado"]} ({g}): {v["voto"]}'
                partes.append(
                    f'<rect x="{x}" y="{y}" width="{CELDA}" height="{CELDA}" '
                    f'fill="{_color(g)}"><title>{_esc(detalle)}</title></rect>'
                )
                celdas += 1
                x += CELDA + HUECO
            if bloque:
                x += HUECO_GRUPO  # separación visible entre bloques de grupo
        y += CELDA + 14 if celdas else 4
    return (
        f'<svg viewBox="0 0 {ANCHO} {y}" width="100%" role="img" '
        'aria-label="El pleno en una cuadrícula: una celda por diputado con el color de su '
        'grupo, ordenadas por secciones según el sentido del voto">'
        + "".join(partes)
        + "</svg>"
    )


def _leyenda(orden: list[str]) -> str:
    chips = "".join(
        f'<span><i style="background:{_color(g)}"></i>{sigla} — {_esc(nombre)}</span>'
        for g in orden
        for sigla, nombre, _ in [GRUPOS.get(g, (g, g, NEUTRO))]
    )
    return f'<p class="leyenda">{chips}</p>' if chips else ""


def _tabla_grupos(votos: list[dict]) -> str:
    orden = _orden_grupos(votos)
    filas = []
    for g in orden:
        n = {s: 0 for s, _ in SENTIDOS}
        for v in votos:
            if v["grupo"] == g:
                n[v["voto"]] = n.get(v["voto"], 0) + 1
        filas.append(
            f"<tr><td>{_esc(g)}</td><td>{n.get('Sí', 0)}</td><td>{n.get('No', 0)}</td>"
            f"<td>{n.get('Abstención', 0)}</td><td>{n.get('No vota', 0)}</td></tr>"
        )
    return (
        "<table><tr><th>Grupo</th><th>Sí</th><th>No</th><th>Abst.</th><th>No vota</th></tr>"
        + "".join(filas)
        + "</table>"
    )


def _sentencia(si: int, no: int) -> str:
    if si > no:
        return "Más Sí que No."
    if no > si:
        return "Más No que Sí."
    return "Empate entre Sí y No."


def generar_ficha(fila, votos: list[dict], temas: list[str], destino: Path, legislatura: str) -> Path:
    """Escribe la ficha de una votación (fila de la tabla `votaciones` + sus votos)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    titulo = html.escape(fila["titulo"])
    pregunta = html.escape(fila["texto_expediente"])
    sin_individual = bool(fila["sin_voto_individual"])
    si, no = fila["afavor"], fila["en_contra"]
    if sin_individual:
        waffle = (
            '<p class="sin-individuales">Votación no nominal (secreta o por asentimiento): '
            "solo se publican los totales oficiales.</p>"
        )
        leyenda, tabla = "", "<p class=\"sin-individuales\">Sin voto por grupo: no hay voto individual publicado.</p>"
    else:
        waffle = _waffle(votos)
        leyenda = _leyenda(_orden_grupos(votos))
        tabla = _tabla_grupos(votos)
    if temas:
        pie_temas = (
            "<p>Clasificación por temas: Congreso Abierto (congresoabierto.org), "
            "a partir de datos oficiales del Congreso de los Diputados · CC BY 4.0.</p>"
        )
        temas_linea = f'<p class="temas">Tema: <b>{_esc(", ".join(sorted(temas)))}</b></p>'
    else:
        pie_temas, temas_linea = "", ""
    destino.write_text(
        PLANTILLA.format(
            css=CSS,
            titulo=titulo,
            sesion=fila["sesion"],
            fecha=html.escape(fila["fecha"]),
            numero=fila["numero"],
            legislatura=legislatura,
            temas=temas_linea,
            pregunta=pregunta,
            si=si, no=no, abst=fila["abstenciones"], novota=fila["no_votan"],
            presentes=fila["presentes"],
            sentencia=_sentencia(si, no),
            waffle=waffle,
            leyenda=leyenda,
            tabla=tabla,
            fuente=html.escape(fila["fuente_url"]),
            pie_temas=pie_temas,
        ),
        encoding="utf-8",
    )
    return destino


def generar_fichas(bd: Path, destino_dir: Path, legislatura: str) -> int:
    """Escribe TODAS las fichas de la legislatura (regeneración completa del directorio)."""
    con = sqlite3.connect(bd)
    con.row_factory = sqlite3.Row
    votaciones = con.execute(
        "SELECT * FROM votaciones WHERE legislatura = ? ORDER BY id", (legislatura,)
    ).fetchall()
    votos: dict[str, list[dict]] = {}
    for vid, asiento, diputado, grupo, voto in con.execute(
        "SELECT votacion_id, asiento, diputado, grupo, voto FROM votos"
    ):
        votos.setdefault(vid, []).append(
            {"asiento": asiento, "diputado": diputado, "grupo": grupo, "voto": voto}
        )
    temas: dict[str, list[str]] = {}
    for vid, tema in con.execute("SELECT votacion_id, tema FROM temas_votacion"):
        temas.setdefault(vid, []).append(tema)
    con.close()
    if destino_dir.exists():
        shutil.rmtree(destino_dir)  # regeneración completa: sin fichas huérfanas
    destino_dir.mkdir(parents=True)
    for fila in votaciones:
        generar_ficha(
            fila, votos.get(fila["id"], []), temas.get(fila["id"], []),
            destino_dir / f"{fila['id']}.html", legislatura,
        )
    return len(votaciones)
