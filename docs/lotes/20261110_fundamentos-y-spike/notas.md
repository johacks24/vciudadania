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
  cerrar D.2, la apuesta pasa a **producción** en `docs/apuestas.md`). Las tres
  adelantadas y completadas el 11/11 (abajo).

## B.6 completada: credencial propia del proyecto (11/11/2026)

- **Estado verificado:** el llavero guarda el token fino con cuenta `johacks24`; la
  credencial del editor (`90719580`) está borrada. Comprobado con
  `security find-internet-password` (solo queda la cuenta `johacks24`) y
  `git credential fill` → `username=johacks24`.
- **Caducidad del token fino:** martes **9/2/2027** (90 días). Renovar antes: generar
  otro fine-grained (solo repo `vciudadania`, permiso Contents: Read and write) en
  github.com/settings/personal-access-tokens y repetir el runbook de abajo. Ventana de
  renovación: a partir del 12/1/2027.
- **Primera vuelta fallida (4x4 nº 5, lección en AGENTS.md):** los comandos se
  ejecutaron en el terminal de VSCodium; su `GIT_ASKPASS` inyectó la sesión del editor,
  el `git push` autenticó en silencio con `90719580` y el llavero la volvió a guardar.
  Síntoma: el push «funcionaba» sin pedir credenciales y `git credential fill` seguía
  devolviendo `90719580`.
- **Runbook corregido (verifica cada peldaño):**
  1. `printf 'protocol=https\nhost=github.com\n' | git credential reject`
  2. Verificar: `security find-internet-password -s github.com` → «could not be found».
     Si sigue apareciendo: `security delete-internet-password -s github.com >/dev/null`
     y repetir la verificación.
  3. `env -u GIT_ASKPASS git push` → pide credenciales: usuario `johacks24`,
     contraseña = el token fino (permitir el acceso al llavero si macOS lo pide).
  4. Verificar: `security find-internet-password -s github.com -a johacks24` y
     `git credential fill` → `username=johacks24`.
- Con la credencial propia en el llavero, los pushes ya no consultan el `GIT_ASKPASS`
  del editor (solo entraría en juego si el llavero no respondiera).

## D.2 completada: ficha pública en GitHub Pages (11/11/2026)

- **URL pública:** `https://johacks24.github.io/vciudadania/` — verificada: HTTP 200,
  21 votaciones, 20 tablas por grupo, 1 nota de «votación no nominal» (suplicatorio),
  21 enlaces «Fuente oficial» y el enlace al método corregido (D.3).
- **Workflows en verde:** «Paginas» (completed/success) y CI (completed/success).
- **Hueco encontrado en el token fino:** el push del workflow fue rechazado
  («refusing to allow a Personal Access Token to create or update workflow … without
  `workflow` scope»): el permiso Contents RW no basta para crear workflows. Resuelto
  añadiendo **Workflows: Read and write** al token en
  github.com/settings/personal-access-tokens. **El token del proyecto necesita
  Contents RW + Workflows RW.** Editar los permisos no cambia el valor del token: el
  llavero no se tocó.
- Reparto del día: activar Pages y los permisos del token, el humano (en GitHub);
  código, workflow, push y verificación, el agente.
