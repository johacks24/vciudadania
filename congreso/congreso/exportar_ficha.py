"""Generador de la ficha web (web/index.html) desde datos validados.

Cumple el recorrido de 5 pasos del lote 00: qué se votó → resultado y recuento →
voto por grupo → fuente oficial. Sin colores de partido (docs/diseno.md).
No editar web/index.html a mano: se regenera con `make exportar`.
"""

from __future__ import annotations

import html
from pathlib import Path

from .fuentes.congreso_es import cargar_registro
from .modelo import RegistroVotacion

CSS = """
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 system-ui,sans-serif;color:#111;background:#fff}
main{max-width:720px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:22px;margin:0 0 4px}
h2{font-size:16px;margin:24px 0 8px;color:#555;font-weight:600}
.lead{color:#555;margin:0 0 20px;font-size:14px}
.card{border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:16px 0}
.card h3{margin:0 0 2px;font-size:17px}
.tipo{color:#555;font-size:13px;margin:0 0 10px}
.barras{display:flex;height:14px;border-radius:7px;overflow:hidden;background:#d1d5db;margin:8px 0}
.barras span{display:block;height:100%}
.s{background:#16a34a}.n{background:#dc2626}.a{background:#9ca3af}
.nums{font-size:14px;color:#555;margin:4px 0 10px}
.nums b{color:#111}
table{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0}
th,td{text-align:right;padding:4px 8px;border-bottom:1px solid #f0f0f0}
th:first-child,td:first-child{text-align:left}
.sin-individuales{font-size:13px;color:#555;background:#f9fafb;border-radius:8px;padding:8px 10px;margin-top:8px}
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
<title>vCiudadania — Votaciones del Pleno</title>
<style>{css}</style>
</head>
<body>
<main>
<h1>vCiudadania</h1>
<p class="lead">Sesión {sesion} del Pleno · {fecha_legible} · Legislatura {legislatura}
· {n} votaciones · recuentos validados contra los totales oficiales</p>
{tarjetas}
<footer>
<p>Fuente: vCiudadania (vciudadania), a partir de los <a href="https://www.congreso.es/es/opendata">datos abiertos
del Congreso de los Diputados</a>. Cada votación enlaza su registro oficial. La valoración es tuya:
no recomendamos el voto. Método y límites: <a href="https://github.com/johacks24/vciudadania/blob/main/docs/metodo/metodo.md">docs/metodo/metodo.md</a>.</p>
</footer>
</main>
</body>
</html>"""


def _barra(r: RegistroVotacion) -> str:
    t = r.totales
    total = max(t.afavor + t.en_contra + t.abstenciones + t.no_votan, 1)
    return (
        '<div class="barras">'
        f'<span class="s" style="width:{t.afavor / total * 100:.1f}%"></span>'
        f'<span class="n" style="width:{t.en_contra / total * 100:.1f}%"></span>'
        f'<span class="a" style="width:{t.abstenciones / total * 100:.1f}%"></span>'
        "</div>"
    )


def _resultado(t) -> str:
    if t.afavor > t.en_contra:
        return "Más Sí que No."
    if t.en_contra > t.afavor:
        return "Más No que Sí."
    return "Empate entre Sí y No."


def _tarjeta(r: RegistroVotacion) -> str:
    t, i = r.totales, r.informacion
    titulo = html.escape(i.titulo)
    pregunta = html.escape(i.texto_expediente)
    if i.titulo_subgrupo:
        pregunta = f"<b>{html.escape(i.titulo_subgrupo)}.</b> {pregunta}"
    filas = ""
    if not r.sin_voto_individual:
        filas = (
            "<table><tr><th>Grupo</th><th>Sí</th><th>No</th><th>Abst.</th><th>No vota</th></tr>"
            + "".join(
                f"<tr><td>{html.escape(g['grupo'])}</td><td>{g['Sí']}</td><td>{g['No']}</td>"
                f"<td>{g['Abstención']}</td><td>{g['No vota'] + g['otro']}</td></tr>"
                for g in r.resumen_por_grupo()
            )
            + "</table>"
        )
    nota_secreto = (
        '<p class="sin-individuales">Votación no nominal (secreta o por asentimiento): '
        "solo se publican los totales oficiales.</p>"
        if r.sin_voto_individual
        else ""
    )
    fuente = (
        f'<p class="fuente">Fuente oficial: <a href="{html.escape(r.fuente_url)}">'
        "registro de la votación (opendata del Congreso)</a></p>"
        if r.fuente_url
        else ""
    )
    return (
        '<section class="card">'
        f"<h3>{titulo}</h3>"
        f'<p class="tipo">{html.escape(i.fecha)} · votación nº {i.numero_votacion}</p>'
        f"<p>{pregunta}</p>"
        + _barra(r)
        + f'<p class="nums"><b>{t.afavor}</b> Sí · <b>{t.en_contra}</b> No · '
        f"<b>{t.abstenciones}</b> Abstención · <b>{t.no_votan}</b> No vota · "
        f"{t.presentes} presentes — {_resultado(t)} Recuento de este trámite; el acuerdo "
        "oficial es el del Diario de Sesiones.</p>"
        + filas
        + nota_secreto
        + fuente
        + "</section>"
    )


def generar(ficheros: list[Path], destino: Path, legislatura: str) -> Path:
    regs = [cargar_registro(f) for f in ficheros]
    regs.sort(key=lambda r: r.informacion.numero_votacion)
    primera = regs[0].informacion if regs else None
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        PLANTILLA.format(
            css=CSS,
            sesion=primera.sesion if primera else "?",
            fecha_legible=primera.fecha if primera else "?",
            legislatura=legislatura,
            n=len(regs),
            tarjetas="\n".join(_tarjeta(r) for r in regs),
        ),
        encoding="utf-8",
    )
    return destino
