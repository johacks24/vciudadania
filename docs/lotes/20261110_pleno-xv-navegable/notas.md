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

## 23/11/2026 · B.5 completada: SQLite completa de la XV

- `make exportar-legislatura`: **2.175 votaciones + 760.518 votos + 19.561 resúmenes
  por grupo + 412 diputados** en `data/processed/congreso.sqlite` (59 MB), en 3 s,
  con 0 votaciones marcadas con descuadre. Las 2 no nominales son los dos
  suplicatorios (Leg202-021 y Leg89-005, Comisión del Estatuto de los Diputados).
- **Cierre exacto con quevotan, otra vez:** sus 764.718 votos individuales −
  nuestros 760.518 = **4.200 = 12 llamamiento × 350 diputados** (los nombres que
  ellas recuperan del Diario y que el opendata no publica).
- Reconstrucción limpia: el exportador ahora también borra `votaciones` antes de
  escribir (antes dejaba votaciones huérfanas de una exportación anterior).
- Modo legislatura: carga los diputados ANTES de escribir nada (fallo rápido, sin
  base a medias); el modo sesión del lote 00 queda intacto y verificado (`make
  exportar` regeneró la ficha de la sesión 202 sin cambios).
- La web completa de la XV (portada, buscador, ~2.190 fichas) es el scope C: esta
  base es su fuente.
- 4 tests nuevos (`test_exportar.py`): las cuatro tablas, fallo rápido sin
  diputados, reconstrucción limpia entre modos, idempotencia → 23/23.

## 23/11/2026 · C.1 completada: portada índice con scroll infinito

- `make web` → `web/portada.html` + `web/indice.json`, generados desde la SQLite de
  B.5 (la web del scope C lee la base, no los raw: la base es su capa de datos).
- **Decisión de transición:** la portada vive en `portada.html` hasta que C.4 genere
  las ~2.190 fichas; entonces se promueve a `index.html`. Así la producción del
  lote 00 (ficha de la sesión 202 en Pages) no queda rota a medias. Los enlaces de
  los elementos ya apuntan a `votacion/<id>.html` (existen a partir de C.4).
- Mejora progresiva: los primeros **50** van en el propio HTML (se ven sin
  JavaScript); el resto se carga al llegar al final (IntersectionObserver con
  margen de 600 px; botón «Mostrar más» como respaldo). Índice: 510 KB con 2.175
  items; el ORDEN del array ES la cronología — el cliente no ordena nada.
- Orden: recientes primero, parseando la fecha de la fuente (D/M/YYYY no es
  ordenable como texto); dentro de un día, sesión y número descendentes. Extremos
  verificados: la más reciente es Leg202-021 (30/9/2026) y la más antigua
  Leg2-001 (19/9/2023), la primera votación de la XV.
- Los elementos muestran recuentos («137 Sí · 175 No · 34 Abst.»), no veredictos:
  la ficha del lote 00 ya razonó por qué («Más Sí que No» ≠ «aprobada» con mayoría
  cualificada). Las 2 no nominales llevan su marca explícita. Todo texto de la
  fuente, escapado.
- 5 tests nuevos (`test_portada.py`): orden, contrato del índice, primeros sin
  JavaScript, límite de N estáticos, escape de HTML → 28/28.

## 23/11/2026 · C.2 completada: búsqueda por palabra y filtro por resultado

- Todo en cliente sobre el índice de C.1 (ADR-0002), con antirrebote de 150 ms y el
  mismo scroll por tandas para los resultados.
- **Búsqueda por palabra sobre título + texto del expediente**, normalizando
  acentos y mayúsculas. Decisión con datos: el ejemplo del propio plan
  («alquiler») no aparece en **ningún** título de la XV (la palabra oficial es
  «arrendamiento»), pero sí en 14 expedientes; «vivienda», en 71. El índice
  (1,0 MB) lleva el campo `expediente` solo para buscar: la lista sigue mostrando
  el título. Verificado como lo hace el cliente: «alquiler» → 14;
  «convalidación» y «convalidacion» → 97.
- **Filtro por resultado honesto:** «Más Sí que No» / «Más No que Sí» / «Empate»,
  calculado **en vivo** desde los recuentos — el índice no guarda veredicto, porque
  «más Sí que No» no es «aprobada» cuando la mayoría es cualificada (nota visible
  bajo el filtro). Distribución real de la XV: 993 · 1.163 · 19 empates.
- Contador de resultados accesible (`aria-live`) y estado vacío («Sin resultados
  para esa búsqueda»).
- 3 tests nuevos → 31/31. La búsqueda y el filtro requieren JavaScript (mejora
  progresiva): sin él, la portada sigue mostrando los primeros 50 de C.1.

## 23/11/2026 · Corrección (4x4 nº 7): enlaces «Fuente oficial» rotos — resuelto

Al preparar C.3 (cruce con el CSV de CongresoAbierto por `url_votacion`) la
intersección dio **0 de 2.175**: nuestras `fuente_url` reconstruidas eran inválidas
y **todos los enlaces «Fuente oficial» de la ficha en producción daban 404**. Dos
conversiones que `url_desde_ruta` no hacía, verificadas contra el servidor con
peticiones reales:

