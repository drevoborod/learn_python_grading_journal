init:
	@$(MAKE) up
	@sleep 3
	python -m grading_journal.create_database

up:
	@docker-compose up -d

down:
	@docker-compose down

run:
	@$(MAKE) up
	@uvicorn grading_journal.main:app --host 0.0.0.0 --port 8882 --log-level debug

