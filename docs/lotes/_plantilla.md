# Plantilla de apuesta — `docs/lotes/_plantilla.md`

Fuente de verdad de los campos. Cada apuesta copia esta plantilla al crear su carpeta.

**Reglas de la plantilla (lecciones del 10/11/2026):**

1. **Nada se omite sin declararlo.** Si un campo no aplica, se escribe «No aplica» y el
   porqué. Omitir en silencio es cómo nacen los desvíos.
2. **Cada dato vive en un único sitio.** El estado de la apuesta vive SOLO en
   `docs/apuestas.md`; aquí van fechas y tamaño, no estado.
3. **Sin calcos forzados:** concepto explícito en castellano o término en inglés entre
   paréntesis. Prohibidos: «colina», «conejos», «piteado».
4. **Nombres de carpeta:** `yymmdd_<nombre-corto>`. La fecha es la de apertura y no
   cambia nunca. Las referencias cruzadas usan el nombre corto.
5. **Evidencias largas** (auditorías, análisis): `informe-<tema>.md` en la misma carpeta.
   `notas.md` queda para el diario del lote.

---

## Fichero `plan.md`

```markdown
# <Nombre corto>

**Fechas:** apertura → · **Tamaño estimado:** ~X semanas

## Problema

## Apuesta

## No-objetivos

## Riesgos de desvío (rabbit holes)
1. **Riesgo** — mitigación.

## Recorridos de usuario (el «hecho» es el recorrido completo)
1. ...

## Cuándo está hecho
- ...
```

## Fichero `tareas.md`

```markdown
# Tareas — <Nombre corto>

Marca `[x]` al completar. El agente trabaja de arriba abajo con `/siguiente`.

## Estado vivo

- **En exploración:** tareas cuyo «cómo» aún no está decidido. Al decidirlo, migran a
  «En construcción».
- **En construcción:** tareas con el «cómo» claro: solo queda ejecutarlas.

## Scopes (tareas con checkboxes)
```

## Fichero `notas.md`

```markdown
# Notas — <Nombre corto>

## <fecha> · <tema>
- <qué pasó · qué aprendimos>
```
