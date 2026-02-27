# (c) qirelo 2025

.PHONY: help dev build prod test lint docker-build test-all

PORT ?= 8000

PROJECT_NAME := $(notdir $(CURDIR))
IMAGE_TAG ?= latest
IMAGE_SHA ?= unknown
APP=start.py

help:
	@echo "Available commands:"
	@echo "--------------------------------"
	@echo "make help          - Display this help message"
	@echo "make dev           - Run development server"
	@echo "make prod          - Run production server"
	@echo "make test          - Run tests"
	@echo "make lint          - Run linter"
	@echo "make docker-build  - Build docker image"
	@echo "make test-all  	  - Test all"
	@echo "make reset	  	  - Reset dev DB & cache"

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

reset:
	rm -f db.sqlite3
	rm -rf **/__pycache__
