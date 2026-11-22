# Notas — Lote 01 (Pleno XV navegable)

## 22/11/2026 · Moldeo: verificaciones previas y decisiones de «cómo»

Verificaciones contra fuentes (comandos exactos en `informe-ecosistema.md`):

- **El opendata sigue vivo:** `congreso.es/es/opendata/votaciones` responde HTTP 200 con
  user-agent de navegador y trae el índice `diasVotaciones` con **147 días con
  votaciones** en la XV: del 19/09/2023 al **02/10/2026** (última votación).
- **La XV es un corpus cerrado:** disuelta el 06/10/2026 (Real Decreto 806/2026;
  elecciones el 29/11/2026, BOE-A-2026-20742). No entran votaciones nuevas hasta la
  XVI. Magnitudes de contraste (quevotan.eu, verificadas): 2.189 votaciones
  (2.185 con voto nominal), 149 sesiones plenarias, 764.718 votos individuales,
  412 diputados distintos (altas/bajas).
- **La sesión 202 del spike cuadra con el ecosistema:** quevotan lista las mismas
  21 votaciones del 30/09/2026 que validamos en el lote 00, y su última sesión (203,
  02/10/2026, 2 votaciones) coincide con el último día del índice oficial.

Decisiones de diseño tomadas al moldear (los «cómo» quedan resueltos; ninguna tarea
arranca «En exploración»):

1. **Corpus cerrado → ingesta única:** la XV completa se descarga y valida de una vez;
   sin actualización periódica hasta que exista XVI. Refuerza ADR-0002 (estático por
   lotes) y simplifica la CI.
2. **Búsqueda por palabra en sitio estático:** índice JSON compacto (id, fecha,
   título, resultado, tema) que el navegador filtra en cliente. Sin servidor ni
   buscador externo; coherente con ADR-0002 y con el diseño móvil primero.
3. **Filtro por tema:** se reutiliza la asignación de temas de CongresoAbierto
   (`data/manual/temas.json`, CC BY 4.0) **con atribución y validación nuestra**
   (ADR-0005, punto 3: fuente secundaria jamás sin contrastar). Nada de clasificación
   con IA en este lote (eso es la apuesta «Resúmenes trazables», fuera de alcance).
4. **Categorías sin voto individual:** suplicatorios (secreto; solo totales) y
   **públicas por llamamiento** (12 en la XV: investiduras, amnistía, reforma del
   art. 49 CE…): se marcan «sin voto individual publicado» con enlace al Diario de
   Sesiones. Extraer los nombres del PDF del Diario (como hace quevotan) queda
   **fuera** del lote: mejora futura, no ampliación.
5. **Diputados:** tabla propia desde la exportación del buscador oficial de diputados
   (altas/bajas, formación, grupo), esquema pydantic antes que el código (regla de
   AGENTS.md); el modelo no supone una sola legislatura (ADR-0003).
6. **Tamaño fijado:** ~2 semanas. Justificación: corpus cerrado (sin carga periódica),
   pipeline validado y generador de ficha ya existentes del lote 00; queda escalar la
   ingesta (147 días), el buscador estático, el dataset y el despliegue.

La apuesta pasa a **desarrollo** en `docs/apuestas.md` (única fuente de verdad del
estado). El análisis previo obligatorio del plan (riesgo 4) se ejecuta como tarea A.1
→ `informe-ecosistema.md`.

## 22/11/2026 · A.1 completada: informe del ecosistema

- Ambos proyectos analizados con el checklist del lote 00 y verificación cruzada
  (sesión 202 y última votación cuadran con nuestro spike y con el índice oficial).
  Detalle y evidencias en `informe-ecosistema.md`.
- Conclusiones operativas: el alcance del lote **no cambia**; quevotan y
  CongresoAbierto servirán como contraste de totales en B.3; los temas de
  CongresoAbierto alimentan el filtro por tema (C.3) con atribución y validación;
  la XVI (post 29/11/2026) no entra en este lote.

## 22/11/2026 · Dirección de diseño del humano + A.2 (ADR-0007)

El humano dirigió el diseño del recuento visual antes de ejecutar A.2 (quedó en
`docs/decisiones/0007-color-grupos.md` y en `docs/diseno.md`):

