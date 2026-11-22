# ADR-0007: Color de los grupos parlamentarios — solo en el recuento visual

**Fecha:** 2026-11-22 · **Estado:** aceptada
**Dirección de diseño del humano:** sesión del 22/11/2026, registrada en
`docs/lotes/20261110_pleno-xv-navegable/notas.md`. Contexto del ecosistema en
`docs/lotes/20261110_pleno-xv-navegable/informe-ecosistema.md`.

## Contexto

El plan del lote 01 (riesgo 2) dejaba pendiente decidir si la web usa color por grupo
parlamentario: eslahoradelaverdad lo evita por neutralidad; quevotan y Hola Política lo
usan siendo neutrales. El humano fijó el criterio que zanja el debate: **la neutralidad
es minimizar el sesgo, no ocultar datos** — mostrar qué votó cada grupo es un dato, y
el color no es en sí una valoración. La pregunta correcta es funcional: ¿en qué
interfaz hace trabajo el color? En el lote 01, solo en una: el recuento visual de la
ficha, una vista simplificada del pleno (una celda por diputado). En el listado, las
tablas y el dataset, el texto ya identifica y el color no aporta nada.

## Decisión

1. **Sí al color por grupo, solo en el recuento visual de la ficha** (tarea C.4):
   cuadrícula (waffle) con una celda por diputado con voto nominal; el relleno de la
   celda es el color del grupo.
2. **El sentido del voto se codifica por posición, no por color**: la cuadrícula se
   divide en secciones — Sí / No / Abstención / No vota —, cada una con cabecera con
   el color de sentido ya definido en `docs/diseno.md` más su número. Dentro de cada
   sección, bloques por grupo ordenados por nº de diputados del grupo en esa votación
   (igual que la tabla «voto por grupo» de debajo); el Grupo Mixto siempre al final.
   Así se responde de un vistazo a «qué votó cada grupo y cómo acordaron»: un grupo
   unido es un bloque único en una sección; un grupo dividido, su color picado en
   varias.
3. **El color nunca es el único canal** (accesibilidad): leyenda chip + sigla + nombre
   bajo el gráfico; orden de bloques fijo y aprendible; alternativa textual en cada
   celda (`title`/`aria-label`: «Nombre (Grupo): voto»); y la tabla «voto por grupo»
   conserva todo en texto. Una persona daltónica pierde matices de matiz, no datos:
   el voto se lee por secciones y el grupo por orden y leyenda.
4. **Paleta con contraste ≥ 3:1 sobre blanco** (WCAG 1.4.11, objetos gráficos). Base
   documentada: `grupos.yaml` de quevotan (AGPL-3.0, nuestra misma licencia);
   oscurecida por matiz —luminosidad HSL a la baja hasta cumplir— cuando no llegaba
   (fórmula de luminancia relativa WCAG; ver tabla). **Limitación declarada:** la
   luminancia no separa todos los pares para daltonía (p. ej. Junts y EH Bildu quedan
   en ~0.29) y no se puede separar el abanico completo manteniendo matices
   reconocibles; la garantía es la regla 3 (redundancia), no la paleta.
5. **Sin siglas dentro de las celdas**: ilegibles a ~12 px y ruido visual; la sigla
   vive en la leyenda y el detalle por diputado aparece a demanda (title/aria-label).
6. **Sin hemiciclo literal**: el campo `asiento` de la fuente se conserva en los datos
   (fidelidad a la fuente) pero no se pinta. El waffle ordena por sentido del voto y
   por grupo: es la representación mínima del pleno. Si algún día se quisiera el
   hemiciclo real, ADR nueva que sustituya a esta.
7. **Votaciones sin voto individual publicado** (suplicatorios secretos, 12 públicas
   por llamamiento en la XV): sin waffle; solo totales, como ya hace el lote 00.

## Paleta

| Grupo | Sigla | Color | Fuente | Contraste s/ blanco |
|---|---|---|---|---|
| GP | PP | `#1d84ce` | quevotan | 4.00 |
| GS | PSOE | `#e30613` | quevotan | 4.88 |
| GVOX | Vox | `#4fa82e` | quevotan (`#5ac035`) oscurecido | 3.01 |
| GSUMAR | Sumar | `#e51c55` | quevotan | 4.54 |
| GR | ERC | `#d08200` | quevotan (`#ffb232`) oscurecido | 3.05 |
| GJxCAT | Junts | `#00a496` | quevotan (`#00c3b2`) oscurecido | 3.11 |
| GEH Bildu | EH Bildu | `#849c13` | quevotan (`#a7c518`) oscurecido | 3.11 |
| GV (EAJ-PNV) | PNV | `#2e7d32` | quevotan | 5.13 |
| GMx | Mixto | `#949494` | quevotan (`#9e9e9e`) oscurecido | 3.03 |

Si la ingesta de la XV (B.1–B.3) descubre grupos sin color, se añaden con estas mismas
reglas: matiz de convención contrastada + oscurecido a ≥ 3:1 + registro en esta tabla.

## Consecuencias

- **Ganamos:** el pleno de un vistazo y la disciplina de grupo visible sin leer
  números; el color deja de ser un debate ideológico y queda acotado a donde informa.
- **Renunciamos a:** el hemiciclo literal (posición de asiento) y a la doble
  codificación por celda (relleno + contorno, o mitades voto/grupo), ilegible a ~12 px
  y con doble canal de color, que es justo lo que colapsa para daltónicos.
- `docs/diseno.md` sustituye su regla provisional («un solo color neutro») por las
  reglas operativas de esta ADR.
- La decisión es de diseño de producto, no de neutralidad: mostrar el dato del grupo
  ya era parte del recorrido; el color solo lo hace más rápido de leer.
