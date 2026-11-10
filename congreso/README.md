# congreso — paquete de ingesta y validación

Descarga las votaciones del Pleno desde los datos abiertos del Congreso de los Diputados
(fuente primaria), valida los recuentos contra los totales oficiales y exporta a SQLite
y a la ficha web.

```sh
congreso ingesta  --legislatura XV --sesion 202 --fecha 2026-09-30
congreso validar  --legislatura XV --sesion 202 --fecha 2026-09-30
congreso exportar --legislatura XV --sesion 202 --fecha 2026-09-30
```

Regla del proyecto (ver `AGENTS.md`): si el Congreso dice 172 Sí, la base debe decir 172.
`validar` sale con error si hay cualquier descuadre.
