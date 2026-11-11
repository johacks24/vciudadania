# ADR-0005: Sobre qué construir — fuente primaria propia + contribución a CongresoAbierto

**Fecha:** 2026-11-10 · **Estado:** aceptada
**Evidencia completa:** `docs/lotes/20261110_fundamentos-y-spike/informe-auditoria.md` (auditoría con checklist a–g,
metodología y verificación cruzada)

## Contexto

El proyecto necesita una base de datos de votaciones con trazabilidad. Regla aceptada
por el humano: vale una API open source revisable o una API gratuita de terceros **si
existe sistema de validación contra la fuente oficial**. Candidatos auditados:

| Candidato | Veredicto | Motivo |
|---|---|---|
| **CongresoAbierto** (congresoabierto.org, MIT + CC BY 4.0) | **Vivo y apto** | Último commit 2026-10-11; 2.175 votaciones del Pleno XV; su importador consume los JSON oficiales y **aborta si el recuento nominal no cuadra con los totales**; CI con 8 ficheros de tests; CORS abierto; hoja de ruta con issues encajables. Riesgo: una sola persona, 1 mes de vida; su descarga es semimanual (script pegado en consola del navegador). |
| civis-api | Descartado | Muerto (>4 años sin commits, Heroku 404, sin LICENSE, CC BY-NC). |
| API Reforma Digital | Descartado | Bloqueo programático total (429 + checkpoint JS/WASM de Vercel en todos los endpoints) y ~5 % de cobertura (121 de 2.175 votaciones). Sin licencia verificable. |

Verificación cruzada: 3/3 votaciones al azar de su CSV cuadran exactamente con el JSON
oficial (totales y recuento nominal); el mismo día, nuestro spike validó 21/21 votaciones
de la sesión 202 contra la fuente primaria.

## Decisión

1. **Fuente primaria siempre el opendata oficial del Congreso** con nuestro importador
   (`congreso/`), que ya está vivo y validado (lote 00). No nos acoplamos a la
   infraestructura de terceros.
2. **CongresoAbierto = proyecto hermano al que contribuir** (vía de aportación open
   source): prioridades en su hoja de ruta que encajan con nuestro pipeline —
   automatizar la descarga diaria, ingestar comisiones, exponer el voto nominal en
   CSV/JSON público. Las contribuciones de código a su repo serán MIT (su licencia);
   nuestro código propio sigue AGPL-3.0.
3. Sus datos derivados (temas, votaciones clave, CSV) se usan como **fuente secundaria
   con atribución CC BY 4.0 y validación nuestra** — jamás sin contrastar.

## Consecuencias

- No reinventamos curación que ya existe (temas, votaciones clave): la reutilizamos
  verificándola.
- La segunda barrera de validación (`make validar`) permanece: dos productores
  independientes (Congreso y CongresoAbierto) + nuestra verificación = cadena de
  confianza sin punto único de fallo.
- Si CongresoAbierto se estanca, nuestro pipeline regenera todo desde la fuente primaria
  (ruta documentada en su propia metodología): riesgo de dependencia mitigado por diseño.
