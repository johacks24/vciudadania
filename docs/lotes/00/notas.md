# Notas — Lote 00

## Verificaciones previas (10/11/2026, durante el moldeo)

- **Fuente primaria accesible:** los JSON por votación responden 200 con user-agent de
  navegador. Ejemplo validado (sesión 202, votación 010):
  `https://www.congreso.es/webpublica/opendata/votaciones/Leg15/Sesion202/20260930/Votacion010/VOT_20260930153609.json`
- **Estructura del JSON oficial:**
  - `informacion`: sesion, numeroVotacion, fecha, titulo, textoExpediente, tituloSubGrupo, textoSubGrupo, votacionesConjuntas
  - `totales`: asentimiento (Sí/No), presentes, afavor, enContra, abstenciones, noVotan
  - `votaciones`: lista por diputado — {asiento, diputado, grupo, voto}
- **Enumeración:** la página `congreso.es/es/opendata/votaciones?targetDate=30/09/2026&targetLegislatura=XV`
  lista los 21 JSON de la sesión 202 (requiere UA navegador; sin él, 403).
- **Votación 010 (muestra):** 346 presentes, 34 Sí, 312 No, 0 Abst, 4 No votan; 350 votos
  individuales; grupos: GP 137, GS 121, GSUMAR 26, GVOX 32, GMx 9, GR 7, GJxCAT 7,
  GEH Bildu 6, GV (EAJ-PNV) 5.
- **Votación 021 (suplicatorio):** solo totales (340 Sí, 0, 0, 10 No votan) — voto
  secreto, sin individuales. Confirma la categoría «sin voto individual publicado».
- **Índice de contraste:** `congresoabierto.org/datos/csv/votaciones.csv` (MIT) incluye
  `url_votacion` que apunta a los JSON oficiales — sirve de contraste, no de fuente.
- **Licencia AGPL-3.0:** texto completo descargado de gnu.org → `LICENSE`.

## Auditoría de base (scope A)

Ver `notas-auditoria.md` (se genera con la auditoría) → decisión en
`docs/decisiones/0005-sobre-que-construir.md`.
