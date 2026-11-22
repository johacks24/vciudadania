# Notas — Lote 01 (Pleno XV navegable)

## 22/11/2026 · Moldeo: verificaciones previas y decisiones de «cómo»

Verificaciones contra fuentes (comandos exactos en `informe-ecosistema.md`):

- **El opendata sigue vivo:** `congreso.es/es/opendata/votaciones` responde HTTP 200 con
  user-agent de navegador y trae el índice `diasVotaciones` con **147 días con
  votaciones** en la XV: del 19/09/2023 al **02/10/2026** (última votación).
- **La XV es un corpus cerrado:** disuelta el 06/10/2026 (Real Decreto 806/2026;
  elecciones el 29/11/2026, BOE-A-2026-20742). No entran votaciones nuevas hasta la
  XVI. Magnitudes de contraste (quevotan.eu, verificadas): 2.189 votaciones
  (2.185 con voto nominal), 149 sesiones plenarias, 764.718 votos individuales,
  412 diputados distintos (altas/bajas).
- **La sesión 202 del spike cuadra con el ecosistema:** quevotan lista las mismas
  21 votaciones del 30/09/2026 que validamos en el lote 00, y su última sesión (203,
  02/10/2026, 2 votaciones) coincide con el último día del índice oficial.

Decisiones de diseño tomadas al moldear (los «cómo» quedan resueltos; ninguna tarea
arranca «En exploración»):

1. **Corpus cerrado → ingesta única:** la XV completa se descarga y valida de una vez;
   sin actualización periódica hasta que exista XVI. Refuerza ADR-0002 (estático por
   lotes) y simplifica la CI.
2. **Búsqueda por palabra en sitio estático:** índice JSON compacto (id, fecha,
   título, resultado, tema) que el navegador filtra en cliente. Sin servidor ni
   buscador externo; coherente con ADR-0002 y con el diseño móvil primero.
3. **Filtro por tema:** se reutiliza la asignación de temas de CongresoAbierto
   (`data/manual/temas.json`, CC BY 4.0) **con atribución y validación nuestra**
   (ADR-0005, punto 3: fuente secundaria jamás sin contrastar). Nada de clasificación
   con IA en este lote (eso es la apuesta «Resúmenes trazables», fuera de alcance).
4. **Categorías sin voto individual:** suplicatorios (secreto; solo totales) y
   **públicas por llamamiento** (12 en la XV: investiduras, amnistía, reforma del
   art. 49 CE…): se marcan «sin voto individual publicado» con enlace al Diario de
   Sesiones. Extraer los nombres del PDF del Diario (como hace quevotan) queda
   **fuera** del lote: mejora futura, no ampliación.
5. **Diputados:** tabla propia desde la exportación del buscador oficial de diputados
   (altas/bajas, formación, grupo), esquema pydantic antes que el código (regla de
   AGENTS.md); el modelo no supone una sola legislatura (ADR-0003).
6. **Tamaño fijado:** ~2 semanas. Justificación: corpus cerrado (sin carga periódica),
   pipeline validado y generador de ficha ya existentes del lote 00; queda escalar la
   ingesta (147 días), el buscador estático, el dataset y el despliegue.

La apuesta pasa a **desarrollo** en `docs/apuestas.md` (única fuente de verdad del
estado). El análisis previo obligatorio del plan (riesgo 4) se ejecuta como tarea A.1
→ `informe-ecosistema.md`.

## 22/11/2026 · A.1 completada: informe del ecosistema

- Ambos proyectos analizados con el checklist del lote 00 y verificación cruzada
  (sesión 202 y última votación cuadran con nuestro spike y con el índice oficial).
  Detalle y evidencias en `informe-ecosistema.md`.
- Conclusiones operativas: el alcance del lote **no cambia**; quevotan y
  CongresoAbierto servirán como contraste de totales en B.3; los temas de
  CongresoAbierto alimentan el filtro por tema (C.3) con atribución y validación;
  la XVI (post 29/11/2026) no entra en este lote.

## 22/11/2026 · Dirección de diseño del humano + A.2 (ADR-0007)

El humano dirigió el diseño del recuento visual antes de ejecutar A.2 (quedó en
`docs/decisiones/0007-color-grupos.md` y en `docs/diseno.md`):

- **Neutralidad ≠ ocultar datos:** mostrar qué votó cada grupo es un dato; la pregunta
  del color no es ideológica sino funcional: ¿en qué interfaz trabaja?
- **Recuento visual = waffle aprobado:** una celda por diputado, color de grupo, voto
  por posición (secciones). Descartadas las codificaciones de doble canal por celda
  (contorno de voto o barra en mitades): ilegibles a ~12 px y doblan el problema
  daltónico. Sin siglas dentro de las celdas (ilegibles); leyenda + orden fijo +
  detalle a demanda.
