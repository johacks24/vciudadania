.PHONY: setup ingesta validar exportar test dev tail-logs limpiar

# Punto de entrada unico para humanos y agentes (Simon Willison / Armin Ronacher).
# Comandos defensivos: si se usan mal, avisan en vez de romperse.

SESION      := 202
FECHA       := 2026-09-30
LEGISLATURA := XV

setup: ## crear .venv e instalar el paquete congreso
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e "congreso[dev]"
	@echo "Listo. Prueba: make test"

ingesta: ## descargar la sesion de prueba desde la fuente primaria (Congreso)
	.venv/bin/congreso ingesta --legislatura $(LEGISLATURA) --sesion $(SESION) --fecha $(FECHA)

validar: ## cuadrar recuentos individuales contra los totales oficiales
	.venv/bin/congreso validar --legislatura $(LEGISLATURA) --sesion $(SESION) --fecha $(FECHA)

exportar: ## generar data/processed/congreso.sqlite y la ficha web/index.html
	.venv/bin/congreso exportar --legislatura $(LEGISLATURA) --sesion $(SESION) --fecha $(FECHA)

test: ## suite de tests
	.venv/bin/pytest congreso -q

dev: ## servir la ficha en http://localhost:8000
	python3 -m http.server 8000 --directory web

tail-logs: ## ultimas lineas del log combinado (capa de conciencia del agente, regla 4x4)
	@tail -n 40 data/proceso.log 2>/dev/null || echo "sin log todavia (data/proceso.log)"

limpiar: ## borrar artefactos regenerables
	rm -rf data .pytest_cache congreso/*.egg-info congreso/congreso/__pycache__ congreso/congreso/tests/__pycache__
	@echo "data/ borrada: regenera con make ingesta"
