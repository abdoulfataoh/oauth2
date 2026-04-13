# coding: utf-8

.PHONY: help dev build prod test lint docker-build test-all

PORT ?= 8000

PROJECT_NAME := $(shell basename "$$(pwd)")
IMAGE_TAG ?= latest
IMAGE_SHA ?= unknown
APP=start.py

help:
	@echo "Available commands:"
	@echo "--------------------------------"
	@echo "make help            - Display this help message"
	@echo "make dev             - Run development server"
	@echo "make prod            - Run production server"
	@echo "make test            - Run tests"
	@echo "make lint            - Run linter"
	@echo "make docker-build    - Build docker image"
	@echo "make test-all        - Run lint + tests"
	@echo ""
	@echo "Database commands:"
	@echo "--------------------------------"
	@echo "make db-migrate m='msg' - Create migration"
	@echo "make db-upgrade        - Apply migrations"
	@echo "make db-downgrade      - Rollback last migration"
	@echo "make db-current        - Show current revision"
	@echo "make db-history        - Show migration history"
	@echo "make db-reset          - Reset DB (dev only)"
	@echo ""
	@echo "Cleanup:"
	@echo "--------------------------------"
	@echo "make reset            - Reset DB + clean cache"


dev:
	fastapi dev $(APP) --host 0.0.0.0 --port $(PORT)

prod:
	gunicorn start:app \
		-k uvicorn.workers.UvicornWorker \
		-w 4 \
		-b 0.0.0.0:$(PORT)

test:
	pytest -v

lint:
	mypy start.py app
	flake8 app

docker-build:
	docker build \
		-t $(PROJECT_NAME):$(IMAGE_TAG) \
		-t $(PROJECT_NAME):sha-$(IMAGE_SHA) \
		-t $(PROJECT_NAME):latest \
		.

test-all: lint test
	@echo "All test are OK"


db-migrate:
	alembic revision --autogenerate -m "$(m)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-current:
	alembic current

db-history:
	alembic history

db-reset:
	rm -rf alembic/versions
	rm -f db.sqlite3
# 	alembic upgrade head

reset:
	make db-reset
	find . -type d -name "__pycache__" -exec rm -rf {} +
