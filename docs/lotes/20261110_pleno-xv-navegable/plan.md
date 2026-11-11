# Lote 01 — Pleno XV navegable

**Plan borrador aprobado como apuesta en investigación.** Al moldear se afina este plan
y nacen `tareas.md` y `notas.md` (desde `_plantilla.md`). Estado vivo en `docs/apuestas.md`.
**Tamaño estimado:** 2–3 semanas (a fijar al moldear).

## Problema

Una votación demostró la cadena (lote 00), pero nadie puede usar todavía el proyecto
para mirar qué votó su diputado o su partido a lo largo de la legislatura.

## Apuesta

Ingesta completa de la XV (~2.200 votaciones del Pleno) con el pipeline validado del
lote 00, buscador y ficha por votación, en producción.

## No-objetivos

Resúmenes con IA (Resúmenes trazables) · juego (Juego de coincidencias) · comisiones ·
Senado · XIV · API pública v1.

## Riesgos de desvío (rabbit holes)

1. Tipos raros de votación (asentimiento, suplicatorios, votaciones por puntos) — regla:
   cubrir lo publicable; marcar explícitamente lo no publicable.
2. **Color de los grupos parlamentarios:** eslahoradelaverdad lo evita por neutralidad.
   Decidir con ADR propia (0007) dentro de este lote.
3. Identificadores estables de diputado (altas/bajas/cambios de grupo).
4. **Análisis previo obligatorio:** holapolitica y quevotan (informe-ecosistema) antes
   de fijar el alcance — pueden mover el diseño del buscador y de las afinidades.

## Recorridos de usuario

1. Abro la web y veo las votaciones más recientes.
2. Busco por palabra («alquiler») y filtro por tema/resultado.
3. Abro una ficha: qué se votó, recuento, voto por grupo, fuente oficial.
4. Descargo el dataset completo con su cita.

## Cuándo está hecho

La XV completa navegable en producción, validación verde en CI, dataset descargable.
