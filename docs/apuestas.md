# Apuestas — tablero

El trabajo del proyecto son **lotes verticales**: cada uno entrega funcionalidad completa
para producción (backend → frontend → URL pública), pero estrecha. Reglas: se moldea el
lote antes de construir (shaping), se apuesta, se construye con `/siguiente`, y entre
lote y lote hay cooldown (limpiar, aprender, repasar).

| Lote | MVP vertical | Estado |
|---|---|---|
| **00 Fundamentos + spike** | Una votación real publicada en internet, con recuentos validados al 100 % | **En curso** (10/11/2026) |
| 01 Pleno XV navegable | Todas las votaciones de la XV con búsqueda, fichas y apoyo por grupo | Piteado (ver abajo) |
| 02 API pública v1 | Datasets estáticos (JSON + CSV) con documentación y citas | Apuntado |
| 03 Resúmenes trazables | Resumen por frase citada (extract → redact → verify) + golden set | Apuntado |
| 04 Juego de coincidencias | 12–30 votaciones reales, % de acuerdo con grupos, compartible | Apuntado |
| 05 Chat "investiga la iniciativa" | Preguntas sobre el expediente con citas obligatorias | Apuntado (fase 2) |

---

## Lote 01 — Pleno XV navegable (piteado, pendiente de moldear)

**Problema:** una única votación demostró la cadena; nadie puede *usar* el proyecto
todavía para mirar qué votó su diputado o su partido.

**Apuesta:** ingesta completa de la XV (~2.200 votaciones del Pleno) con el mismo
pipeline validado del lote 00, buscador y ficha por votación, en producción.

**No-objetivos:** resúmenes con IA (03), juego (04), comisiones, Senado, XIV.

**Conejos (riesgos):** (1) tamaño de ingesta y tipos raros de votación (asentimiento,
suplicatorios secretos, votaciones por puntos) — regla: cubrir lo publicable, marcar lo
no publicable; (2) **decisión de diseño sobre el color de los grupos** — eslahoradelaverdad
evita colores de partido por neutralidad; decidir con ADR propia dentro del lote;
(3) identificadores de diputado entre legislaturas.

**Recorridos de usuario:**
1. Abro la web y veo las votaciones más recientes.
2. Busco por palabra (p. ej. «alquiler») y filtro.
3. Abro una ficha: qué se votó, recuento, voto por grupo, fuente oficial.
4. Descargo el dataset completo con su cita.

**Cuándo está hecho:** la XV completa navegable en producción con validación verde en CI.

---

## Cómo se decide el siguiente lote

Al cerrar un lote (cooldown): revisar `docs/aprender.md`, repasar la lista de arriba,
moldear el elegido (`lotes/<NN>/plan.md` completo) y cambiarlo a "En curso".
