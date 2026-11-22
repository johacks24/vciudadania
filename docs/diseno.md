# Diseño — guías transversales (v0)

Lo que Lazar llama "design guidelines": sin esto, la IA se pone "sobrecreativa" y cada
pantalla sale distinta. Estas reglas aplican a todo lo visual del proyecto.

## Principios

1. **Minimalista y legible**: tipografía de sistema, mucho aire, cero adorno. Si un
   elemento no responde a una de las 5 preguntas del recorrido (qué se votó, qué
   consecuencia tiene, qué cambia y para quién, qué no cambia, quién votó qué con su
   fuente), no entra en pantalla.
2. **Lenguaje claro**: titulares en lengua ciudadana, nunca jerga sin glosario inline
   («convalidación» → explicada al pasar).
3. **Neutralidad**: sin eslóganes, sin adjetivos valorativos, sin recomendación de voto.
   El color por grupo existe **solo como codificación visual en el recuento de la ficha**
   (ADR-0007), nunca como valoración ni fuera de ese contexto.
4. **Móvil primero**: se diseña a 375 px y se ensancha.
5. **Sin registro, sin tracking**: lo que el usuario responda (juego) queda en su navegador.

## Paleta (neutra, provisional)

- Fondo: blanco; texto: gris-negro (#111); secundario: gris (#555).
- Sentidos del voto (neutros, sin connotación política): Sí #16a34a, No #dc2626,
  Abstención #9ca3af, No vota #d1d5db — solo como categorías de recuento, nunca como
  identidad de partido.
- Un acento único para acciones: azul (#2563eb).

## Tipografía y tono

- Fuente de sistema (`system-ui`). Títulos con peso 700, cuerpo 400, 16–18 px.
- Frases cortas. Verbos concretos. Números siempre con su contexto (n y fecha).

## Tablas de grupos

- Ordenadas por nº de escaños, descendente. El Grupo Mixto va aparte, al final.
- Siempre con el enlace a la fuente oficial debajo.

## Recuento visual de la ficha (waffle)

Reglas operativas de la vista simplificada del pleno (decisión y paleta: ADR-0007).

- **Una celda por diputado** con voto nominal; relleno = color del grupo (paleta en
  ADR-0007, contraste ≥ 3:1 sobre blanco). Celdas de ~12 px a 375 px; SVG estático
  generado, sin JavaScript.
- **El voto se lee por posición**: secciones Sí / No / Abstención / No vota, cada una
  con cabecera de color de sentido + número. El color de la celda nunca codifica el
  voto.
- **Dentro de cada sección**: bloques por grupo ordenados por nº de diputados del
  grupo en esa votación (como la tabla «voto por grupo» de debajo); el Grupo Mixto
  siempre al final; separación visible entre bloques.
- **Sin texto dentro de las celdas**: la sigla vive en la leyenda (chip + sigla +
  nombre, en el mismo orden que los bloques) y el detalle por diputado aparece a
  demanda (`title`/`aria-label`: «Nombre (Grupo): voto»).
- **Color redundante, nunca único**: la tabla «voto por grupo» de debajo conserva todo
  el dato en texto para lectoras de pantalla y personas daltónicas.
- **Votaciones sin voto individual publicado**: sin waffle; solo totales.
- Lectura esperada: grupo unido = un bloque en una sección; grupo dividido = su color
  repartido en varias secciones.