- **legislatura**: el almacenamiento usa el romano (`data/raw/LegXV/`) y la URL
  oficial el ordinal (`…/votaciones/Leg15/…`) — LegXV → 404, Leg15 → 200;
- **sesión**: el almacenamiento guarda el entero sin ceros (`Sesion98`) y la URL
  oficial rellena a 3 dígitos (`Sesion098`) — Sesion2 y Sesion98 → 404;
  Sesion002 y Sesion098 → 200 (la página del día de hoy enlaza con relleno).

Arreglado con parser romano→ordinal y relleno a 3 dígitos en `url_desde_ruta`
(el almacenamiento no cambia: es nuestro y coherente). Regenerados ficha y base;
**verificado con peticiones reales a sesiones 002, 098 y 202: HTTP 200**, y el cruce
con el CSV pasa a **2.175 de 2.175**. La causa raíz: la verificación del lote 00
(D.2) comprobó que los enlaces estaban en la página, no que resolvieran — y el
primer intento de arreglo solo probó la sesión 202, que no necesita relleno.
Lección nº 7 en `AGENTS.md`. El despliegue de la ficha corregida va con este
commit.

## 23/11/2026 · C.3 completada: temas de CongresoAbierto + filtro por tema

- `make temas` descarga su CSV a `data/raw/congresoabierto/votaciones.csv`
  (inmutable) e importa la asignación de temas como **fuente secundaria**
  (ADR-0005.3): cruce por `fuente_url` —la URL oficial del JSON, ya corregida
  esta misma tarde— y **atribución CC BY 4.0** visible en el pie de la portada y en
  el log.
- **Contraste: 2.175 de 2.175** votaciones cruzadas (2.504 pares tema-votación),
  sin avisos.
- Catálogo corregido con el separador real: la columna `temas` separa con **« | »**.
  El primer sondeo partía por comas y dio 76 «temas» falsos (cadenas unidas por
  pipe). El real: **15 temas**, 299 votaciones con varios (p. ej., el suplicatorio
  de la 89: «justicia | instituciones»), 0 sin tema. Frecuencia: otros (749),
  transporte (266), economia (261), justicia (169), trabajo (158), sanidad (139)…
- Filtro por tema en la portada (tercer desplegable, con la cuenta en cada
  opción), combinable con palabra y resultado. El índice lleva `temas` por
  votación; sin tabla de temas, la portada degrada a «Todos» sin romperse.
- Su columna `resultado` (Aprobada 951 · Rechazada 1.170 · Convalidado 42 ·
  Derogado 12) **no se adopta**: mantenemos los recuentos honestos de la ficha.
- 5 tests nuevos (fixture de 2 filas reales de su CSV) → 37/37.

## 23/11/2026 · C.4 completada: fichas de toda la XV con waffle + portada promovida

- `make web` genera ahora la web completa en 3 s: **portada promovida a
  `index.html`** (la ficha del lote 00 queda sustituida por la portada con
  buscador; `portada.html` retirada), el índice y **2.175 fichas** en
  `web/votacion/<id>.html` (102 MB; comparable al ~90 MB de quevotan).
- Cada ficha (recorrido 3): qué se votó (título + expediente + tema con
  atribución CC BY 4.0), recuento honesto («Más No que Sí», sin veredictos),
  **waffle según la ADR-0007** (una celda por diputado, relleno con el color del
  grupo, voto por posición en secciones Sí/No/Abstención/No vota con su número,
  detalle por diputado a demanda en el `<title>` del rectángulo, leyenda
  chip+sigla+nombre en el orden fijo de bloques con el Mixto al final), la tabla
  «voto por grupo» completa en texto (el color es redundante, nunca único) y la
  fuente oficial enlazada. SVG estático, sin JavaScript.
- **Sin voto individual (los 2 suplicatorios):** sin waffle ni tabla; totales +
  nota de categoría, con su fuente enlazada igualmente.
- Verificación con la lección nº 7 aplicada: enlaces de fuente de 4 fichas con
  sesiones de 1, 2 y 3 dígitos (Leg2-001, Leg89-005, Leg98-021, Leg202-010) →
  **HTTP 200**; integridad del waffle contra la base: 350 celdas = 350 votos
  nominales, y las secciones reproducen los totales oficiales (34/312/0/4 en la
  202-010; 176/169/2/3 en la 2-001, la primera votación de la XV).
- El modo sesión de `exportar` deja de escribir la web (solo SQLite de esa
  sesión): `make web` es el único generador del sitio y regenera el directorio
  de fichas completo (sin huérfanas).
- 4 tests nuevos (estructura del waffle, ficha nominal, ficha no nominal,
  regeneración limpia) → 41/41.

## 23/11/2026 · D.1 completada: dataset descargable con su cita

