# Informe del ecosistema: holapolitica y quevotan (lote 01)

Fecha del análisis: **2026-11-22**. Analista: agente de sesión. Objetivo: el riesgo 4 del
plan obliga a analizar **Hola Política** y **Qué votan** antes de fijar el alcance del
buscador y las afinidades. Checklist del lote 00 (a–g): licencia, actividad, cobertura XV,
calidad/validación, datos/API, comunidad, riesgo de dependencia.

## Metodología

Fuentes y comandos usados (todos el 2026-11-22):

- Búsqueda web del ecosistema (consultas «holapolitica web España votaciones Congreso»
  y «quevotan España web qué votan partidos Congreso de los Diputados»).
- `webfetch https://www.holapolitica.org/about` y `https://github.com/Pardo24/holapolitica`
  (README completo: estado, arquitectura, principios, licencias).
- `webfetch https://quevotan.eu/` (portada: coberturas, últimas sesiones, fuente) y
  `https://codefloe.com/RazZziel/quevotan` (README completo: pipeline, fuentes,
  verificaciones, licencia).
- Índice oficial vivo: `curl -A "Mozilla/5.0 …" https://www.congreso.es/es/opendata/votaciones`
  → HTTP 200 (99.178 bytes); parseado del array `diasVotaciones` con Python:
  **147 días con votaciones**, del 19/09/2023 al **02/10/2026**.

---

## Ficha 1: Hola Política

Web: https://www.holapolitica.org · Código: https://github.com/Pardo24/holapolitica

**a) Licencia.** Código **EUPL-1.2**; datos **CC-BY 4.0**; contenidos editoriales
CC-BY-SA 4.0. Reutilizable con atribución.

**b) Actividad.** 901 commits, producción viva con ingesta automática cada 4 h. Mantenedor
único (Daniel Pardo, «solo project»), desarrollo asistido por IA (Claude) con revisión
humana declarada. Financiación: autofinanciado, con solicitudes de ayuda en marcha
(NLnet NGI Zero, Fundació Jaume Bofill, Goteo).

**c) Cobertura.** Fase 1 = Congreso XV en producción: ~1.840 votaciones, 430
iniciativas, 350 diputados activos con historial de grupo, 617.000 registros de voto
individual. En catalán/castellano/inglés. Fases futuras: Parlament de Catalunya y
Ayuntamiento de Barcelona.

**d) Calidad y validación.** Ingesta idempotente cada 4 h desde el opendata oficial;
clasificación de temas con Mistral Small (política explícita contra OpenAI/Gemini);
cruce con el BOE por la API consolidada oficial. Nuestra validación nominal-vs-totales
no se declara en el README (sí en quevotan); su acento está en agregados: cohesión,
asistencia, matrices de coalición.

**e) Datos/API.** **API pública** (api.holapolitica.org, docs en `/docs`), 5 widgets
incrustables para redacciones, boletín semanal (Listmonk), push, PWA, tarjetas sociales.
Stack vivo: FastAPI + PostgreSQL 16 + Redis + Next.js 15 (Hetzner + Vercel).

**f) Comunidad.** Repositorio público, CONTRIBUTING, 3 estrellas, 0 forks. Audiencia
declarada: periodistas, investigadores, activistas.

**g) Riesgo de dependencia.** Proyecto de una persona con infraestructura viva (BD,
workers, frontend). Para nosotros no es fuente de datos sino **referente de producto**;
no hay acoplamiento posible ni necesario.

**Principio rector (textual):** «Mirror, not megaphone». Sin reacciones, sin
comentarios, **sin votos paralelos** («¿cómo habrías votado?»), sin juicios de valor
editoriales; métricas agregadas bajo regla de simetría. Coincide con nuestra regla de
neutralidad de `docs/diseno.md`, excepto en lo del voto paralelo: nuestra apuesta
«Juego de coincidencias» es justo eso (aunque sin registro ni deliberación); cuando se
moldee habrá que diferenciarla con claridad.

---

## Ficha 2: Qué votan

Web: https://quevotan.eu · Código: https://codefloe.com/RazZziel/quevotan (Forja
CodeFloe/Forgejo)

**a) Licencia.** Código **AGPL-3.0** (la misma que la nuestra). Datos: del Congreso
(datos abiertos).

**b) Actividad.** 29 commits (primer commit 2026-10-06, último 2026-10-24). CI diaria
(05:00 UTC) que descarga lo nuevo, carga, clasifica, genera y publica el sitio estático;
los datos crudos viven en la rama `datos` (~10 MB empaquetados).

**c) Cobertura.** **La XV completa**: 2.189 votaciones (2.185 con voto nominal),
149 sesiones plenarias, 764.718 votos individuales, 412 diputados distintos, última
votación 02/10/2026. La XV está **disuelta** (Real Decreto 806/2026; elecciones el
29/11/2026): corpus cerrado.

**d) Calidad y validación.** **La misma regla que la nuestra, verificable en su
README**: `ingest` comprueba en cada votación que los votos individuales suman los
totales oficiales, que sesión/número/fecha cuadran con la página del día y que todo
voto se asocia a un diputado oficial; sale con código 1 si hay problemas. Además
`verifica_pdf.py` compara la base con el PDF oficial de una muestra aleatoria
(última ejecución: 25/25 idénticas) y `metrics` comprueba que la suma por formaciones
reproduce los totales. Tests con fixtures reales.

**e) Datos/API.** Sitio 100 % estático (Jinja2) servido por Pages (~90 MB, ~3.500
ficheros): votaciones, sesiones, grupos, formaciones, diputados (asistencia, disciplina,
cambios de grupo), temas, **posturas** («Limitar o contener el precio del alquiler»),
**afinidad** entre grupos, metodología y descarga en CSV. Sin API ni registro.