- **Neutralidad ≠ ocultar datos:** mostrar qué votó cada grupo es un dato; la pregunta
  del color no es ideológica sino funcional: ¿en qué interfaz trabaja?
- **Recuento visual = waffle aprobado:** una celda por diputado, color de grupo, voto
  por posición (secciones). Descartadas las codificaciones de doble canal por celda
  (contorno de voto o barra en mitades): ilegibles a ~12 px y doblan el problema
  daltónico. Sin siglas dentro de las celdas (ilegibles); leyenda + orden fijo +
  detalle a demanda.
- **Listado sin paginación:** carga automática al llegar al final de la página
  (scroll infinito) sobre el índice JSON de C.2; los primeros N sin JavaScript.
- **Sin hemiciclo literal:** el campo `asiento` se conserva en los datos (fidelidad a
  la fuente) pero no se muestra. «Lo que me interesa es qué votó cada grupo y cómo
  acordaron» — el waffle ordena por sentido del voto y por grupo, y hace visible la
  disciplina (bloque unido = grupo unido).
- **Paleta (evidencia del método):** base `grupos.yaml` de quevotan (AGPL-3.0, misma
  licencia); comprobación WCAG de contraste sobre blanco con la fórmula de luminancia
  relativa; 4 colores cumplen ≥ 3:1 tal cual y 5 se oscurecen por matiz hasta
  cumplirlo (Vox, ERC, Junts, EH Bildu, Mixto). Limitación declarada en la ADR: la
  luminancia no separa todos los pares para daltonía (Junts/EH Bildu ≈ 0.29), así que
  la garantía es la redundancia (posición + leyenda + texto), no la paleta.

A.2 completada; C.1 y C.4 actualizadas con esta dirección.

## 22/11/2026 · B.1 completada: enumeración por legislatura

Qué se construyó (commits «Lote 01: B.1 …»):

- **Cliente:** `pagina_indice` + `dias_votaciones(leg)` leen el índice del opendata
  (`?targetLegislatura=XV`), que publica `var diasVotaciones = [20230919, …]` con
  **enteros**, no claves JSON. Verificado en vivo: **XV = 147 días**
  (19/09/2023 → 02/10/2026); XIV = 170 (el parámetro discrimina legislaturas).
- **Sesión y fecha desde la URL:** la URL oficial ya trae
  `Leg15/Sesion202/20260930/…`, así que `sesion_y_fecha_de_url` las extrae y la
  ingesta ya no necesita `--sesion`: el almacenamiento es idéntico al del lote 00
  (`data/raw/LegXV/Sesion{n}/{fecha}/VotacionNNN/VOT_*.json`), sin rupturas para
  `validar`/`exportar`.
- **Modo legislatura:** `congreso ingesta --legislatura XV` (sin `--fecha`) recorre los
  147 días; **pausa educada de 0,5 s** entre descargas (como quevotan); los días sin
  JSON **no** son error en este modo. `--fecha` mantiene el modo día del lote 00.
- **Makefile:** `make ingesta` (día de prueba) sin `--sesion`; nuevo
  `make ingesta-legislatura` (XV completa) — B.2 lo ejecutará.

Evidencias de la verificación (22/11/2026):

- `make test`: **9/9** (4 del lote 00 + 5 nuevos sin red, con fixtures recortados de
  las páginas reales: `indice_opendata.html` y `dia_llamamiento.html`).
- `make ingesta` sobre la sesión 202 ya descargada: 0 ficheros nuevos, mismo layout
  (idempotencia). `make validar` sin regresión: 21 votaciones, 0 descuadres.
- `dias_votaciones("XV")` en vivo: 147 días.
- **Sesión 203 (02/10/2026):** sus 2 votaciones (RDL 26/2026 y 27/2026) son públicas
  por llamamiento y **no publican JSON por votación** — solo un ZIP por sesión
  (`VOT_20261002180000.zip`), que no usamos. En modo día devuelve código 1 con
  mensaje explicando ambos casos (fecha errónea o día de solo llamamiento); en modo
  legislatura, continúa. Esto anticipa que la cuenta de JSON de B.2 será ~2.175
  (lo de CongresoAbierto), no 2.189: la diferencia son las 12 de llamamiento, y el
  contraste exacto es tarea de B.3.

