# Auditoría de candidatos a base de datos (lote 00)

Fecha de auditoría: **2026-11-10**. Auditor: subagente de sesión. Objetivo: evaluar 3 candidatos como base de datos de votaciones del Congreso de los Diputados (XV legislatura) con un checklist idéntico (a–g) y dar recomendación de carril.

## Metodología

Comandos y fechas usados (todos el 2026-11-10):

- GitHub REST API v3, sin autenticación:
  - `curl https://api.github.com/repos/MarcoAnarmo/CongresoAbierto`
  - `curl https://api.github.com/repos/slopezmenend/civis-api`
  - `curl https://api.github.com/repos/<owner>/<repo>/commits?per_page=3`
  - `curl https://api.github.com/repos/MarcoAnarmo/CongresoAbierto/contributors`
  - `curl https://api.github.com/repos/MarcoAnarmo/CongresoAbierto/issues?state=all&per_page=100`
  - `curl https://api.github.com/repos/MarcoAnarmo/CongresoAbierto/git/trees/main?recursive=1`
- Ficheros fuente vía `https://raw.githubusercontent.com/...` (scripts, licencia, README, metodología).
- CSV de CongresoAbierto: `curl -s https://congresoabierto.org/datos/csv/votaciones.csv` (HTTP 200, `text/csv`, 947.043 bytes, 2.176 líneas = 2.175 votaciones) y `curl -s https://congresoabierto.org/datos/csv/diputados.csv` (HTTP 200).
- Cabeceras CORS: `curl -I -H "Origin: https://example.org" https://congresoabierto.org/datos/csv/votaciones.csv` → `access-control-allow-origin: *`.
- Reforma Digital: `curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ..." https://reforma-digital.es/api/congreso` y variantes (`/api/congreso/`, `/api/congreso/votaciones?q=vivienda&limite=5`, `https://www.reforma-digital.es/api/congreso`, `/`) → **429 en todas**, con cabecera `x-vercel-challenge-token` (checkpoint JS/WASM de Vercel). También `webfetch` falló con 429.
- Inspección del código: `git clone --depth 1` bloqueado por la política del sandbox; se sustituyó por lectura de los mismos ficheros vía GitHub API/raw (equivalente a shallow clone a efectos de evidencia).
- Verificación cruzada: script Python que descargó `votaciones.csv`, tomó 3 filas al azar (`random.seed(42)`) y comparó sus totales con el JSON oficial de `url_votacion` usando `curl -A "Mozilla/5.0 ..."`.

Nota metodológica: la lección registrada en AGENTS.md (catalogar los valores reales de `voto` antes de validar) ya la cumple por su cuenta el importador de CongresoAbierto: mapea exactamente `Sí/No/Abstención/No vota` → `S/N/A/X`, incluido «No vota», y aborta ante recuentos que no cuadren.

---

## Ficha 1: CongresoAbierto

Web: https://congresoabierto.org/ · Código: https://github.com/MarcoAnarmo/CongresoAbierto

**a) Licencia.** Código: MIT (campo `license` de la API de GitHub: `MIT`, `LICENSE` en el repo; badge MIT en README). Datos: **CC BY 4.0**, declarado en código: `src/lib/datos/licencia.ts` → `id: 'CC-BY-4.0'` con cita sugerida «Congreso Abierto (congresoabierto.org), a partir de datos oficiales del Congreso de los Diputados». **Sí permite reutilización con atribución** en ambos casos. Los datos subyacentes son del opendata del Congreso (uso comercial no restringido por la Cámara en datos abiertos).

**b) Actividad.** Último commit: `28288bd` de **2026-10-11** («Merge pull request #39 … feat: portada como plataforma de transparencia legislativa»), firma GPG verificada. `pushed_at: 2026-10-11`, `updated_at: 2026-10-22`. Repo creado 2026-10-03 → **30 días desde el último commit, plenamente activo** (dentro de los últimos 6 meses con holgura).

**c) Cobertura.** XV legislatura completa desde septiembre de 2023: **2.175 votaciones** (CSV `votaciones.csv`, 2.176 líneas − cabecera; la web dice «Buscar entre las 2175 votaciones del Pleno»). **Solo Pleno** (no comisiones): `data/raw/votaciones/pleno.jsonl` y el propio importador se titulan «votaciones del Pleno»; el opendata oficial también incluye comisiones permanentes y el proyecto no las ingestiona todavía (hueco natural para contribuir).

