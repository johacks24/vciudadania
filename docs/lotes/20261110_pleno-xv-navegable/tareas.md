# Tareas — Lote 01

Marca `[x]` al completar. El agente trabaja de arriba abajo con `/siguiente`.

## Estado vivo

- **En exploración:** ninguna. Los «cómo» abiertos al moldear quedaron resueltos y
  documentados en `notas.md` (corpus cerrado → ingesta única; búsqueda estática en
  cliente; temas de CongresoAbierto con validación; categorías sin voto individual;
  tabla de diputados propia).
- **En construcción:** todas las tareas de los scopes A–E, de arriba abajo.

## Scope A — Análisis previo (obligatorio antes de los detalles)

- [x] A.1 Informe del ecosistema: **holapolitica** y **quevotan** con el checklist del
      lote 00 (licencia, actividad, cobertura XV, calidad/validación, datos/API,
      comunidad) + qué adoptar, qué evitar y qué mueve el buscador y las afinidades
      → `informe-ecosistema.md` — *hecha el 22/11: ambos vivos y alineados con la
      validación nominal-vs-totales; XV disuelta (corpus cerrado de 2.189 votaciones
      según quevotan); el alcance del lote se confirma sin cambios y las
      implicaciones quedan en el informe (contraste de totales como tercera barrera,
      afinidades diferenciadas por experiencia, no por existencia)*
- [x] A.2 ADR-0007 «color de los grupos parlamentarios» con la decisión documentada
      (mientras tanto rige lo provisional de `docs/diseno.md`: un solo color neutro)
      — *hecha el 22/11: decisión funcional con dirección del humano — color de grupo
      SOLO en el recuento visual de la ficha (waffle: celda por diputado, voto por
      posición, color redundante con leyenda y alternativa textual); paleta de quevotan
      (AGPL-3.0) oscurecida a contraste ≥ 3:1 sobre blanco; sin hemiciclo literal y sin
      siglas en celdas. En esta misma sesión se registró la dirección de diseño: C.1
      pasa a scroll infinito y C.4 incorpora el waffle (notas.md)*

## Scope B — Ingesta XV completa (el corazón de datos)

- [x] B.1 Enumeración por legislatura: escalar el cliente de sesión suelta a la XV
      completa (índice `diasVotaciones`: 147 días, 19/09/2023 → 02/10/2026) y
      preparar el CLI/Makefile para legislatura entera
      — *hecha el 22/11: índice real `var diasVotaciones = [enteros]` con
      `targetLegislatura` (147 días verificados en vivo); sesión y fecha derivadas de
      la propia URL oficial (ingesta pierde `--sesion`); pausa educada 0,5 s; día sin
      JSON (llamamiento) es categoría en modo legislatura y error solo en modo día;
      `make ingesta-legislatura` listo para que B.2 lo ejecute; 9/9 tests sin red con
      fixtures reales (índice y día de llamamiento)*
- [x] B.2 Descarga completa de la XV a `data/raw/` (inmutable; ~2.190 JSON de
      votación, pausa educada entre peticiones)
      — *hecha el 22/11: **2.175 JSON** (72 MB, 144 sesiones, ~30 min, 0 errores,
      idempotente: los 21 de la sesión 202 se saltaron); 5 de los 147 días sin JSON
      (solo llamamiento); cuadra exacto con CongresoAbierto (2.175) y deja los 14
      de diferencia con quevotan (2.189) para el contraste de B.3; pausa educada
      también entre páginas de día*
- [x] B.3 Validación 100 % de la legislatura (recuentos individuales == totales
      oficiales, votación a votación) con categorías explícitas «sin voto individual
      publicado»: suplicatorios (secreto) y públicas por llamamiento (12 en la XV) →
      contraste del total con quevotan (2.189) y CongresoAbierto (2.175)
      — *hecha el 22/11: **2.175 validadas: 2.173 nominales == totales oficiales,
      2 suplicatorios (sesiones 89 y 202), 0 descuadres, 0 duplicadas**, en 1,3 s;
      `make validar` pasa a modo legislatura con detección de duplicados y 13/13
      tests. Contraste cerrado con evidencia: CongresoAbierto 2.175 (exacto);
      quevotan 2.189 = +14 llamamiento sin JSON (sesiones 5, 6, 8, 11, 15×4, 17, 18,
      30, 43, 203×2; 12 con nominal recuperado del Diario). La tarea decía «12»:
      la cifra exacta verificada es 14*
- [x] B.4 Tabla de diputados de la XV: esquema pydantic primero, luego carga desde el
      opendata de diputados (altas/bajas, formación, grupo) — identificadores
      estables; sin suponer una sola legislatura (ADR-0003)
      — *hecha el 22/11: `Diputado` (esquema primero); exportadores Activos + DeBaja
      del opendata: **137 + 275 = 412**, la cifra exacta de quevotan; clave natural
      nombre + legislatura (412 únicos, formato idéntico al campo `diputado` de las
      votaciones); 9 grupos con nombre oficial; limitación declarada: el exportador
      trae el grupo final (Belarra → Mixto el 05/12/2023), la historia previa se
      derivará de las votaciones si hace falta; tabla SQLite PK (legislatura, nombre);
      `make diputados`, idempotente verificado; 19/19 tests; 4x4 nº 6: los tests de
      URLs asertan la URL completa*
- [x] B.5 Exportación SQLite completa de la XV (data/processed/congreso.sqlite)
      — *hecha el 23/11: `make exportar-legislatura` → **2.175 votaciones +
      760.518 votos + 19.561 resúmenes + 412 diputados** (59 MB, 3 s, 0 descuadres);
      760.518 + 4.200 (12 llamamiento × 350) = 764.718 de quevotan, cierre exacto;
      reconstrucción limpia (también se borra votaciones) y fallo rápido si faltan
      los diputados; el modo sesión del lote 00 verificado sin cambios; 23/23 tests*

## Scope C — Buscador y fichas (la web navegable)

- [ ] C.1 Portada índice: las votaciones más recientes primero, con carga automática
      al llegar al final de la página (scroll infinito) sobre el índice JSON de C.2;
      los primeros N sin JavaScript (recorrido 1)
- [ ] C.2 Búsqueda por palabra y filtro por resultado con índice JSON compacto
      filtrado en cliente (decisión en `notas.md`; ADR-0002)
- [ ] C.3 Tema por votación: importar los temas de CongresoAbierto (CC BY 4.0) con
      atribución y validación nuestra (ADR-0005.3) → filtro por tema (recorrido 2)
- [ ] C.4 Ficha por votación para toda la XV (~2.190 fichas: qué se votó, recuento
      con waffle por diputado — ADR-0007: celda de color de grupo, voto por posición,
      alternativa textual —, voto por grupo, fuente oficial; recorrido 3) — generador
      del lote 00 escalado

## Scope D — Dataset descargable

- [ ] D.1 Export JSON + CSV de la XV con cita y método de reutilización (recorrido 4;
      la API documentada de la apuesta «API pública v1» sigue siendo no-objetivo)

## Scope E — Producción y cierre

- [ ] E.1 CI verde (tests sin red, con fixture) y `make validar` al 100 % sobre la XV
      completa documentado en `notas.md`
- [ ] E.2 Despliegue en Pages verificado (HTTP 200, recorridos 1–4) y apuesta a
      producción en `docs/apuestas.md` + commits limpios por scope
