# Lote 00 — Fundamentos + spike vertical

**Fechas:** 10/11/2026 → 11/11/2026 · **Tamaño:** ~1 semana · Estado vivo en `docs/apuestas.md`

## Problema

Cada lote futuro arrastra tres riesgos si este no cierra: construir sobre una base de
datos equivocada, publicar sin trazabilidad de fuente, y no tener el suelo de licencias
y método. Además, aún no hay prueba de que la cadena completa funcione.

## Apuesta

En una semana, la cadena completa andando con **una** votación real: Congreso → ingesta
→ validación 100 % → base de datos → ficha web **desplegada y pública**. Más la decisión
documentada de sobre qué construir (auditoría).

## No-objetivos

Web navegable con búsqueda · resúmenes con IA · juego · chat · comisiones · Senado ·
XIV legislatura · API documentada para terceros.

## Riesgos de desvío (rabbit holes)

1. **Bloqueos del Congreso** a clientes no-navegador (403 sin UA) — mitigado: UA de
   navegador verificado; si empeora, carril alternativo documentado en notas.
2. **Votaciones sin voto individual** (suplicatorios secretos, asentimiento) — regla:
   categoría explícita, no error.
3. **Auditoría no concluyente** — mitigado: timebox 2 h/candidato y carril 3 por defecto
   (pipeline propio desde fuente primaria).

## Recorridos de usuario (el "hecho" es el recorrido completo)

1. Abro la **URL pública** de la ficha.
2. Leo en lenguaje claro **qué se votó** (la pregunta del trámite).
3. Veo el **resultado y el recuento** (Sí / No / Abstención / No vota).
4. Veo **cómo votó cada grupo**.
5. Veo el **enlace a la fuente oficial** y puedo comprobarlo yo.

## Cuándo está hecho

- URL pública con la ficha cumpliendo los 5 pasos.
- `make ingesta && make validar` cuadra al 100 % la sesión 202 (30/09/2026).
- Repo con licencias, AGENTS.md, CI verde y ADR-0005 publicada.
- `docs/apuestas.md` con la apuesta «Pleno XV navegable» en investigación.
