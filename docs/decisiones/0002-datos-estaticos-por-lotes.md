# ADR-0002: Datos estáticos, actualización por lotes programados

**Fecha:** 2026-11-10 · **Estado:** aceptada

**Contexto:** ¿MVP estático (regenerar datasets/web periódicamente) o dinámico (API viva
consultando fuentes)? El Congreso publica los votos con horas/días de retraso.

**Decisión:** estático por lotes. Ingesta programada que regenera datasets y web. Sin
servidores de base de datos ni backends vivos en el MVP.

**Consecuencias:** coste ~0, despliegue sencillo (estáticos), cada publicación es una
versión reproducible y auditable. Renunciamos al «tiempo real», que además no existe
contra esta fuente. Una API estática (JSON/CSV publicados) cubre el producto «API»
(lote 02). Se revisará si algún día se necesita interactividad servidor.
