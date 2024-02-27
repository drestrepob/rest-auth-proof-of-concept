build-and-start:
	docker-compose up --build

start:
	docker-compose up

stop:
	docker-compose down

clean:
	docker-compose down --volumes --rmi all

database-migrate:
	docker exec -it backend alembic migrate -m "$(message)"

database-revision:
	docker exec -it backend alembic revision -m "$(message)"

database-migration-history:
	docker exec -it backend alembic history

database-upgrade:
	docker exec -it backend alembic upgrade head

database-downgrade:
	docker exec -it backend alembic downgrade

test:
	poetry run pytest --no-header --no-summary
