# Tareas — Lote 00

Marca `[x]` al completar. El agente trabaja de arriba abajo con `/siguiente`.

## Estado vivo

- **En exploración:** ninguna
- **En construcción:** B.6 · D.2 · D.3 — programadas para el **12/11/2026**. Orden del
  día: B.6 antes del primer push (la credencial nueva debe quedar en el llavero), D.3
  antes del push final de D.2 (la ficha sube ya corregida). Desbloqueos y hallazgos del
  11/11: `notas.md`

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
- [ ] B.6 Credencial git propia (token fino del humano) — *migrar del token OAuth
      general del editor al token fino (fine-grained) ya creado (permiso de código RW):
      reject + push desde un Terminal normal (usuario `johacks24`, el token como
      contraseña) y verificar con `git credential fill` (username=johacks24, ya no
      `90719580`). Runbook y cadena completa: `notas.md` 11/11 — día 12/11*

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
- [ ] D.2 Despliegue público en GitHub Pages — *bloqueo resuelto el 11/11 (repo público:
      `github.com/johacks24/vciudadania`). Día 12/11: (1) Settings → Pages → Source:
      GitHub Actions (se activa antes del primer despliegue); (2) crear
      `.github/workflows/paginas.yml` que publique `web/` (checkout → configure-pages →
      upload-pages-artifact con `path: web` → deploy-pages; disparo: push a main que
      toque `web/**` + manual); (3) push y verificar: workflow «Paginas» en verde y URL
      `https://johacks24.github.io/vciudadania/` con los 5 pasos del recorrido; (4)
      cerrar: apuesta a **producción** en `docs/apuestas.md`. Decisión y alternativas:
      `docs/decisiones/0006-despliegue.md`. Ejecutar D.3 antes del push final*
- [ ] D.3 Enlace al repo en la ficha — *la ficha generada enlaza
      `github.com/vciudadania` (no existe). Corregir en el generador
      (`congreso/congreso/exportar_ficha.py`, ~línea 59) a
      `github.com/johacks24/vciudadania` — opción mejor: enlace directo al fichero
      (`blob/main/docs/metodo/metodo.md`, que es lo que dice el texto del enlace) —,
      regenerar con `make exportar` y validar. Consecuencia prevista en ADR-0006 —
      día 12/11*

## Scope E — Cierre

- [x] E.1 docs/apuestas.md con la apuesta «Pleno XV navegable» en investigación
- [x] E.2 Commits limpios por scope (perfect commit: código + test + doc juntos)
