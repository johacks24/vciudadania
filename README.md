# vCiudadania

**La versión ciudadana de las decisiones públicas.** Trazabilidad de las votaciones del
Congreso de los Diputados (España), para votar con más información y luchar contra la
polarización. Cívico, independiente, sin publicidad y sin recomendación de voto.

La «v» es de **versión**, como en `doc_v0, doc_v1, doc_vN`: vParlamento frente a
vCiudadania — el homenaje a g0v («fork the government») y a su «versión del pueblo» de
la web oficial. Nace en el Congreso y no lleva el nombre de ninguna institución: está
pensado para extenderse a parlamentos autonómicos y ayuntamientos, y para que algún día
la ciudadanía co-redacte normas con canal de retorno real (vTaiwan, Leyes Abiertas, ILP).

**Principios:** fuentes primarias siempre citadas · open by default · simplicidad ·
neutralidad (decimos qué se votó y quién votó qué; la valoración es tuya).

## Estado

Apuesta en desarrollo: cadena completa validada (Congreso → validación 100 % → datos →
ficha pública). Tablero: `docs/apuestas.md`. Lotes: `docs/lotes/`.

## Arranque

```sh
make setup      # crea .venv e instala el paquete congreso
make ingesta    # descarga la sesión de prueba desde el Congreso (fuente primaria)
make validar    # cuadra los recuentos contra los totales oficiales
make exportar   # genera data/processed/congreso.sqlite y web/index.html
make dev        # sirve la ficha en http://localhost:8000
make test       # suite de tests
```

## Estructura

- `congreso/` — paquete Python (fuentes, modelo, exportación, tests). La unidad open source.
- `web/` — la webapp (fichas y, más adelante, el juego de coincidencias).
- `docs/` — el método público, las decisiones (ADR), las referencias y las apuestas con sus lotes.
- `data/` — generada, no versionada. `data/raw/` inmutable.

## Licencias

- **Código:** AGPL-3.0 (`LICENSE`).
- **Contenidos y datos elaborados** (resúmenes, fichas, normalizaciones): CC BY-SA 4.0
  (`LICENSE-CONTENIDOS.md`).
- **Datos originales** del Congreso de los Diputados y del BOE: no son nuestros; se rigen
  por las condiciones de reutilización de cada organismo.

## Cómo citar

> vCiudadania (vciudadania), a partir de los datos abiertos del Congreso de los Diputados.
