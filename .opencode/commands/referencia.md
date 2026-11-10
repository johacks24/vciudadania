---
description: Guardar una referencia (URL) en docs/referencias
---
Guarda la referencia $ARGUMENTS siguiendo las reglas de `docs/referencias/indice.md`:

1. Descarga la URL y conviértela a Markdown limpio (sin publicidad ni ruido de nav).
2. Guárdala como `docs/referencias/_privado/<slug>.md` con cabecera: título, URL
   original y fecha de guardado.
3. Añade una fila a la tabla de `docs/referencias/indice.md`: título, origen local,
   y **una línea «principio que sacamos de aquí»** — pídemela si no está clara antes
   de escribirla.
4. Si la descarga falla, dímelo y guarda solo la fila del índice con la URL.
