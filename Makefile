install:
	pip install -U -r requirements.txt
	pip install flake8 pytest

lint:
	flake8

test:
	@python --version
	pytest -v

build:
	docker build -t markdown-sections .
