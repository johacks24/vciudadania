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
3. **Neutralidad**: sin eslóganes, sin adjetivos valorativos, sin colores de partido.
   El uso de color por grupo parlamentario está **pendiente de ADR** (lote 01); mientras
   tanto, un solo color neutro para todo.
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
