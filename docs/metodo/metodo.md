# Método — cómo lo hacemos (v0, pública)

Tres compromisos: **fuente primaria siempre citada**, **todo recuento validado**,
**sin valoraciones**.

## De dónde salen los datos

- Votaciones, resultados y voto de cada diputado: datos abiertos del Congreso de los
  Diputados (`congreso.es/es/opendata`).
- Textos de las normas: Boletín Oficial del Estado (BOE) y, para iniciativas en
  tramitación, el Boletín Oficial de las Cortes Generales (BOCG).

## Reglas de trazabilidad

1. Cada ficha enlaza el registro oficial (JSON de la votación, PDF del Diario de
   Sesiones, BOE) de cada dato que muestra.
2. Los recuentos de la ficha se **validan automáticamente** contra los totales oficiales
   antes de publicarse. Las discrepancias bloquean la publicación.
3. `data/raw/` (lo descargado) es inmutable y la transformación es reproducible con
   `make ingesta && make validar && make exportar`.

## Reglas de neutralidad

- Decimos **qué se votó** (la pregunta concreta del trámite, no el título legal), **qué
  resultado hubo** (recuento) y **quién votó qué** (grupos y diputados).
- No decimos a quién beneficia una norma, no recomendamos el voto, no puntuamos ni
  clasificamos a los partidos. La valoración es de quien lee.
- Los objetivos que declara una norma se atribuyen a la norma («según su exposición de
  motivos, busca…»), nunca los afirmamos nosotros.

## Distinciones que nunca mezclaremos

- **Abstención ≠ no votar.** La abstención es un voto; «no votó» incluye ausencias y no
  explica el motivo.
- **Una votación ≠ una ley.** Cada ficha indica el trámite (enmienda, dictamen,
  convalidación…) y que el resultado es de ese trámite, no de la tramitación completa.
- **Sin voto individual publicado** (suplicatorios secretos, asentimiento) es una
  categoría visible, no un fallo.

## Límites actuales (v0)

- Solo Pleno del Congreso, solo legislatura XV. Ni Senado, ni comisiones (aún), ni
  parlamentos autonómicos.
- Los resúmenes con IA llegan en el lote 03, marcados como tales y con cita por frase.

## Correcciones

Si encuentras un error, indícalo en una issue del repositorio. Las correcciones
aceptadas se publican y quedan registradas en el historial del proyecto.
