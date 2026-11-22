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
