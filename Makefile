# coding: utf-8

help:
	@echo "make help						- Display help"
	@echo "make flake8						- Check linting with flake8"
	@echo "make mypy						- Check typing with mypy"
	@echo "make ipython						- Launch ipython shell"
	@echo "make test-server					- Run test server"
	@echo "make reset						- Reset database"


flake8:
	flake8 start.py app recipes

mypy:
	mypy start.py app

ipython:
	ipython

run-dev:
	fastapi dev start.py --host 0.0.0.0 --reload

reset:
	rm -f db.sqlite3
	rm -rf **/__pycache__
