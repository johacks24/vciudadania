# Referencias — índice

Lo que guía el proyecto y de dónde sale cada principio. Los originales de terceros
(transcripciones, HTMLs guardados) viven en `_privado/` (no versionado); lo nuestro es
este índice y los destilados que hagamos.

| Referencia | Origen local | Principio que sacamos |
|---|---|---|
| *Shape Up* (Ryan Singer, Basecamp) — lectura gratuita en shapeup.com | `_privado/shape-up/` (transcripción MD por capítulos) | Moldear antes de construir: pitch con problema, apuesta, no-objetivos, conejos; lotes con "cuándo está hecho"; hills; cooldown |
| *Here's how I use LLMs to help me write code* + notas sobre codebases para agentes (Simon Willison) | — (web) | Tests que el agente pueda ejecutar; notas de arranque del dev server; errores con detalle; "no commiteo lo que no puedo explicar" |
| *My LLM codegen workflow atm* (Harper Reed) | — (web) | Bucles discretos: brief → plan → ejecutar; ficheros como memoria entre sesiones (plan.md/tareas.md) |
| *My AI Adoption Journey* (Mitchell Hashimoto) | — (web) | Harness engineering: cuando el agente falla, añadir una regla o una herramienta; revisión final "¿se me olvidó algo?" |
| *Agentic Coding Recommendations* (Armin Ronacher) | — (web) | Makefile como punto de entrada único; log combinado con tail; stack aburrido y estable |
| Sistema del vibe coder profesional (Lazar Jovanovic, Lenny's Podcast 2026-02-08) | — (web) | 80% planificar; 4 ficheros → plantilla de lote; orden permanente "lee los planes, ejecuta la siguiente tarea"; 4x4 de depuración; enseñar al agente tras cada fix |
| Guías anti-sobrecarga de Karpathy (Simplicity First, Surgical Changes, criterios verificables) | — (web) | Nada especulativo; cada línea trazable a la tarea; criterios de éxito verificables |
| *Plurality* y la práctica g0v/"fork the government" (Audrey Tang) | — (web) | Open by default; open data/API como infraestructura pública; transparencia radical del método y las correcciones |
| Es la hora de la verdad (eslahoradelaverdad.es) — referencia de producto y método | — (web) | Benchmark de producto; sus reglas de resumen y neutralidad (CC BY 4.0, citable) |
| CongresoAbierto (congresoabierto.org, MIT) · civis-api · API Reforma Digital | — (web) | Candidatos de la auditoría de base (ADR-0005) |

## Reglas de esta carpeta

1. Lo público son el índice y los destilados con palabras nuestras.
2. Los originales de terceros van a `_privado/` y no se commitean.
3. Cada nueva referencia entra con `/referencia <url>`: se convierte a Markdown, se
   guarda en `_privado/` y se añade aquí con el principio que sacamos de ella.
