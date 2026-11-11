# Apuestas — índice

La tabla es la ÚNICA fuente de verdad de los estados (regla: cada dato vive en un único
sitio). La **descripción** dice qué es la apuesta (estable; se escribe al moldear). El
**estado** dice dónde está (se actualiza aquí y solo aquí).

**Estados:** consideración → investigación → desarrollo → producción

- **consideración:** idea apuntada. Sin carpeta.
- **investigación:** carpeta creada (`yymmdd_<nombre>`); se moldea el plan.
- **desarrollo:** plan aprobado; se construye con `/siguiente`.
- **producción:** desplegada, validada y pública.

| Apuesta | Descripción | Estado | Carpeta |
|---|---|---|---|
| Fundamentos y spike | Cadena completa validada (Congreso → ingesta → validación 100 % → datos → ficha pública) + decisiones de base | producción | 20261110_fundamentos-y-spike |
| Pleno XV navegable | Toda la legislatura XV con búsqueda, fichas y voto por grupo | investigación | 20261110_pleno-xv-navegable |
| API pública v1 | Datasets estáticos (JSON + CSV) documentados, con citas y método de reutilización | consideración | — |
| Resúmenes trazables | Resumen de cada iniciativa por frase citada (extract → redact → verify) + golden set | consideración | — |
| Juego de coincidencias | 12–30 votaciones reales, % de acuerdo con cada grupo, compartible y sin registro | consideración | — |
| Chat «investiga la iniciativa» | Preguntas sobre el expediente y su evolución con citas obligatorias | consideración | — |
| Co-creación ciudadana de normas | Co-redacción de proyectos de ley (estilo Leyes Abiertas), continuidad de cada ILP en el Pleno y presión ciudadana en su consideración; el canal de retorno es la ILP (Boreal resuelve las firmas; Polis, el consenso; la trazabilidad del proyecto, la continuidad) | consideración | — |

## Cómo se decide la siguiente apuesta

Al cerrar una (cooldown): revisar `docs/aprender.md`, repasar la tabla, moldear la
elegida (crear su carpeta desde `_plantilla.md` y escribir su `plan.md`) y cambiar su
estado a **desarrollo**. Las apuestas en *consideración* no llevan carpeta: se crea al
empezar la investigación.
