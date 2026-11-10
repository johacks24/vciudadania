# Revisora Legislativa

Trazabilidad de las votaciones del Congreso de los Diputados (España), para votar con
más información y luchar contra la polarización. Proyecto cívico, independiente, sin
publicidad y sin recomendación de voto.

**Principios:** fuentes primarias siempre citadas · open by default · simplicidad ·
neutralidad (decimos qué se votó y quién votó qué; la valoración es tuya).

## Estado

Lote 00 en curso: cadena completa andando (Congreso → validación → base de datos →
ficha web pública). Ver `docs/apuestas.md`.

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
- `web/` — la webapp (fichas +, más adelante, el juego de coincidencias).
- `docs/` — el método público, las decisiones (ADR) y los lotes de trabajo.
- `data/` — generada, no versionada. `data/raw/` inmutable.

## Licencias

- **Código:** AGPL-3.0 (`LICENSE`).
- **Contenidos y datos elaborados** (resúmenes, fichas, normalizaciones): CC BY-SA 4.0
  (`LICENSE-CONTENIDOS.md`).
- **Datos originales** del Congreso de los Diputados y del BOE: no son nuestros; se rigen
  por las condiciones de reutilización de cada organismo.

## Cómo citar

> Revisora Legislativa (repositorio: revisora_legislativa), a partir de los datos abiertos
> del Congreso de los Diputados.
