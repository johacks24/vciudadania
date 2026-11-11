# Referencias — índice

Lo que guía el proyecto y de dónde sale cada principio. Los originales de terceros
(transcripciones, HTMLs guardados) viven en `_privado/` (no versionado); lo nuestro es
este índice y los destilados que hagamos.

| Referencia | Origen local | Principio que sacamos |
|---|---|---|
| *Shape Up* (Ryan Singer, Basecamp) — lectura gratuita en shapeup.com | `_privado/shape-up/` (transcripción MD por capítulos) | Moldear antes de construir: pitch con problema, apuesta, no-objetivos, riesgos de desvío; "cuándo está hecho"; tareas por resolver/resueltas; cooldown |
| *Here's how I use LLMs to help me write code* + notas sobre codebases para agentes (Simon Willison) | — (web) | Tests que el agente pueda ejecutar; notas de arranque del dev server; errores con detalle; "no commiteo lo que no puedo explicar" |
| *My LLM codegen workflow atm* (Harper Reed) | — (web) | Bucles discretos: brief → plan → ejecutar; ficheros como memoria entre sesiones (plan.md/tareas.md) |
| *My AI Adoption Journey* (Mitchell Hashimoto) | — (web) | Harness engineering: cuando el agente falla, añadir una regla o una herramienta; revisión final "¿se me olvidó algo?" |
| *Agentic Coding Recommendations* (Armin Ronacher) | — (web) | Makefile como punto de entrada único; log combinado con tail; stack aburrido y estable |
| Sistema del vibe coder profesional (Lazar Jovanovic, Lenny's Podcast 2026-02-08) | — (web) | 80% planificar; 4 ficheros → plantilla de lote; orden permanente "lee los planes, ejecuta la siguiente tarea"; 4x4 de depuración; enseñar al agente tras cada fix |
| Guías anti-sobrecarga de Karpathy (Simplicity First, Surgical Changes, criterios verificables) | — (web) | Nada especulativo; cada línea trazable a la tarea; criterios de éxito verificables |
| *Plurality* y la práctica g0v/"fork the government" (Audrey Tang) | — (web) | Open by default; open data/API como infraestructura pública; transparencia radical del método y las correcciones |
| Es la hora de la verdad (eslahoradelaverdad.es) — referencia de producto y método | — (web) | Benchmark de producto; sus reglas de resumen y neutralidad (CC BY 4.0, citable) |
| CongresoAbierto (congresoabierto.org) · civis-api · API Reforma Digital | `informe-auditoria` del lote de fundamentos | Candidatos de la auditoría de base (ADR-0005: fuente primaria propia + contribución a CongresoAbierto) |
| holapolitica.org (EUPL) | `informe-ecosistema-votaciones` | Plataforma cívica mantenible por una sola persona: ingesta idempotente, multicámara, quiz — análisis profundo pendiente |
| quevotan.eu (AGPL, CodeFloe/Forgejo) | `informe-ecosistema-votaciones` | Sitio estático + «qué significa votar sí/no»; el precedente de Codeberg en producción |
| votoenclaro.es (datos CC BY-NC) | `informe-ecosistema-votaciones` | El verificador determinista: una pregunta solo se publica si cada cita aparece literal en el documento oficial |
| quienvota.org | `informe-ecosistema-votaciones` | Huella SHA-256 por fichero oficial + fecha de consulta: copiar para `sources.yaml` |
| Boreal (boreal.es) | `informe-ecosistema-votaciones` | La ILP como canal legal de retorno (merge back): firmas → admisión → Pleno |
| Polis (compdemocracy.org, AGPL) | `informe-ecosistema-votaciones` | Consenso sin botón de respuesta; argumentos-puente; vTaiwan: 80 % de temas → acción legislativa |
| DemocracyOS / Leyes Abiertas (GPL-3) | `informe-ecosistema-votaciones` | Co-redacción de normas con versiones y colaboradores acreditados |
| Decidim (AGPL) · Consul (AGPL) | `informe-ecosistema-votaciones` | Participación institucional en España: integrar, no reinventar |
| Gobierto (Populate, AGPL) | `informe-ecosistema-votaciones` | Fase ayuntamientos: infraestructura municipal existente |
| e-cidadania (Apache 2.0, abandonada ~2013) | `informe-ecosistema-votaciones` | Los proyectos mueren sin mantenimiento: por eso lotes estrechos y base estable |
| unitedstates/congress (CC0) | `informe-ecosistema-votaciones` | El estándar de recolector comunitario: modelo para la API pública v1 |

## Reglas de esta carpeta

1. Lo público son el índice y los destilados con palabras nuestras.
2. Los originales de terceros van a `_privado/` y no se commitean.
3. Cada nueva referencia entra con `/referencia <url>`: se convierte a Markdown, se
   guarda en `_privado/` y se añade aquí con el principio que sacamos de ella.
