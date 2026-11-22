"""Portada de la legislatura (web/portada.html) e índice compacto (web/indice.json).

Decisión del lote (notas.md): la portada se genera en `portada.html` hasta que C.4
genere las fichas; entonces se promueve a index.html y sustituye a la ficha del
lote 00. Así la producción del lote 00 no se rompe a medias.

Mejora progresiva: los primeros `N_ESTATICOS` elementos van en el propio HTML (se
ven sin JavaScript) y el resto se carga al llegar al final de la página (scroll
infinito) desde `indice.json`. En el índice, el ORDEN del array es la cronología
(la más reciente primero): el cliente no ordena nada, solo recorre.

Búsqueda y filtro (C.2), todo en cliente sobre el índice ya cargado:
- por palabra, sobre el título Y el texto del expediente (medido el 23/11: «alquiler»
  no aparece en ningún título de la XV pero sí en 14 expedientes — la palabra oficial
  es «arrendamiento» —; «vivienda», en 71), normalizando acentos y mayúsculas
  («convalidacion» encuentra «Convalidación»), con antirrebote de 150 ms; el
  expediente es solo buscable: la lista siempre muestra el título;
- por resultado, con las categorías honestas de la ficha del lote 00 («Más Sí que
  No» / «Más No que Sí» / «Empate»), calculadas EN VIVO a partir de los recuentos:
  el índice no guarda ningún veredicto, porque «más Sí que No» no es «aprobada»
  cuando la mayoría exigida es cualificada (docs/diseno.md: números con contexto).

Los elementos muestran recuentos oficiales (Sí n · No n · Abst. n), no veredictos.
"""

from __future__ import annotations

import html
import json
import sqlite3
from pathlib import Path

N_ESTATICOS = 50  # primeros N elementos sin JavaScript (decisión del moldeo)
POR_LOTE = 50  # cuántos pinta el scroll infinito por tanda
ANTIRREBOTE = 150  # ms antes de filtrar al teclear

CSS = """
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 system-ui,sans-serif;color:#111;background:#fff}
main{max-width:720px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:22px;margin:0 0 4px}
.lead{color:#555;margin:0 0 16px;font-size:14px}
.busqueda{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 4px}
.busqueda label{font-size:12px;color:#555;display:block;margin:0 0 3px}
.busqueda input,.busqueda select{font:inherit;padding:8px 10px;border:1px solid #d1d5db;border-radius:8px;background:#fff;color:#111}
.busqueda .campo{flex:1 1 220px}
.busqueda .campo input{width:100%}
#contador{font-size:13px;color:#555;margin:8px 0 0}
.nota{font-size:12px;color:#555;margin:4px 0 14px}
#lista{list-style:none;margin:0;padding:0}
#lista li{border-bottom:1px solid #f0f0f0}
#lista a{display:block;padding:12px 2px;text-decoration:none;color:#111}
#lista .fecha{display:block;font-size:12px;color:#555}
#lista .titulo{display:block;font-size:15px;line-height:1.45;margin:2px 0}
#lista .recuento{display:block;font-size:13px;color:#555}
#centinela{padding:28px 0;color:#555;font-size:13px;text-align:center}
footer{margin-top:40px;font-size:13px;color:#555;border-top:1px solid #e5e7eb;padding-top:16px}
footer a{color:#2563eb}
"""

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>vCiudadania — Votaciones del Pleno ({legislatura})</title>
<style>{css}</style>
</head>
<body>
<main>
<h1>vCiudadania</h1>
<p class="lead">Legislatura {legislatura} · {n} votaciones del Pleno · recuentos validados
contra los totales oficiales. Se listan de la más reciente a la más antigua.</p>
<div class="busqueda">
  <div class="campo">
    <label for="q">Buscar por palabra</label>
    <input id="q" type="search" placeholder="p. ej., alquiler" autocomplete="off">
  </div>
  <div class="campo">
    <label for="filtro">Resultado</label>
    <select id="filtro">
      <option value="todos">Todos</option>
      <option value="si">Más Sí que No</option>
      <option value="no">Más No que Sí</option>
      <option value="empate">Empate</option>
    </select>
  </div>