**f) Comunidad.** Proyecto personal (Ismael Barros²). Metodología pública y
extraordinariamente documentada (gold sets etiquetados a mano para temas y posturas,
comparación de modelos, huellas para regenerar solo lo que cambia, overrides manuales).

**g) Riesgo de dependencia.** Cero como fuente (no consumimos sus datos): su valor es
ser **tercer productor independiente** para contrastes y el referente técnico más
cercano a nuestro carril (mismo enfoque estático, misma licencia, misma validación).

**Hallazgos técnicos que nos afectan directamente:**
- **12 votaciones públicas por llamamiento** sin JSON nominal en la XV (investiduras,
  amnistía, reforma del art. 49 CE…): quevotan extrae los nombres del PDF del Diario de
  Sesiones y solo lo publica si cuadra con los totales. Nosotros las marcaremos «sin
  voto individual publicado» con enlace al Diario (decisión en `notas.md`); extraer el
  PDF queda fuera del lote.
- La descarga completa de la XV les cuesta ~2.900 peticiones y ~30 min con pausa
  educada: calibra nuestra B.2.
- CongresoAbierto declaraba 2.175 votaciones (ingesta semimanual, puede ir retrasado);
  quevotan, 2.189. Nuestra enumeración dirá la cifra definitiva (tarea B.3).

---

## Otros actores vistos (sin verificación profunda; solo hallazgos de búsqueda)

- **loquevotan.es**: «14.449 votaciones explicadas» y preguntas naturales por partido
  («¿Votó el PP a favor de subir pensiones?»).
- **elcongresoentumano.es**: «Parliament, made clear», fichas por partido.
- **CongresoAbierto**: ya auditado en el lote 00 (ADR-0005); sigue siendo el proyecto
  hermano al que contribuir.
- **Civio**: citado por Hola Política como infraestructura cívica complementaria.

Conclusión de ecosistema: la demanda está confirmada — al menos cuatro proyectos vivos
publican lo mismo desde la fuente oficial. Nadie compite por ser «la versión ciudadana»:
el hueco de vCiudadania sigue siendo castellano claro, trazabilidad estricta (cada
dato con su enlace, recuentos validados), minimalismo sin registro ni notificaciones.

## Verificación cruzada

| Hecho | Ecosistema | Nosotros (verificado) |
|---|---|---|
| Sesión 202 (30/09/2026) | quevotan: 21 votaciones, totales por votación (p. ej. PNL migración: 137/175/34) | Spike del lote 00: 21/21 validadas, mismos totales |
| Última votación de la XV | quevotan: 02/10/2026 (sesión 203, 2 votaciones) | Índice `diasVotaciones`: último día 2026-10-02 |
| Fuente | ambos: JSON oficiales de congreso.es | Mismo pipeline desde el lote 00 |

## Implicaciones para el buscador y las afinidades (lo que pedía el plan)

1. **Buscador:** ambos confirman el patrón del recorrido 1–3 (recientes + búsqueda +
   ficha). Mantenemos: índice estático filtrado en cliente (ADR-0002), sin widgets ni
   boletines. El diferencial es lo que ya fija `docs/diseno.md`: lenguaje ciudadano,
   glosario al pasar, un color neutro, fuente en cada ficha.
2. **Afinidades:** quevotan ya publica afinidad por grupo/formación y posturas
   valoradas con LLM verificado; Hola Política publica cohesión y matrices bajo
   simetría. La futura apuesta «Juego de coincidencias» no podrá diferenciarse por
   «hay afinidad» sino por la experiencia: sin registro, compartible, sobre votaciones
   reales citadas. Nota para cuando se moldee esa apuesta; este lote no toca
   afinidades.
3. **Textos generados con IA:** ambos usan Mistral con gold sets y comprobaciones —
   valida el enfoque de la apuesta «Resúmenes trazables» (extract → redact → verify +
   golden set). Este lote publica solo texto oficial + enlace.
4. **Colores por grupo:** quevotan los define (`data/grupos.yaml`); Hola Política usa
   hemiciclo gráfico. El ecosistema no zanja la cuestión de neutralidad: la decisión
   sigue siendo nuestra (ADR-0007, tarea A.2).
5. **Corpus cerrado:** la XV no recibe votaciones nuevas hasta la XVI → la ingesta de
   este lote es una descarga única completa, no un actualizador (decisión 1 del
   moldeo en `notas.md`).

## Recomendación

Mantener el carril propio (ADR-0005) sin cambios: fuente primaria oficial, validación
dura, estático. Con dos matices operativos: (1) usar a quevotan y CongresoAbierto como
**contraste de totales** cuando la B.3 valide la XV completa (tercera barrera
independiente); (2) reutilizar los **temas de CongresoAbierto** (CC BY 4.0) con
atribución y validación para el filtro por tema (ya decidido en el moldeo). Ni uno ni
otro cambian el alcance del lote: lo confirman y calibran.

## Riesgos

- **«Ya existe» como desánimo:** hay cuatro proyectos vivos. Contrapeso: ninguno es la
  versión ciudadana castellana con trazabilidad total; nuestro recorrido es más
  estrecho y más claro, y la apuesta sigue siendo publicable.
- **Quevotan converge con nuestra hoja de ruta** (dataset, metodología, XVI ya
  contemplada): el riesgo de quedar como copia exige mantener el diferencial de
  lenguaje claro y neutralidad estricta, y documentar los contrastes en `notas.md`.
- **La XVI llega el 29/11/2026:** si el lote no está cerrado, habrá tentación de
  ampliarlo. Regla: cerrar la XV como estaba planeado; la XVI es otra decisión (y la
  clave `--leg` del modelo de ADR-0003 ya lo permite).
