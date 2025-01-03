.DEFAULT_GOAL := help

DOCKER_REGISTRY ?= cespeleta
DOCKER_IMAGE_NAME ?= food-review-api
DOCKER_IMAGE_TAG ?= local
DOCKER_OPTS ?=

PROJECT_DIR = food_review_api
TEST_DIR = tests

#help:			@ List available tasks on this project.
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| sort | tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#clean:			@ Clean cache and temporary files
clean:
	find . | grep -E "(/\.coverage|/\.pytest_cache|/\.ruff_cache|/\.test_results|dist)" | xargs rm -rf

#setup:			@ Setup Python environment and pre-commit hooks
setup:
	poetry install
	poetry run pre-commit install

#lint.fix:		@ Fix format and lint issues.
lint.fix:
	poetry run ruff check --fix
	poetry run ruff format

#lint.check:	@ Check format and lint issues.
lint.check:
	poetry run ruff check --diff
	poetry run ruff format --check --diff

#test:			@ Run repository unit test suite
test:
	poetry run pytest --cov=$(PROJECT_DIR) $(TEST_DIR)

#build.docker: 	@ Build service docker image
build.docker:
	docker build -t $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) $(DOCKER_OPTS) .

#run.app: 		@ Run unicorn in local
run.app:
	poetry run uvicorn \
	--loop uvloop \
	--workers 1 \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info \
    --access-log \
    --factory \
    food_review_api:build_service_app
