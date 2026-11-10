# ADR-0001: Solo yo + agentes; lotes de 1–2 semanas

**Fecha:** 2026-11-10 · **Estado:** aceptada

**Contexto:** proyecto individual con agentes de código (OpenCode). Había que decidir
ceremonia de proceso y tamaño de iteración.

**Decisión:** sin equipo humano inicial. Lotes de 1–2 semanas con cooldown entre ellos.
Todo el flujo de construcción pasa por la plantilla de lote (plan.md + tareas.md) y el
comando /siguiente.

**Consecuencias:** sin PRs de personas, CI simple; los lotes deben ser estrechos porque
el revisor final es uno. Si entra alguien, se revisa esta decisión.
