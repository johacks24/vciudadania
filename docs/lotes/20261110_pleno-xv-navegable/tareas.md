# Tareas — Lote 01

Marca `[x]` al completar. El agente trabaja de arriba abajo con `/siguiente`.

## Estado vivo

- **En exploración:** ninguna. Los «cómo» abiertos al moldear quedaron resueltos y
  documentados en `notas.md` (corpus cerrado → ingesta única; búsqueda estática en
  cliente; temas de CongresoAbierto con validación; categorías sin voto individual;
  tabla de diputados propia).
- **En construcción:** todas las tareas de los scopes A–E, de arriba abajo.

## Scope A — Análisis previo (obligatorio antes de los detalles)

- [ ] A.1 Informe del ecosistema: **holapolitica** y **quevotan** con el checklist del
      lote 00 (licencia, actividad, cobertura XV, calidad/validación, datos/API,
      comunidad) + qué adoptar, qué evitar y qué mueve el buscador y las afinidades
      → `informe-ecosistema.md`
- [ ] A.2 ADR-0007 «color de los grupos parlamentarios» con la decisión documentada
      (mientras tanto rige lo provisional de `docs/diseno.md`: un solo color neutro)

## Scope B — Ingesta XV completa (el corazón de datos)

- [ ] B.1 Enumeración por legislatura: escalar el cliente de sesión suelta a la XV
      completa (índice `diasVotaciones`: 147 días, 19/09/2023 → 02/10/2026) y
      preparar el CLI/Makefile para legislatura entera
- [ ] B.2 Descarga completa de la XV a `data/raw/` (inmutable; ~2.190 JSON de
      votación, pausa educada entre peticiones)
- [ ] B.3 Validación 100 % de la legislatura (recuentos individuales == totales
      oficiales, votación a votación) con categorías explícitas «sin voto individual
      publicado»: suplicatorios (secreto) y públicas por llamamiento (12 en la XV) →
      contraste del total con quevotan (2.189) y CongresoAbierto (2.175)
- [ ] B.4 Tabla de diputados de la XV: esquema pydantic primero, luego carga desde el
      opendata de diputados (altas/bajas, formación, grupo) — identificadores
      estables; sin suponer una sola legislatura (ADR-0003)
- [ ] B.5 Exportación SQLite completa de la XV (data/processed/congreso.sqlite)

## Scope C — Buscador y fichas (la web navegable)

- [ ] C.1 Portada índice: las votaciones más recientes primero, paginadas
      (recorrido 1)
- [ ] C.2 Búsqueda por palabra y filtro por resultado con índice JSON compacto
      filtrado en cliente (decisión en `notas.md`; ADR-0002)
- [ ] C.3 Tema por votación: importar los temas de CongresoAbierto (CC BY 4.0) con
      atribución y validación nuestra (ADR-0005.3) → filtro por tema (recorrido 2)
- [ ] C.4 Ficha por votación para toda la XV (~2.190 fichas: qué se votó, recuento,
      voto por grupo, fuente oficial; recorrido 3) — generador del lote 00 escalado

## Scope D — Dataset descargable

- [ ] D.1 Export JSON + CSV de la XV con cita y método de reutilización (recorrido 4;
      la API documentada de la apuesta «API pública v1» sigue siendo no-objetivo)

## Scope E — Producción y cierre

- [ ] E.1 CI verde (tests sin red, con fixture) y `make validar` al 100 % sobre la XV
      completa documentado en `notas.md`
- [ ] E.2 Despliegue en Pages verificado (HTTP 200, recorridos 1–4) y apuesta a
      producción en `docs/apuestas.md` + commits limpios por scope
