# AGENTS.md — reglas del proyecto

Proyecto: **vCiudadania** — la versión ciudadana de las decisiones públicas (la «v» es
de versión: vParlamento frente a vCiudadania). Trazabilidad de votaciones del Congreso
de los Diputados (España). Cívico, independiente, sin recomendación de voto.

## Idioma y estilo

- Todo en **castellano**. No hay i18n (decisión registrada en docs/decisiones).
- Explicaciones: primero qué es, luego para qué sirve aquí, luego el comando exacto.
- **Sin calcos forzados:** concepto explícito en castellano, o término en inglés entre
  paréntesis. Prohibidos: «colina», «conejos», «piteado». Estados de tarea:
  **En exploración / En construcción**. Estados de apuesta: **consideración /
  investigación / desarrollo / producción**.

## Comandos (hacer, no improvisar)

Todo entra por el Makefile: `make setup | ingesta | validar | exportar | test | dev | tail-logs`.
Si un comando falla, no inventes variantes: lee el error, arregla la causa.

## Estructura

- `congreso/` — paquete Python: `fuentes/` (clientes de congreso.es y BOE), `modelo.py`
  (esquemas pydantic), `exportar_sqlite.py`, `exportar_ficha.py`, `cli.py`, `tests/`.
- `web/` — la webapp (la ficha se GENERA con `make exportar`; no edites `web/index.html` a mano).
- `docs/` — `apuestas.md` (índice de apuestas: ÚNICA fuente de verdad de los estados),
  `lotes/` (una carpeta por apuesta: plan.md + tareas.md + notas.md + `informe-<tema>.md`;
  plantilla canónica en `lotes/_plantilla.md`), `decisiones/` (ADR), `metodo/` (público),
  `referencias/` (indice.md público; `_privado/` con originales de terceros, no versionado).

### Convenciones de docs (lecciones de moldeo del 10-11/11/2026)

- Carpetas de apuesta: `yymmdd_<nombre-corto>`. La fecha es la de apertura y no cambia
  nunca. Referencias cruzadas por **nombre corto**, nunca por número o fecha.
- El estado de una apuesta vive **solo** en `docs/apuestas.md`. En `plan.md`: fechas y
  tamaño, no estado. Descripción del índice = qué es (estable), no progreso.
- Nada de una plantilla se omite sin declararlo («No aplica» + porqué).
- Evidencias largas del lote → `informe-<tema>.md`; `notas.md` es el diario del lote.
- Plantilla de apuesta obligatoria: nueva carpeta se crea copiando `lotes/_plantilla.md`.
- `data/` — generada, nunca versionada. `data/raw/` es inmutable: no editar lo descargado.

## Fuentes y trazabilidad (innegociable)

- Fuente primaria: datos abiertos del Congreso (JSON por votación en
  `congreso.es/webpublica/opendata/votaciones/...`) y BOE.
- **Cada dato publicado lleva su enlace a la fuente oficial.** Sin fuente, no se publica.
- Todo recuento se **valida** contra los totales oficiales (`make validar`). Si el
  Congreso dice 172 Sí, la base debe decir 172.
- Los JSON descargados en `data/raw/` son inmutables; la transformación es reproducible.

## Licencias

- Código: AGPL-3.0. Contenidos y datos elaborados: CC BY-SA 4.0 (`LICENSE-CONTENIDOS.md`).
- No commitear originales de terceros (libros, artículos HTML): van en
  `docs/referencias/_privado/` (gitignored). Lo nuestro es el destilado en `indice.md`.

## Cuando algo se rompe: regla 4x4 (Lazar Jovanovic)

Cada peldaño se intenta **UNA vez**; no repitas un peldaño que ya falló.

1. **Reintenta** en la misma sesión (auto-corrección).
2. **Capa de conciencia:** ejecuta `make tail-logs`, lee el error real y pega la salida
   al contexto. El agente no arregla lo que no ve. Esto resuelve casi todo.
3. **Revisor externo** en sesión nueva (subagente u otro modelo): **solo diagnostica,
   no toca código**.
4. **Retrocede** a commits limpios y replantea el prompt: casi siempre el fallo es un
   brief mal planteado.

Después de cada 4x4 resuelto: escribe la lección en «Lecciones» (abajo) como regla
operativa para el agente, no como nota para el humano. El aprendizaje del proyecto
(datos, producto, fuentes) va a `docs/aprender.md`.

## Trato al agente (cultural, de Lazar)

- «Ya está arreglado» no es verdad hasta que los logs o los tests lo confirman.
- Sin broncas al modelo: gasta tokens gestionando el enfado en vez del bug.
- Si algo se rompe, el sospechoso inicial es el brief: corrige el brief.

## Ejecución de tareas

- **Ninguna tarea se ejecuta sin su brief** en `tareas.md` del lote en curso. Los pedidos
  libres solo sirven para explorar; el cambio real siempre nace de una tarea listada.
- Un lote es un **corte vertical** completo (backend → frontend → producción) pero
  **estrecho**: mejor una votación publicada que diez a medias.
- Antes de tocar datos: define primero el esquema (modelo pydantic), después el código.
- Cambios quirúrgicos: cada línea debe trazarse a la tarea. No "mejorar" código ajeno.

## Lecciones (el agente aprende aquí, peldaño 5 del 4x4)

- 2026-11-10 (4x4 nº 1, validación): el primer `make validar` falló en las 20 votaciones
  nominales porque el catálogo de valores de `voto` se escribió de memoria (faltaba
  «No vota»). **Regla: catalogar los valores reales observados en los datos ANTES de
  escribir reglas de validación**; si aparece un valor no catalogado, mirar su
  distribución real antes de asumir que es un error del dato.
- 2026-11-11 (4x4 nº 2, revisión del lote): la plantilla de lote se escribió «de
  memoria» y se omitió la sección de estados de tarea sin declararlo. **Regla: toda
  apuesta nueva se crea copiando `docs/lotes/_plantilla.md`; nada se omite sin
  declararlo («No aplica» + porqué).**
- 2026-11-11 (4x4 nº 3, revisión del lote): el lote 01 existía en dos sitios
  (`apuestas.md` y `lotes/01/plan.md`) y las copias divergieron. **Regla: cada dato
  vive en un único sitio** — el estado de las apuestas solo en `docs/apuestas.md`;
  descripciones estables, nunca progreso duplicado.
- 2026-11-11 (4x4 nº 4, lengua): se usaron calcos del inglés que en castellano no se
  entienden («colina» por hillchart, «conejos» por rabbit holes, «piteado» por
  pitch/ched). **Regla: concepto explícito en castellano o término en inglés entre
  paréntesis; cuando haya duda de traducción, se deja en inglés.**
