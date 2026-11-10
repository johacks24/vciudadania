# Aprender — registro público de aprendizajes del proyecto

Lecciones sobre datos, producto y fuentes (las lecciones operativas para agentes van en
`AGENTS.md`). Una entrada por aprendizaje: fecha, qué pasó, qué aprendimos.

## 2026-11-10 · Planificación

- Los lotes deben ser **verticales pero estrechos**: una votación publicada vale más que
  diez a medias. Lo confirmó el diseño del lote 00.
- Del sistema de Lazar Jovanovic adoptamos: 4 ficheros comprimidos en plantilla de lote
  (plan.md + tareas.md + diseno.md transversal), la orden permanente `/siguiente`, el 4x4
  de depuración y el peldaño 5 (enseñar al agente). Descartamos master_plan global
  (lo hace apuestas.md) y prototipos paralelos salvo para diseño visual.
- El error de OpenRouter del día 1 fue una credencial con la clave duplicada separada por
  un salto de línea: los headers HTTP no perdonan saltos de línea. Lección operativa
  también en `.env.example`.

## 2026-11-10 · Datos del Congreso (verificado en el spike)

- La página de datos abiertos (`congreso.es/es/opendata/votaciones?targetDate=DD/MM/AAAA`)
  lista los JSON por votación, pero **bloquea peticiones sin user-agent de navegador**
  (403). Con UA funciona. Anotado para el cliente HTTP.
- El JSON oficial por votación tiene: `informacion` (sesión, número, fecha, título,
  textoExpediente), `totales` (asentimiento, presentes, afavor, enContra, abstenciones,
  noVotan) y `votaciones` (voto individual: asiento, diputado, grupo, voto).
- No todas las votaciones publican voto individual: los **suplicatorios** se votan en
  secreto (solo totales) y las de **asentimiento** no tienen votación nominal. Regla:
  «sin voto individual publicado» es una categoría, no un error.
- Los grupos llegan codificados (GP, GS, GVOX, GMx…): hace falta tabla de mapeo a nombres.
- El CSV de CongresoAbierto sirve como índice de contraste, pero la enumeración desde la
  fuente primaria funciona: no dependemos de terceros.

## 2026-11-10 · Auditoría de base (ADR-0005)

- **civis-api está muerto** (>4 años sin commits, Heroku 404, sin LICENSE, CC BY-NC):
  descartado. **Reforma Digital bloquea todo acceso programático** (429 + checkpoint
  JS/WASM de Vercel en todos los endpoints) y cubre ~5 % del Pleno: descartada.
- **CongresoAbierto es el único candidato vivo** (commit 2026-10-11, MIT + CC BY 4.0,
  CI con 8 ficheros de tests) y su filosofía coincide con la nuestra: consume los JSON
  oficiales y **aborta si el recuento nominal no cuadra con los totales** — la misma
  regla que implementamos hoy de forma independiente.
- La ingesta de CongresoAbierto es semimanual (script pegado a mano en la consola del
  navegador): automatizarla es su issue de hoja de ruta y nuestra contribución natural.
- Decisión: fuente primaria propia + contribuciones upstream (ADR-0005). Sin acoplarse
  a su infraestructura: si se estanca, nuestro pipeline regenera todo desde el opendata.
