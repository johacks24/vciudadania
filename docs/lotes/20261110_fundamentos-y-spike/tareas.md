# Tareas — Lote 00

Marca `[x]` al completar. El agente trabaja de arriba abajo con `/siguiente`.

## Estado vivo

- **En exploración:** ninguna
- **En construcción:** ninguna. Lote 00 cerrado el 11/11/2026: cadena completa
  validada, ficha pública en `https://johacks24.github.io/vciudadania/` y apuesta a
  producción en `docs/apuestas.md`. Siguiente: moldear «Pleno XV navegable» (cooldown:
  revisar `docs/aprender.md` y `docs/apuestas.md`)

## Scope A — Auditoría de base

- [x] A.1 Evaluar CongresoAbierto, civis-api y Reforma Digital con el checklist fijo
      (licencia, actividad, cobertura XV, calidad, API, comunidad) — timebox 2 h por
      candidato → `informe-auditoria.md`
- [x] A.2 ADR-0005 «sobre qué construir» con el carril elegido

## Scope B — Esqueleto del repo

- [x] B.1 Licencias (AGPL-3.0 código + CC BY-SA contenidos), README, .gitignore,
      .env.example, Makefile, opencode.jsonc
- [x] B.2 AGENTS.md con regla 4x4, lecciones y reglas de fuentes
- [x] B.3 docs/: apuestas.md, aprender.md, diseno.md, metodo/metodo.md, decisiones
      0001–0004, referencias/ (indice + _privado gitignored)
- [x] B.4 Plantilla de lote aplicada (este lote: plan + tareas + notas) y comandos
      /siguiente y /referencia
- [x] B.5 CI mínima verde (tests) — *verde en el primer push (11/11/2026):
      https://github.com/johacks24/vciudadania/actions/runs/42938522655*
- [x] B.6 Credencial git propia (token fino del humano) — *hecha el 11/11: el llavero
      guarda ya el token fino (`git credential fill` → `username=johacks24`; la
      credencial del editor, `90719580`, borrada). Primera vuelta fallida por la
      inyección de GIT_ASKPASS (terminal del editor). Runbook corregido, caducidad del
      token (9/2/2027) y lección 4x4 nº 5: `notas.md` y `AGENTS.md`, 11/11*

## Scope C — Spike de datos (el corazón)

- [x] C.1 Modelo pydantic del registro de votación (información, totales, votos)
- [x] C.2 Cliente de fuente primaria: enumerar y descargar los JSON de la sesión 202
- [x] C.3 Validación: recuentos individuales == totales oficiales, votación por votación
      → **100 %: 20 nominales OK + 1 no nominal (suplicatorio secreto), 0 descuadres**
- [x] C.4 Exportación a SQLite (data/processed/congreso.sqlite)
- [x] C.5 Tests permanentes con fixture commiteado (CI sin red) → 4/4 pasan

## Scope D — Ficha web vertical

- [x] D.1 Generador de ficha (web/index.html) desde los datos validados: los 5 pasos del
      recorrido, sin colores de partido, con fuente enlazada
- [x] D.2 Despliegue público en GitHub Pages — *hecha el 11/11: Pages activada
      (Source: GitHub Actions), workflow «Paginas» creado y empujado, y despliegue
      verificado: `https://johacks24.github.io/vciudadania/` (HTTP 200) con las 21
      votaciones, los 5 pasos del recorrido y 21 enlaces de fuente. Workflows
      «Paginas» y CI en verde. La apuesta pasa a **producción** en `docs/apuestas.md`.
      Decisión y alternativas: `docs/decisiones/0006-despliegue.md`*
- [x] D.3 Enlace al repo en la ficha — *hecho el 11/11: el pie de la ficha enlaza el
      método en el repo real
      (`github.com/johacks24/vciudadania/blob/main/docs/metodo/metodo.md`, la opción
      mejor del brief). Corregido en el generador, regenerado con `make exportar`,
      validación 100 % (`make validar`) y tests 4/4 (`make test`)*

## Scope E — Cierre

- [x] E.1 docs/apuestas.md con la apuesta «Pleno XV navegable» en investigación
- [x] E.2 Commits limpios por scope (perfect commit: código + test + doc juntos)
