# Informe: ecosistema de votaciones, deliberación e ILP

**Fecha:** 2026-11-10/11 · **Origen:** auditoría de base (`informe-auditoria.md`),
investigación web y comprobaciones de colisión de nombre.
**Alcance:** qué existe, qué naturaleza tiene, qué solapa con nuestro mapa y qué
heredamos. Alimenta las apuestas en consideración y el moldeo de «Pleno XV navegable».

## 1. Proyectos de votaciones del Congreso (España)

| Proyecto | Qué hace | Código / licencia | Estado | Solape con nuestro mapa | Qué heredamos |
|---|---|---|---|---|---|
| **CongresoAbierto** (congresoabierto.org) | Votaciones del Pleno XV: fichas, CSVs, hemiciclo | GitHub · **MIT** + datos CC BY 4.0 | Vivo (commit 2026-10-11), 1 persona | Datos y CSVs | **Nuestra base (ADR-0005)**: su importador consume los JSON oficiales y aborta si el recuento nominal no cuadra |
| **holapolitica.org** | Registro de votos: ingesta cada 4 h, clasificación temática (Mistral), widgets, boletín, quiz cívico en `/joc`. Visión multicámara (Congreso → Parlament → Ajuntament BCN) | GitHub · **EUPL-1.2** + datos CC BY + editorial CC BY-SA | Producción, 1 persona | Quiz (nuestro lote de juego), clasificación temática, visión multicámara | Arquitectura de plataforma mantenible por una persona; solape con el juego → **análisis profundo antes de moldear «Pleno XV navegable»** |
| **quevotan.eu** | Sitio estático: qué significa votar sí/no, posturas por tema, afinidad entre grupos, disciplina/asistencia, CSVs | CodeFloe (Forgejo) · **AGPL-3.0** | Producción, 1 persona | Afinidades (lote de juego), significado del voto | Su tratamiento del «qué significa votar sí» (mejor que un título legal); extrae votos de Diario de Sesiones para votaciones por llamamiento |
| **votoenclaro.es** | Votaciones + banco de preguntas explicadas + test «qué partido vota como tú» | Web · datos CC **BY-NC** · código PolyForm NC (no open source) | Producción, 1 persona | Test (lote de juego), resúmenes | **Benchmark metodológico**: su verificador determinista (una pregunta solo se publica si cada cita aparece literal en el documento oficial) es nuestro pipeline «verify», en producción |
| **quienvota.org** | Registro con **huella SHA-256 de cada fichero oficial** y fecha de consulta; CSV descargable | Por confirmar (repo no localizado) | Producción | Datos | Su idea de hash por fichero: la copiaremos para `sources.yaml` |
| **eslahoradelaverdad.es** | Fichas, test, resúmenes IA, 4 idiomas, MCP | Cerrado · contenido CC BY 4.0 | Producción | Todo el mapa | Benchmark de producto y método (ya adoptado en `docs/metodo`) |
| **congreso-scrapper** | Scraper del Congreso, incompleto | GitHub · MIT | Parado (2023) | Ingesta | Marginal |

**Lectura:** el nicho está poblado (7+ proyectos solo en votaciones del Congreso).
Nuestros diferenciales en pie: **validación dura + trazabilidad frase→fuente + juego +
chat de evolución + (futuro) co-creación con continuidad**. La diferenciación ya no es
opcional: decidida en ADR-0005 (fuente primaria propia + contribución a CongresoAbierto).

## 2. Deliberación y co-creación (apuesta «Co-creación ciudadana de normas»)

