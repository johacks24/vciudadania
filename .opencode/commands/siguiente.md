---
description: Ejecutar la siguiente tarea del lote en desarrollo
---
Trabaja por el plan de la apuesta en desarrollo, en orden:

1. Lee `docs/apuestas.md` y localiza la apuesta con estado «desarrollo» (columna Estado).
2. Lee su `plan.md`, su `tareas.md` y `docs/diseno.md` (y `AGENTS.md` si aún no lo conoces).
3. En `tareas.md`: si hay tareas «En exploración» sin resolver, resuelve primero su
   «cómo» (decisión documentada en `notas.md` o ADR si cambia el rumbo) y muévelas a
   «En construcción». Después busca la primera tarea sin marcar de «En construcción».
4. Ejecútala completa: código + test + doc si aplica (perfect commit). Marca la casilla
   `[x]` al terminar.
5. Informe breve al terminar: qué cambiaste (ficheros) y **cómo lo pruebo** (comando
   exacto, p. ej. `make validar`).

No empieces otra tarea. No amplíes el alcance del plan. Si algo se rompe, aplica la
regla 4x4 de `AGENTS.md` y deja la lección aprendida en su sección «Lecciones».
