install:
	pip install -U -r requirements.txt
	pip install flake8 pytest

lint:
	flake8

test:
	@python --version
	pytest -v

IMAGE=amirkdv/pydantic-pr-checks
VERSION=$(shell git describe --tags --dirty)
docker-build:
	docker build -t $(IMAGE):$(VERSION) .

docker-test: docker-build
	docker run -it $(IMAGE):$(VERSION) sh -c "pip install pytest && pytest -v"

docker-push: docker-test
	@echo $(VERSION) | grep -q dirty && { echo "refusing to push a dirty tag!"; exit 1; } || true
	docker tag $(IMAGE):$(VERSION) $(IMAGE):latest
	docker push $(IMAGE):latest
