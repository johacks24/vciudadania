# Lote 01 — Pleno XV navegable

**Estado:** piteado — PENDIENTE DE MOLDEAR (rellenar este plan antes de construir)

## Problema

Una votación demostró la cadena (lote 00), pero nadie puede usar todavía el proyecto
para mirar qué votó su diputado o su partido a lo largo de la legislatura.

## Apuesta

Ingesta completa de la XV (~2.200 votaciones del Pleno) con el pipeline validado del
lote 00, buscador y ficha por votación, en producción.

## No-objetivos

Resúmenes con IA (lote 03) · juego (04) · comisiones · Senado · XIV · API documentada (02).

## Conejos

1. Tipos raros de votación (asentimiento, suplicatorios, votaciones por puntos) — regla:
   cubrir lo publicable; marcar explícitamente lo no publicable.
2. **Color de los grupos parlamentarios:** eslahoradelaverdad lo evita por neutralidad.
   Decidir con ADR propia (0006) dentro de este lote.
3. Identificadores estables de diputado (altas/bajas/cambios de grupo).

## Recorridos de usuario

1. Abro la web y veo las votaciones más recientes.
2. Busco por palabra («alquiler») y filtro por tema/resultado.
3. Abro una ficha: qué se votó, recuento, voto por grupo, fuente oficial.
4. Descargo el dataset completo con su cita.

## Cuándo está hecho

La XV completa navegable en producción, validación verde en CI, dataset descargable.