**d) Calidad de datos.**
- Voto individual por diputado: **sí**. `scripts/importar-votaciones.ts` guarda `votos: Record<codigoDiputado, 'S'|'N'|'A'|'X'>` por votación (formato compacto «S: '160 317 …'»), y la web muestra «el voto de cada diputado en cualquier votación del Pleno». El CSV público de votaciones solo trae totales, pero el CSV de diputados trae por persona `votos_si/no/abstencion/no_vota` y `votos_distintos_del_grupo`.
- Totales oficiales: **validados en el pipeline**: `importar-votaciones.ts` compara el recuento nominal con `totales.afavor/enContra/abstenciones/noVotan` del JSON oficial y **lanza excepción si no coinciden** («el recuento nominal (…) no coincide con los totales oficiales (…)»).
- Identificadores estables: id `s{sesion}-v{NNN}` (p. ej. `s202-v021`) + campo `fuente` con la URL del JSON oficial de congreso.es. El CSV conserva además `url_votacion` y `url_expediente`.
- Temas/categorías: sí, columna `temas` en el CSV y `data/manual/temas.json` (asignación por palabras, documentada en `docs/metodologia.md`); además `data/manual/votaciones-clave.json` con textos votados literales (BOE/BOCG) para votaciones clave.

**e) API programática.** No hay API REST: es una web estática (Astro) con **ficheros estáticos** CSV/JSON servidos por CDN (Cloudflare; `cache-control: public, max-age=14400`). **CORS abierto**: `access-control-allow-origin: *` verificado. Rate limits: no documentados (CDN público, sin clave). También están los JSON agregados en el propio repo (`data/congreso/votaciones.json`, `diputados.json`, `resumen.json`).

**f) Mantenimiento y comunidad.** 2 contributors (MarcoAnarmo 217 commits, peiodiazi 2). 40 issues+PRs históricos: 37 PRs cerrados, hoja de ruta pública vía issues con label `hoja-de-ruta` (abiertas: publicar JSON/CSV abiertos #20, ratio de asistencia #40, actualización mensual #14, gobiernos autonómicos #15). Hay CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, plantillas de issue (error en un dato / sugerencia) y **CI** (`.github/workflows/ci.yml`) con tests (`npm test` → `node --test tests/*.test.ts`, 8 ficheros de tests: csv, derivados, estadísticas, vínculos…).

**g) Riesgo de dependencia.** Mantenimiento por **una persona** (Marco Anarmo, pseudónimo; único contributor con peso) y proyecto **muy joven** (1 mes de vida pública). Señales positivas de sostenibilidad: ritmo de PRs alto, CI, hoja de ruta, metodología publicada y compromiso explícito «solo datos oficiales, cada dato enlaza a su documento original». Riesgo real de abandono, pero mitigado: los datos son reproducibles desde el opendata oficial y la licencia permite fork.

**Dato clave del carril 1 — ¿consume los JSON oficiales?**
**Sí, verificado en código.**
- `scripts/browser/votaciones-pleno.js` (código literal, repo `main`): selecciona los enlaces del calendario de opendata con `[...document.querySelectorAll('a[href*="/opendata/votaciones/"][href$=".json"]')]`, hace `fetch(url)` de cada uno y guarda `{ url, pdf, datos }` en `votaciones-AAAAMMDD.jsonl`. Es decir, descarga exactamente los JSON de `congreso.es/webpublica/opendata/votaciones/...` que el proyecto usa como fuente primaria.
- `scripts/importar-votaciones.ts` transforma esos JSON oficiales en `data/raw/votaciones/pleno.jsonl` (una votación por línea, votos nominales por código de diputado, totales oficiales, recuento por grupo oficial, diputados que se saltan la disciplina), **con validación dura contra los totales oficiales**.
- El CSV lo confirma empíricamente: `url_votacion` apunta a `https://www.congreso.es/webpublica/opendata/votaciones/Leg15/Sesion202/20260930/Votacion021/VOT_20260930153628.json`, etc.

