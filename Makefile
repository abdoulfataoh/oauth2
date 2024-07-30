# coding: utf-8
# Copyright (C) 2024 vela

help:
	@echo "make help						- Display help"
	@echo "make flake8						- Check linting with flake8"
	@echo "make mypy						- Check typing with mypy"
	@echo "make ipython						- Launch ipython shell"
	@echo "make test-server					- Run test server"
	@echo "make reset						- Reset database"


flake8:
	flake8

mypy:
	mypy start.py fastapi_oauth2_service

ipython:
	ipython

test-server:
	uvicorn start:app --port 8000 --host 0.0.0.0 --reload

reset:
	rm -rf db.sqlite3
	rm -rf **/__pycache__
