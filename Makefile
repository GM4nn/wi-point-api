# Docker 

up:
	docker compose up --build -d

down:
	docker compose down

restart-api:
	docker compose restart api

logs:
	docker compose logs -f api

# Alembic

migration:
	docker compose exec api alembic revision --autogenerate -m "$(m)"

migrate:
	docker compose exec api alembic upgrade head

downgrade:
	docker compose exec api alembic downgrade -1

# Seed

seed:
	docker compose exec api python -m app.seed.main

# tests

tests:
	docker compose exec api pytest