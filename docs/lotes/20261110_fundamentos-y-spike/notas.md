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
  individuales; **diputados por grupo** (no votos): GP 137, GS 121, GSUMAR 26, GVOX 32,
  GMx 9, GR 7, GJxCAT 7, GEH Bildu 6, GV (EAJ-PNV) 5.
- **Votación 021 (suplicatorio):** solo totales (340 Sí, 0, 0, 10 No votan) — voto
  secreto, sin individuales. Confirma la categoría «sin voto individual publicado».
- **Índice de contraste:** `congresoabierto.org/datos/csv/votaciones.csv` (MIT) incluye
  `url_votacion` que apunta a los JSON oficiales — sirve de contraste, no de fuente.
- **Licencia AGPL-3.0:** texto completo descargado de gnu.org → `LICENSE`.

## Auditoría de base (scope A)

Hecha el 10/11/2026 → `informe-auditoria.md` (metodología, checklist a–g por candidato,
verificación cruzada 3/3). Decisión en `docs/decisiones/0005-sobre-que-construir.md`:
fuente primaria propia + contribución a CongresoAbierto (civis-api y Reforma Digital,
descartados con evidencia). Contraste cruzado adicional hecho en el spike: 21/21
votaciones de la sesión 202 coinciden entre el CSV de CongresoAbierto y el JSON oficial.

## Publicación del repo y desbloqueos (11/11/2026)

- **Repo público creado y empujado:** `github.com/johacks24/vciudadania` — 5
  confirmaciones, rama por defecto `main`, visibilidad pública (verificado vía API).
- **CI verde a la primera** → B.5 completa:
  https://github.com/johacks24/vciudadania/actions/runs/42938522655
- **Cadena de credenciales git (por qué el push no pidió token):** el terminal del
  editor (VSCodium) inyecta su sesión de GitHub vía `GIT_ASKPASS`; git guardó ese token
  en el llavero de macOS con usuario `90719580`, el ID numérico de la cuenta (verificado
  contra la API). El fallo previo («Invalid username or token») era un token caducado
  del mismo mecanismo, limpiado con `git credential reject`. El token fino
  (fine-grained) creado por el humano (permiso de código RW) quedó sin usar; B.6 lo
  adopta como credencial propia del proyecto.
- **Runbook de B.6 (migración al token fino), todo desde un Terminal normal (no el del
  editor, que inyecta su credencial):**
  1. `printf 'protocol=https\nhost=github.com\n' | git credential reject` — borra la
     credencial del editor del llavero.
  2. `git push` — pedirá credenciales: usuario `johacks24`, contraseña = el token fino
     (nunca la contraseña de la cuenta de GitHub).
  3. Verificar: `printf 'protocol=https\nhost=github.com\n\n' | git credential fill`
     debe devolver `username=johacks24` (ya no `90719580`).
  Al ejecutar B.6: anotar aquí la fecha de caducidad del token (se consulta en
  github.com/settings/personal-access-tokens).
- **Hallazgo para D.3:** la ficha enlaza el repo como `github.com/vciudadania` (no
  existe; vive en `congreso/congreso/exportar_ficha.py` ~línea 59); el real es
  `github.com/johacks24/vciudadania`. ADR-0006 ya preveía ajustar el enlace al fijar
  la URL.
- **Programado para el 12/11/2026:** B.6 · D.3 · D.2 (Pages en modo GitHub Actions; al
  cerrar D.2, la apuesta pasa a **producción** en `docs/apuestas.md`).