- `make web` genera ahora también **`web/datos/votaciones.json` (1,3 MB) y
  `votaciones.csv` (920 KB)**: una fila por votación con qué se votó (título y
  expediente), totales oficiales, temas, marca de «voto individual» (2 no
  nominales) y **el enlace a su registro oficial en cada fila** — 2.175 filas, 0
  sin fuente. El dataset de votos individuales por diputado queda para la apuesta
  «API pública v1» (no-objetivo del lote, como marca la tarea).
- **El JSON es autodescriptivo**: legislatura, n, cita, licencias y fuente van
  dentro; el CSV se cita solo por fila y la portada lleva la sección «Descarga los
  datos» con la cita completa (la nuestra CC BY-SA 4.0 y la de los temas de
  CongresoAbierto CC BY 4.0) y el enlace al método.
- **Artefactos deterministas:** sin fecha de generación — la XV es un corpus
  cerrado y regenerar no debe cambiar nada (verificado en la práctica: al
  regenerar la web, las 2.175 fichas ni se tocaron; el versionado es el del repo).
- El índice de la portada gana el campo `fuente` por votación: cada dato publicado
  lleva su enlace oficial, también el que viaja en el navegador.
- 3 tests nuevos (JSON autodescriptivo, CSV íntegro con quoting, portada con la
  sección de descarga) → 44/44.

## 23/11/2026 · E.1 completada: CI verde sin red y validación de la XV al 100 %

- **Qué ejecuta la CI** (`.github/workflows/ci.yml`): Python 3.11,
  `pip install -e "congreso[dev]"` y `pytest congreso -q` en cada push y pull
  request. La suite (**44 tests**) es **sin red por construcción**: los datos son
  fixtures reales commiteados (la votación 010 completa de la sesión 202, los
  exportadores de diputados, recortes de las páginas del opendata y 2 filas del
  CSV de CongresoAbierto) y las 4 llamadas HTTP de los tests están interceptadas
  (monkeypatch de `httpx.get` en test_fuentes y test_diputados); la descarga del
  CSV en test_temas se salta por idempotencia (el fichero ya está). Ningún test
  depende de congreso.es ni de congresoabierto.org.
- **`make validar` sobre la XV completa, re-verificado hoy:** 2.175 votaciones —
  2.173 con recuento individual == totales oficiales, 2 no nominales
  (suplicatorios), **0 descuadres, 0 duplicadas** (1,3 s). El método y el contraste
  con el ecosistema, en la entrada de B.3. La regla de publicación: la validación
  es la puerta — un descuadre bloquea la salida (código 1).
- 44/44 en local y **CI verde en cada commit del lote** hasta hoy; este mismo
  commit vuelve a demostrarlo.

## 23/11/2026 · E.2 completada: despliegue verificado y lote cerrado

**Verificación del despliegue en Pages con peticiones reales** (la lección nº 7
aplicada al despliegue: que el fichero exista en la URL no basta; debe resolver Y
ser la versión actual):

- **HTTP 200** en todo el arsenal: portada (`/` e `index.html`), `indice.json`,
  fichas de sesiones de 1, 2 y 3 dígitos (Leg2-001, Leg89-005, Leg98-021,
  Leg202-010/021) y dataset (`datos/votaciones.json` y `.csv`).
- **Byte a byte idénticos al commit** (`cmp` contra `web/`): lo servido es la
  versión de D.1 (portada con «Descarga los datos», índice con `fuente`/`temas`,
  fichas con waffle y fuente oficial corregida Leg15/Sesion202), no un despliegue
  viejo del lote 00. El flujo «Paginas» (`paginas.yml`) despliega `web/` en cada
  push a main que toca `web/**`; el despliegue estaba al día sin intervención.
- **Recorridos 1–4 sobre el sitio servido:** (1) la portada abre con las
  votaciones más recientes (Leg202-021 la primera; 50 estáticas sin JavaScript,
  scroll infinito con botón de respaldo); (2) buscador y filtros cargan su índice
  de 2.175 items con `expediente`, `temas` y `fuente`; (3) la ficha muestra waffle
  + tabla por grupo + fuente oficial; (4) «Descarga los datos» enlaza el JSON
  autodescriptivo (cita, licencias y fuente dentro) y el CSV.
- **Puerta de publicación re-verificada antes de cerrar:** `make validar` →
  2.175 votaciones (2.173 nominales == totales oficiales, 2 suplicatorios),
  0 descuadres, 0 duplicadas; `make test` → 44/44.
- **Corrección menor en producción:** `web/README.md` describía la web del lote 00
  («la ficha pública», generada con `make exportar`) y un comando que desde C.4 ya
  no escribe la web; reescrito con el contenido real (portada, índice, fichas,
  dataset) y la secuencia de dependencias verificada en el CLI (ingesta →
  diputados → validar → exportar → temas → web). El generador no lo toca.
- **Lote cerrado:** 16 commits del moldeo a E.2, uno por tarea (perfect commit:
  código + test + doc); la apuesta pasa a **producción** en `docs/apuestas.md`
  (desplegada, validada y pública). Siguiente: cooldown — revisar
  `docs/aprender.md` y `docs/apuestas.md` y moldear la siguiente apuesta.












