# Tareas — Lote 00

Marca `[x]` al completar. El agente trabaja de arriba abajo con `/siguiente`.

## Estado vivo

- **En exploración:** ninguna
- **En construcción:** B.5 (bloqueada: requiere push a GitHub) · D.2 (bloqueada:
  requiere credenciales de despliegue — decisión en `docs/decisiones/0006-despliegue.md`)

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
- [ ] B.5 CI mínima verde (tests) — *workflow creado; «verde» requiere push a GitHub*

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
- [ ] D.2 Despliegue público (URL accesible) — *BLOQUEO: faltan credenciales del humano.
      Decisión y alternativas: `docs/decisiones/0006-despliegue.md` (GitHub Pages;
      Vercel si la web pasa a Next.js; Codeberg Pages como opción menor). Preparado:
      `make exportar` genera el sitio estático; el despliegue es activar Pages tras el
      primer push.*

## Scope E — Cierre

- [x] E.1 docs/apuestas.md con la apuesta «Pleno XV navegable» en investigación
- [x] E.2 Commits limpios por scope (perfect commit: código + test + doc juntos)