- **Listado sin paginación:** carga automática al llegar al final de la página
  (scroll infinito) sobre el índice JSON de C.2; los primeros N sin JavaScript.
- **Sin hemiciclo literal:** el campo `asiento` se conserva en los datos (fidelidad a
  la fuente) pero no se muestra. «Lo que me interesa es qué votó cada grupo y cómo
  acordaron» — el waffle ordena por sentido del voto y por grupo, y hace visible la
  disciplina (bloque unido = grupo unido).
- **Paleta (evidencia del método):** base `grupos.yaml` de quevotan (AGPL-3.0, misma
  licencia); comprobación WCAG de contraste sobre blanco con la fórmula de luminancia
  relativa; 4 colores cumplen ≥ 3:1 tal cual y 5 se oscurecen por matiz hasta
  cumplirlo (Vox, ERC, Junts, EH Bildu, Mixto). Limitación declarada en la ADR: la
  luminancia no separa todos los pares para daltonía (Junts/EH Bildu ≈ 0.29), así que
  la garantía es la redundancia (posición + leyenda + texto), no la paleta.

A.2 completada; C.1 y C.4 actualizadas con esta dirección.

## 22/11/2026 · B.1 completada: enumeración por legislatura

Qué se construyó (commits «Lote 01: B.1 …»):

- **Cliente:** `pagina_indice` + `dias_votaciones(leg)` leen el índice del opendata
  (`?targetLegislatura=XV`), que publica `var diasVotaciones = [20230919, …]` con
  **enteros**, no claves JSON. Verificado en vivo: **XV = 147 días**
  (19/09/2023 → 02/10/2026); XIV = 170 (el parámetro discrimina legislaturas).
- **Sesión y fecha desde la URL:** la URL oficial ya trae
  `Leg15/Sesion202/20260930/…`, así que `sesion_y_fecha_de_url` las extrae y la
  ingesta ya no necesita `--sesion`: el almacenamiento es idéntico al del lote 00
  (`data/raw/LegXV/Sesion{n}/{fecha}/VotacionNNN/VOT_*.json`), sin rupturas para
  `validar`/`exportar`.
- **Modo legislatura:** `congreso ingesta --legislatura XV` (sin `--fecha`) recorre los
  147 días; **pausa educada de 0,5 s** entre descargas (como quevotan); los días sin
  JSON **no** son error en este modo. `--fecha` mantiene el modo día del lote 00.
- **Makefile:** `make ingesta` (día de prueba) sin `--sesion`; nuevo
  `make ingesta-legislatura` (XV completa) — B.2 lo ejecutará.

Evidencias de la verificación (22/11/2026):

- `make test`: **9/9** (4 del lote 00 + 5 nuevos sin red, con fixtures recortados de
  las páginas reales: `indice_opendata.html` y `dia_llamamiento.html`).
- `make ingesta` sobre la sesión 202 ya descargada: 0 ficheros nuevos, mismo layout
  (idempotencia). `make validar` sin regresión: 21 votaciones, 0 descuadres.
- `dias_votaciones("XV")` en vivo: 147 días.
- **Sesión 203 (02/10/2026):** sus 2 votaciones (RDL 26/2026 y 27/2026) son públicas
  por llamamiento y **no publican JSON por votación** — solo un ZIP por sesión
  (`VOT_20261002180000.zip`), que no usamos. En modo día devuelve código 1 con
  mensaje explicando ambos casos (fecha errónea o día de solo llamamiento); en modo
  legislatura, continúa. Esto anticipa que la cuenta de JSON de B.2 será ~2.175
  (lo de CongresoAbierto), no 2.189: la diferencia son las 12 de llamamiento, y el
  contraste exacto es tarea de B.3.

## 22/11/2026 · B.2 completada: descarga completa de la XV

Ejecución: `make ingesta-legislatura` (22:56 → 23:26, **~30 min, 0 errores**).
Ajuste de código de este mismo commit: la pausa educada de 0,5 s se aplica también
**entre páginas de día** (B.2 exige pausa «entre peticiones»; B.1 solo la ponía
entre descargas de JSON).

- **Resultado:** **2.175 JSON** en `data/raw/LegXV` (2.154 nuevos + los 21 de la
  sesión 202 ya descargados en el lote 00, que se saltaron: idempotencia verificada
  en una ejecución real de 147 días). 144 carpetas de sesión, 72 MB.
- **5 de los 147 días con 0 JSON:** días de solo votaciones públicas por
  llamamiento (el último es 02/10/2026, sesión 203). B.3 los cataloga.
- **Contraste de totales anticipado:** 2.175 = **exactamente** lo que publica
  CongresoAbierto. Con quevotan (2.189) quedan **14 de diferencia**, casi seguro
  votaciones de llamamiento sin JSON (los suplicatorios secretos SÍ publican JSON
  con solo totales, como la votación 021 de la sesión 202). Explicarlo con evidencia
  es la parte de contraste de B.3.

