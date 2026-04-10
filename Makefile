.PHONY: help build up down logs shell migrate makemigrations test createsuperuser loaddata generate clean

.DEFAULT_GOAL := help

DC := docker compose

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build:  ## Build Docker images
	$(DC) build

up:  ## Start services (Django + PostgreSQL)
	$(DC) up -d
	@echo "Django: http://localhost:8000"
	@echo "Admin: http://localhost:8000/admin/"

down:  ## Stop services
	$(DC) down

logs:  ## Show logs (use SERVICE=web or SERVICE=db)
	$(DC) logs -f $(SERVICE)

shell:  ## Django shell
	$(DC) exec web python manage.py shell

migrate:  ## Run migrations
	$(DC) exec web python manage.py migrate

makemigrations:  ## Create migrations
	$(DC) exec web python manage.py makemigrations

createsuperuser:  ## Create admin user
	$(DC) exec web python manage.py createsuperuser

loaddata:  ## Import JSON master data into database
	$(DC) exec web python manage.py import_master_data

test:  ## Run legibility tests
	$(DC) exec web python -m pytest tests/ -v

smoketest:  ## Smoke test all admin and public URLs
	$(DC) exec web python manage.py smoke_test_urls

lint:  ## Run ruff linter
	$(DC) exec web ruff check .

lintfix:  ## Fix auto-fixable lint issues
	$(DC) exec web ruff check --fix .

deadcode:  ## Find dead code with vulture
	$(DC) exec web vulture portfolio/ resumes/views.py resumes/urls.py --min-confidence 80

generate:  ## Generate all static resume outputs
	$(DC) exec web python master_resume_generator.py
	$(DC) exec web python generate_all_resumes.py

clean:  ## Remove containers and volumes
	$(DC) down -v
