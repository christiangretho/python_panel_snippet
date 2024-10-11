.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

setup: requirements.txt
	python3 -m venv venv
	. venv/bin/activate
	$(PIP) install -r requirements.txt

venv:
	. venv/bin/activate

run_test: db_test
	export DB_ENV="TEST_DB" && panel serve app.py

run: venv
	panel serve app.py --show

test_setup: venv
	playwright install

test:
	pytest -v

test_debug: venv
	PWDEBUG=1 pytest -v -s

generate_test: venv
	playwright codegen http://localhost:5006/app

clean: 
	rm -rf venv && rm -rf __pycache__ && rm -rf .pytest_cache

db_dev: venv
	$(PYTHON) database.py

db_test: venv
	export DB_ENV="TEST_DB" && $(PYTHON) database.py

.PHONY: venv