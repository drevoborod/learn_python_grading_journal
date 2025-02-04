-include .env
export

db.run:
	@docker compose up -d db

clean:
	@docker compose down -t 1

db.migrate: db.wait
	python -m grading_journal.create_database

run:
	@uvicorn grading_journal.server:app --host 0.0.0.0 --port 8882

dev.run:
	@python -m grading_journal

db.fill:
	@psql ${DB_URL} -f fixtures/dev.sql

db.cli:
	@psql ${DB_URL}

db.wait:
	@echo "Waiting until postgres is ready..."
	@while ! echo exit | nc ${GRADING_JOURNAL_DATABASE_ADDRESS} ${GRADING_JOURNAL_DATABASE_PORT}; do sleep 5; done