| Plataforma | Qué hace | Licencia | Estado | Qué heredamos |
|---|---|---|---|---|
| **Polis** (compdemocracy.org) | Escucha a escala: sin botón de respuesta (sin flame war), clustering de posturas y **argumentos-puente** destacados | **AGPL** (self-hosteable) | Mantenido por Computational Democracy Project | El motor de consenso; **no consta uso institucional en España → espacio libre**; complementa a Decidim (no compite) |
| **DemocracyOS / Leyes Abiertas** (Democracia en Red, Argentina) | Co-redacción: diputados abren anteproyectos, la ciudadanía comenta por secciones, **versiones** y colaboradores acreditados | **GPL-3** | Producción (Cámara argentina, 2018-21: 62 anteproyectos, 1.326 aportes) | El modelo de co-redacción con versiones — exactamente la pieza «co-redactar» de la apuesta |
| **Decidim** (Barcelona) / **Consul** (Madrid) | Plataformas institucionales de participación | AGPL ambas | Producción en muchos ayuntamientos | Integración futura; no reinventar procesos |
| **Gobierto** (Populate) | Transparencia municipal: presupuestos, agendas, personas | AGPL · empresa activa | Producción | Fase ayuntamientos: aliado/plataforma |
| **e-cidadania** (cooperativa gallega) | Plataforma de e-democracia | Apache 2.0 | **Abandonada (~2013)** | Recordatorio: proyectos mueren sin mantenimiento — por eso lotes estrechos y base estable |

## 3. ILP y canales de retorno

- **Boreal (boreal.es)**: plataforma sin ánimo de lucro end-to-end para ILPs — creación,
  guía, **firmas con certificado digital o hoja sellada**, admisión. Activa: la ILP
  veterinaria (CEVE) cruzó las 500.000 firmas esta misma semana (10-11/2026).
- **La ILP es el canal legal de merge back en España**: es la pieza que a la
  constitución islandesa le faltó (ver §4). Nuestra diferenciación frente a Boreal: no
  competimos en firmas; añadimos **co-redacción** (Leyes Abiertas), **continuidad en el
  Pleno** (nuestra capa de trazabilidad: qué pasó con tu ILP cuando llegó al hemiciclo)
  y **presión ciudadana en su consideración**.

## 4. Casos de referencia internacional

- **vTaiwan / Polis**: 28 temas deliberados, **80 % acabaron en acción legislativa**.
  Claves: funcionarios participantes **con mandato de responder** («Participation
  Officers») y el *merge back* institucional. Finlandia es el otro uso nacional.
- **Constitución islandesa (2011-13)**: redacción crowdsourced en wiki con éxito y
  referéndum favorable (~2/3); **falló la adopción** porque el Parlamento, sin mecanismo
  que le obligara a fusionar, archivó el texto. **Lección: el cuello de botella nunca es
  la multitud redactando; es el canal de retorno.** Diseñar el merge back desde el día 1.
- **unitedstates/congress** (EE. UU.): el estándar de recolector comunitario de datos del
  Congreso (CC0, comunidad desde 2013). Modelo para nuestra apuesta «API pública v1».

## 5. Conclusiones para vCiudadania

1. Construir sobre lo existente (ADR-0005): fuente primaria propia + contribución a
   CongresoAbierto; reutilizar modelos de Polis/Leyes Abiertas cuando llegue la apuesta
   de co-creación.
2. Pendiente de análisis profundo (timebox 2-3 h por proyecto, checklist de la
   auditoría): **holapolitica** y **quevotan** — primera tarea del moldeo de «Pleno XV
   navegable», porque puede mover su alcance (quiz, afinidades, multicámara).
3. La apuesta de co-creación tiene predecesores por pieza: firmas → Boreal; consenso →
   Polis; co-redacción → Leyes Abiertas; continuidad en el Pleno → **nadie la tiene hoy:
   es nuestra pieza** (y es literalmente el core del proyecto: trazabilidad).

## 6. Preguntas de diseño abiertas (apuesta de co-creación, no decidir aún)

- **Validación de expertxs/organizaciones de confianza**: ¿reputación tipo PageRank de
  personas (riesgos: sybil, popularidad ≠ competencia, captura), mecanismos de
  prueba-de-persona/delegación de Vitalik Buterin, o atestación plural y
  argumentos-puente de Plurality (Tang)?
- ¿Qué incluye el «merge back» español exactamente: ILP (canal legal), enmiendas
  presentadas por grupos, preguntas orales?