</div>
<p id="contador" aria-live="polite">{n} votaciones</p>
<p class="nota">La búsqueda necesita JavaScript. El filtro compara recuentos: no dice
si la iniciativa quedó aprobada, porque algunas mayorías son cualificadas.</p>
<ol id="lista">
{items}
</ol>
<p id="centinela">Cargando más votaciones…</p>
<script>
(function () {{
  var ESTATICOS = {n_estaticos}, LOTE = {por_lote}, PAUSA = {antirrebote};
  var lista = document.getElementById('lista');
  var centinela = document.getElementById('centinela');
  var contador = document.getElementById('contador');
  var q = document.getElementById('q');
  var filtro = document.getElementById('filtro');
  var todos = null, vista = [], i = 0, obs = null, temporizador = null;
  function normaliza(s) {{
    return (s || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
  }}
  function categoria(v) {{
    return v.si > v.no ? 'si' : (v.no > v.si ? 'no' : 'empate');
  }}
  function calculaVista() {{
    var texto = normaliza(q.value).trim(), cat = filtro.value;
    vista = todos.filter(function (v) {{
      if (cat !== 'todos' && categoria(v) !== cat) return false;
      return !texto || normaliza(v.titulo + ' ' + v.expediente).indexOf(texto) !== -1;
    }});
  }}
  function resumen() {{
    var total = vista.length, texto = q.value.trim();
    if (!texto && filtro.value === 'todos') return total + ' votaciones';
    var r = total + (total === 1 ? ' resultado' : ' resultados');
    if (texto) r += ' para «' + texto + '»';
    if (filtro.value !== 'todos') r += ' · ' + filtro.options[filtro.selectedIndex].text;
    return r;
  }}
  function pinta(v) {{
    var li = document.createElement('li'), a = document.createElement('a');
    a.href = v.ficha;
    ['fecha', 'titulo', 'recuento'].forEach(function (clase) {{
      var s = document.createElement('span');
      s.className = clase;
      s.textContent = clase === 'fecha' ? v.fecha
        : clase === 'titulo' ? v.titulo
        : v.si + ' Sí · ' + v.no + ' No · ' + v.abst + ' Abst.' +
          (v.sin_individual ? ' · votación no nominal (solo totales)' : '');
      a.appendChild(s);
    }});
    li.appendChild(a);
    lista.appendChild(li);
  }}
  function carga() {{
    if (!todos) return;
    var fin = Math.min(i + LOTE, vista.length);
    for (; i < fin; i++) pinta(vista[i]);
    contador.textContent = resumen();
    if (i >= vista.length) {{
      centinela.textContent = vista.length ? 'Fin: ' + resumen() + '.' : 'Sin resultados para esa búsqueda.';
      if (obs) obs.disconnect();
    }}
  }}
  function reinicia() {{
    if (!todos) return;
    lista.textContent = '';
    i = 0;
    calculaVista();
    if (obs) {{ obs.disconnect(); obs.observe(centinela); }}
    carga();
  }}
  q.addEventListener('input', function () {{
    clearTimeout(temporizador);
    temporizador = setTimeout(reinicia, PAUSA);
  }});
  filtro.addEventListener('change', reinicia);
  fetch('indice.json').then(function (r) {{ return r.json(); }}).then(function (j) {{
    todos = j.votaciones;
    calculaVista();
    i = ESTATICOS;
    contador.textContent = resumen();
    if (i >= vista.length) {{ carga(); return; }}
    if ('IntersectionObserver' in window) {{
      obs = new IntersectionObserver(function (entradas) {{
        if (entradas.some(function (e) {{ return e.isIntersecting; }})) carga();
      }}, {{rootMargin: '600px'}});
      obs.observe(centinela);
    }} else {{
      centinela.textContent = 'Mostrar más';
      centinela.addEventListener('click', carga);
    }}
  }}).catch(function () {{
    centinela.textContent = 'No se pudo cargar el índice (¿sin conexión al servidor?).';
  }});
}})();
</script>
<footer>
<p>Fuente: vCiudadania (vciudadania), a partir de los <a href="https://www.congreso.es/es/opendata">datos abiertos
del Congreso de los Diputados</a>. Cada votación enlaza su registro oficial. La valoración es tuya:
no recomendamos el voto. Método y límites: <a href="https://github.com/johacks24/vciudadania/blob/main/docs/metodo/metodo.md">docs/metodo/metodo.md</a>.</p>
</footer>
</main>
</body>
</html>"""


def _orden_fecha(fecha: str) -> int:
    """'30/9/2026' → 20260930. La fecha de la fuente (D/M/YYYY) no es ordenable como texto."""
    d, m, a = fecha.split("/")
    return int(f"{a}{int(m):02d}{int(d):02d}")


def votaciones_recientes(bd: Path, legislatura: str) -> list[dict]:
    """Todas las votaciones de la legislatura, de la más reciente a la más antigua."""
    con = sqlite3.connect(bd)
    con.row_factory = sqlite3.Row
    filas = con.execute(
        "SELECT id, sesion, numero, fecha, titulo, texto_expediente, afavor, en_contra,"
        " abstenciones, no_votan, sin_voto_individual FROM votaciones WHERE legislatura = ?",
        (legislatura,),
    ).fetchall()
    con.close()
    vots = [
        {
            "id": f["id"], "sesion": f["sesion"], "numero": f["numero"], "fecha": f["fecha"],
            "titulo": f["titulo"], "expediente": f["texto_expediente"],
            "si": f["afavor"], "no": f["en_contra"],
            "abst": f["abstenciones"], "novota": f["no_votan"],
            "sin_individual": bool(f["sin_voto_individual"]),
            "ficha": f"votacion/{f['id']}.html",
        }
        for f in filas
    ]
    vots.sort(key=lambda v: (-_orden_fecha(v["fecha"]), -v["sesion"], -v["numero"]))
    return vots


def generar_indice(vots: list[dict], destino: Path, legislatura: str) -> Path:
    """Escribe web/indice.json (el contrato: el orden del array ES la cronología)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps({"legislatura": legislatura, "votaciones": vots}, ensure_ascii=False),
        encoding="utf-8",
    )
    return destino


def _item(v: dict) -> str:
    titulo = html.escape(v["titulo"])
    recuento = f'{v["si"]} Sí · {v["no"]} No · {v["abst"]} Abst.'
    if v["sin_individual"]:
        recuento += " · votación no nominal (solo totales)"
    return (
        f'<li><a href="{html.escape(v["ficha"])}">'
        f'<span class="fecha">{html.escape(v["fecha"])}</span>'
        f'<span class="titulo">{titulo}</span>'
        f'<span class="recuento">{recuento}</span>'
        "</a></li>"
    )


def generar_portada(vots: list[dict], destino: Path, legislatura: str) -> Path:
    """Escribe web/portada.html: los primeros N_ESTATICOS van en el HTML (sin JavaScript)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        PLANTILLA.format(
            css=CSS,
            legislatura=legislatura,
            n=len(vots),
            n_estaticos=min(N_ESTATICOS, len(vots)),
            por_lote=POR_LOTE,
            antirrebote=ANTIRREBOTE,
            items="\n".join(_item(v) for v in vots[:N_ESTATICOS]),
        ),
        encoding="utf-8",
    )
    return destino