## 22/11/2026 · B.3 completada: validación 100 % de la XV + contraste de totales

**Validación** (`make validar`, ahora en modo legislatura; nuevo en este commit):

- **2.175 votaciones: 2.173 con detalle individual validado (recuento == totales
  oficiales), 2 no nominales, 0 descuadres, 0 duplicadas** — 1,3 s, sin red.
- Las 2 no nominales (suplicatorios secretos, JSON con solo totales): **sesión 89**
  (22/01/2025, votación 5) y **sesión 202** (30/09/2026, votación 21).
- CLI: `congreso validar --legislatura XV` (sin sesión/fecha) valida toda la
  legislatura e imprime solo los problemas; `--sesion/--fecha` mantiene la tabla del
  lote 00. Añade detección de **ids duplicados** (la fuente listando una votación dos
  veces): 0 encontradas. Tests: 4 nuevos → 13/13.

**Contraste de totales** (evidencia, sesión a sesión contra quevotan.eu/XV/sesiones/
consultado el 22/11):

- **CongresoAbierto: 2.175 = exacto** con nuestros JSON (ambos consumimos solo el
  opendata; su CSV iba al día).
- **quevotan: 2.189 = nuestros 2.175 + 14 votaciones públicas por llamamiento sin
  JSON en el opendata**, repartidas en 10 sesiones: 5, 6 (investiduras, 27 y
  29/09/2023), 8, 11, **15 × 4 (día de la amnistía, 10/01/2024)**, 17, 18, 30, 43 y
  **203 × 2 (convalidaciones RDL, 02/10/2026)**. La tarea decía «12 en la XV» (cifra
  de su README); la exacta verificada es **14**, de las que **12** tienen nominal
  recuperado del Diario de Sesiones (su especialidad) y 2 no (las de la sesión 203).
- **Cierre exacto por ambas columnas:** 2.189 = 2.175 + 14, y su «con voto nominal»
  2.185 = 2.173 + 12; sus 4 sin nominal = 2 suplicatorios + 2 de la sesión 203.
- Evidencia directa en sesión mixta: la página de la sesión 15 marca «(Pública por
  llamamiento)» en sus votaciones 8, 9, 11 y 12 — exactamente las 4 que nos faltan
  de sus 12.
- Conclusión de producto: nuestro universo publicable es el de las **2.175 con JSON**
  (el mismo que CongresoAbierto); las 14 de llamamiento quedan como categoría
  documentada «sin voto individual publicado», enlazable al Diario sin extraer el
  PDF (fuera del lote).

## 22/11/2026 · B.4 completada: tabla de diputados de la XV

- **Esquema pydantic `Diputado` antes del código** (regla de AGENTS.md), con los
  campos reales del exportador, catalogados contra la XV completa antes de validar.
- Fuente: `congreso.es/es/opendata/diputados`, exportadores «Diputados en Activo» +
  «De Baja en la legislatura actual». La URL rota a diario con marca temporal: el
  cliente parsea la página del opendata, `data/raw` guarda el fichero con su marca
  temporal (inmutable) y la carga toma el más reciente de cada clase.
- **412 diputados = 137 activos + 275 con baja**, la cifra exacta de quevotan («412
  diputados distintos»). 213 bajas son del 06/10/2026 (disolución) y 62 personales
  (renuncias que trajeron suplentes).
- **Clave natural verificada:** 412 nombres únicos sin duplicados; el formato
  «Apellidos, Nombre» del exportador es idéntico al campo `diputado` de los JSON de
  votación → la unión votos↔diputados será por nombre exacto. El exportador no trae
  código de diputado.
- **9 grupos con nombre oficial completo** (filas de la tabla): Socialista 157,
  Popular 152, VOX 33, Plurinacional SUMAR 30, Mixto 11, Junts 8, Republicano 8,
  Euskal Herria Bildu 7, Vasco (EAJ-PNV) 6. El mapeo código (GS, GP, GVOX…) →
  nombre queda servido para las fichas.
- **Limitación declarada:** el exportador trae el grupo FINAL con su fecha de alta
  (caso real: Belarra, formación SUMAR, grupo Mixto desde el 05/12/2023); la
  pertenencia anterior no consta. La historia completa por diputado se puede derivar
  del campo `grupo` de los JSON de votación si algún día hace falta — no en este lote.
- SQLite: tabla `diputados`, PRIMARY KEY (legislatura, nombre) — ADR-0003: sin suponer
  una sola legislatura; el borrado es por legislatura, no global. `make diputados`
  descarga, valida y escribe; re-ejecutar no re-descarga (idempotente, verificado).
- **4x4 nº 6 resuelto** (lección en AGENTS.md): una regex con grupo de captura
  construyó URLs rotas y el test las dio por buenas asertando subcadenas; el 404 real
  apareció al ejecutar. Ahora el test aserta las URLs completas.




