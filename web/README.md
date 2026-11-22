# web — la webapp

La web pública de la XV se **genera** desde los datos validados:

```sh
make ingesta-legislatura && make diputados && make validar
make exportar-legislatura && make temas && make web
make dev   # http://localhost:8000
```

- `index.html` — portada con buscador y filtros (palabra, resultado, tema); los
  primeros 50 elementos se ven sin JavaScript.
- `indice.json` — alimenta la búsqueda en el navegador (no hay servidor).
- `votacion/` — una ficha por votación (2.175 en la XV).
- `datos/` — dataset descargable (JSON + CSV) con su cita y licencias.

No editar nada a mano: `make web` regenera el sitio y se perderían los cambios.
Las reglas visuales están en `docs/diseno.md`.
