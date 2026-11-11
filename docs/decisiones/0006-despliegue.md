# ADR-0006: Despliegue — GitHub Pages (Vercel y Codeberg como alternativas)

**Fecha:** 2026-11-11 · **Estado:** aceptada

## Contexto

El proyecto produce **estáticos planos** (`make exportar` genera `web/`) y necesita URL
pública. Criterios: alineación con open by default, coste cero, mínima complejidad, y
sin acoplarse a una plataforma (regla del proyecto: regenerable en cualquier sitio).

## Decisión

**GitHub Pages** sirviendo la carpeta `web/` tras el primer push.
URL prevista: `https://<usuario>.github.io/vciudadania`.

## Alternativas consideradas

- **Vercel** (la de eslahoradelaverdad): se activará si la web pasa a ser una app
  Next.js (búsqueda y fichas dinámicas del lote «Pleno XV navegable»). Migración
  trivial: el output sigue siendo estático.
- **Codeberg Pages** (asociación sin ánimo de lucro, plataforma Forgejo): máxima
  coherencia FOSS. Opción menor y de baja probabilidad, registrada por deseo del
  proyecto; la puerta queda abierta y el coste de migración es ≈ 0 por diseño.
- Netlify / Cloudflare Pages: equivalentes a Vercel; sin ventaja diferencial aquí.
- VPS propio: mantenimiento real sin beneficio para estáticos; descartado.

## Consecuencias

- **Cero dependencia de plataforma por diseño:** `make exportar` produce ficheros
  servibles en cualquier host; cambiar de hosting no toca una línea de código.
- La CI y el repo viven en GitHub; una eventual migración a Codeberg llevaría consigo
  repo, CI y Pages a la vez.
- URL final (usuario de GitHub) por fijar al crear el repo; ajustar entonces el enlace
  del método en la ficha generada (`exportar_ficha.py`).
