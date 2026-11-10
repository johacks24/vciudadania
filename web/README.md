# web — la webapp

La ficha pública (`index.html`) **se genera** desde los datos validados:

```sh
make ingesta && make validar && make exportar
make dev   # http://localhost:8000
```

No editar `index.html` a mano: se regenera y se perderían los cambios. Las reglas
visuales están en `docs/diseno.md`. En el lote 01 esta carpeta se convierte en la
webapp navegable (buscador y fichas).