**¿Podría este proyecto contribuir ahí?** Sí, y con ventaja: estructura clara (`scripts/` con un script por fuente, `data/raw/` inmutable versionado, `data/manual/` para curación), tests con CI, CONTRIBUTING, hoja de ruta con issues abiertas encajables (automatizar la descarga hoy semimanual —el script se pega en la consola del navegador día a día—, ingestar votaciones de comisiones, publicar API/CSV de votos nominales). **La licencia MIT del código y CC BY 4.0 de los datos lo permiten** (el AGPL-3.0 de nuestro código es compatible como consumidor de datos CC BY con atribución; si quisiéramos devolver código upstream, bastaría con que la contribución puntual sea MIT, como pide cualquier PR a un proyecto MIT).

---

## Ficha 2: civis-api

Código: https://github.com/slopezmenend/civis-api (README leído completo vía raw).

**a) Licencia.** `license: null` en la API de GitHub (no hay fichero LICENSE). El README declara «licencia de Reconocimiento-NoComercial 3.0 España de Creative Commons» (CC BY-NC 3.0 ES). **No sirve**: es NoComercial, no cubre el código (sin LICENSE no es reutilizable con garantías) y restringe usos.

**b) Actividad.** Último commit: `0e73e4e` de **2022-07-28** («Log Importado Diputados PG», autor slopezmenend@uoc.edu). `pushed_at: 2022-07-28`. **>4 años sin commits → candidato muerto.** Conforme a la instrucción de timebox, no se profundiza más; solo datos mínimos.

**c) Cobertura.** Nace como TFM (UOC) en 2022, antes de la XV; nada indica cobertura XV. Los datos que servía ya no están accesibles (ver e).

**d) Calidad de datos.** No evaluable en vivo (servicio caído). El README reconocía huecos: sin endpoints de iniciativas, diputados parciales, sin declaración de bienes.

**e) API.** Era una API con token (registro de usuarios) hospedada en Heroku: `curl -o /dev/null -w "%{http_code}" https://civis-api.herokuapp.com/public` → **HTTP 404** (Heroku eliminó el plan gratuito en 2022). Hoy no hay API ni ficheros accesibles.

**f) Comunidad.** 1 contributor (42 commits), 0 forks, 1 estrella, 1 issue abierta. Sin roadmap vivo.

**g) Riesgo de dependencia.** Proyecto personal académico abandonado. **Descartado.**

---

## Ficha 3: API de Reforma Digital

Docs: https://reforma-digital.es/api/congreso

**a) Licencia.** No verificable: ni la documentación ni el sitio son accesibles sin navegador (ver e). El sitio (vía búsqueda web) se presenta como «proyecto independiente, sin vinculación con la Administración», v0.1, «en construcción», centrado en trámites administrativos, con una sección Congreso («Cada pleno resumido, cada votación con el voto de cada diputado. Sesiones 39 · Votaciones 121 · Intervenciones analizadas 1549»). No hay licencia visible ni repo verificable desde aquí.

**b) Actividad.** Contenidos recientes (septiembre–octubre de 2026 según el propio sitio), pero no hay repositorio público consultable para comprobar commits.

**c) Cobertura.** Según su propia portada: 39 sesiones, 121 votaciones. Frente a las 2.175 del Pleno XV publicadas en datos abiertos, es una fracción (~5%). No consta comisiones.

**d) Calidad de datos.** Promete voto individual («cada votación con el voto de cada diputado») pero no se pudo inspeccionar un solo registro (acceso bloqueado, ver e). Sin evidencia de validación contra totales oficiales.

**e) API.** **Bloqueo total al acceso programático.** Tres endpoints probados con `curl -A "Mozilla/5.0"` devuelven `HTTP 429` con cabecera `x-vercel-challenge-token` (checkpoint JS/WASM de Vercel): `/api/congreso`, `/api/congreso/votaciones?q=vivienda&limite=5`, `/api/congreso/`, además del dominio raíz. Una API que exige resolver un reto de navegador no es consumible por un pipeline sin trucos frágiles. CORS y rate limits: indocumentados/inaccesibles.

**f) Comunidad.** Sin issues/PRs visibles; el sitio menciona GitHub genérico y contactar por DM («escríbenos por mensaje directo a Samu o a Leo»). Nada auditable.

