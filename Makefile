VENV=venv
PIP=$(VENV)/bin/pip

$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

requirements.txt:
	$(PIP) freeze | sort > $@

lint:
	flake8

test:
	@python --version
	pytest -v