**g) Riesgo de dependencia.** Proyecto v0.1 de dos personas, en construcción, sin licencia visible y con el acceso de datos bloqueado por CDN. **Descartado como fuente**, no por estar muerto sino por ser inutilizable programáticamente hoy.

---

## Verificación cruzada (CongresoAbierto vs JSON oficial del Congreso)

Método: 3 votaciones al azar de `votaciones.csv` (`random.seed(42)`), `curl -A "Mozilla/5.0 (…)"` a la URL de `url_votacion` (JSON oficial de `congreso.es/webpublica/opendata/votaciones/Leg15/...`), comparación de totales.

| id | Sesión/fecha | CSV (S/N/A/NV) | JSON oficial (afavor/enContra/abstenciones/noVotan) | Recuento nominal en JSON | ¿Cuadra? |
|---|---|---|---|---|---|
| s166-v009 | S166 · 2026-03-18 | 268 / 0 / 80 / 2 | 268 / 0 / 80 / 2 | Sí 268 · Abstención 80 · No vota 2 | **Sí** |
| s196-v015 | S196 · 2026-09-10 | 170 / 175 / 0 / 5 | 170 / 175 / 0 / 5 | No 175 · Sí 170 · No vota 5 | **Sí** |
| s101-v064 | S101 · 2025-03-20 | 282 / 30 / 33 / 5 | 282 / 30 / 33 / 5 | Sí 282 · No 30 · Abstención 33 · No vota 5 | **Sí** |

**3/3 cuadran exactamente**, tanto contra los totales oficiales del JSON como contra el recuento nominal diputado a diputado. Coincide además con la validación interna que el propio pipeline impone (falla si nominal ≠ totales). Cobertura de valores de `voto` observados: `Sí, No, Abstención, No vota` — coherente con la regla de catalogar valores reales antes de validar.

---

## Recomendación

**Carril 1: construir sobre la base open source CongresoAbierto, contribuyendo upstream.**

Justificación: (1) es el único candidato vivo, con commit de 2026-10-11, CI y 37 PRs fusionados; (2) cumple exactamente nuestra filosofía de trazabilidad —ingesta desde los JSON oficiales de `congreso.es/webpublica/opendata/votaciones/...` y validación dura del recuento nominal contra los totales oficiales, con aborto si no cuadran—, verificada en su código y reproducida por nosotros con 3/3 votaciones exactas; (3) licencias aptas: código MIT, datos CC BY 4.0, reutilizables con atribución; (4) la brecha que nos importa ya está en su hoja de ruta y es contribución natural: automatizar la descarga (hoy se pega un script en la consola del navegador día a día), ingestar comisiones y exponer el voto nominal en CSV/JSON público (hoy solo en los JSON del repo y la web). civis-api está muerto (>4 años, Heroku 404, CC BY-NC) y Reforma Digital bloquea todo acceso programático tras un checkpoint de Vercel y cubre ~5% de las votaciones. Nuestra validación propia (`make validar`) sigue siendo necesaria como segunda barrera independiente, pero no hay que reinventar la ingesta.

## Riesgos

- **Dependencia de una persona**: CongresoAbierto depende casi al 100% de MarcoAnarmo y tiene 1 mes de vida pública. Mitigación: consumir sus datos/JSON como fuente derivada (CC BY 4.0) sin acoplarnos a su infraestructura, y si el proyecto se estanca, nuestro pipeline puede regenerar los mismos artefactos desde el opendata oficial (la ruta está documentada en su propio `docs/metodologia.md`).
- **Su ingesta de votaciones es semimanual**: si nadie automatiza la descarga diaria, puede quedar desfasado; contribuir eso es prioritario y además prueba del carril 1.
- **Solo Pleno**: las comisiones no están ingestadas; si Revisora necesita comisiones, habrá que contribuir o extenderlo por nuestra cuenta.
- **CSV público de votaciones sin voto nominal**: el voto por diputado está en los JSON del repo y la web, no en el CSV; para nuestra trazabilidad conviene consumir `data/congreso/votaciones.json`/`pleno.jsonl` del repo y validar contra el JSON oficial, como ya hacemos.
- **Reforma Digital**: si en el futuro publica una API realmente accesible (sin checkpoint Vercel) y con licencia, podría reevaluarse como fuente secundaria; hoy, descartado.
