#Global variables
PYTHON_VERSION ?= 3.11
PYTHONVERSION ?=311
PACKAGE_NAME ?= tech_professional_coacher
PROJECT_NAME ?= tech-professional-coacher
PACKAGE_VERSION ?=0.1.0
ENV ?= dev
export APP_NAME ?= tech-professional-coacher
export ARTIFACT_REGISTRY_URI ?= lucasvittal
export TAG ?= v1

#* Variables
SHELL := /usr/bin/env bash
PYTHON := python3
PYTHONPATH := $(shell pwd)
#* Docker variables


#* Wheel Path
WHEEL_PATH := src/$(PACKAGE_NAME)/


#* Installation
.PHONY: uv-create-custom-package
uv-create-custom-package:
	@if [ ! -d "$(PACKAGE_NAME)" ]; then \
		printf "[Makefile] - Creating custom package directory 'src/$(PACKAGE_NAME)'...\n"; \
		uv init --lib $(PACKAGE_NAME); \
	else \
		printf "[Makefile] - Custom package directory "$(PACKAGE_NAME)" already exists!\n"; \
	fi

.PHONY: create-project-base-structure
create-project-base-structure:

	@printf "[Makefile] - Creating project base structure...\n"
	@mkdir -p $(PACKAGE_NAME)/models
	@mkdir -p $(PACKAGE_NAME)/databases
	@mkdir -p $(PACKAGE_NAME)/services
	@mkdir -p $(PACKAGE_NAME)/constants
	@mkdir -p $(PACKAGE_NAME)/api
	@mkdir -p $(PACKAGE_NAME)/api/routes

	@mkdir -p $(PACKAGE_NAME)/utils
	@mkdir -p $(PACKAGE_NAME)/utils/logs
	@mkdir -p $(PACKAGE_NAME)/utils/metrics
	@mkdir -p $(PACKAGE_NAME)/utils/traces
	@mkdir -p $(PACKAGE_NAME)/utils/tools

	@touch $(PACKAGE_NAME)/databases/__init__.py
	@touch $(PACKAGE_NAME)/services__init__.py


	@touch $(PACKAGE_NAME)/constants/__init__.py
	@touch $(PACKAGE_NAME)/constants/settings.py
	@touch $(PACKAGE_NAME)/constants/prompt_templates.py
	@touch $(PACKAGE_NAME)/constants/messages.py

	@touch $(PACKAGE_NAME)/api/__init__.py
	@touch $(PACKAGE_NAME)/api/routes/__init__.py
	@touch $(PACKAGE_NAME)/api/routes/health.py
	@touch $(PACKAGE_NAME)/api/routes/index.py
	@touch $(PACKAGE_NAME)/api/routes/client.py
	@touch $(PACKAGE_NAME)/api/app.py


	@touch $(PACKAGE_NAME)/utils/__init__.py
	@touch $(PACKAGE_NAME)/utils/logs/__init__.py
	@touch $(PACKAGE_NAME)/utils/metrics/__init__.py
	@touch $(PACKAGE_NAME)/utils/traces/__init__.py
	@touch $(PACKAGE_NAME)/utils/tools/__init__.py
	@touch $(PACKAGE_NAME)/constants/__init__.py
	@touch $(PACKAGE_NAME)/utils/logs/log.py
	@touch $(PACKAGE_NAME)/utils/metrics/metric.py
	@touch $(PACKAGE_NAME)/utils/traces/tracer.py
	@touch $(PACKAGE_NAME)/utils/tools/agents.py
	@touch $(PACKAGE_NAME)/utils/tools/generic.py
	@touch $(PACKAGE_NAME)/utils/tools/resources.py

	@touch $(PACKAGE_NAME)/models/__init__.py
	@touch $(PACKAGE_NAME)/models/errors.py
	@touch $(PACKAGE_NAME)/models/api.py



	@printf "[Makefile] - Project base structure created.\n"

.PHONY: uv-sync
uv-sync:
	cd $(PACKAGE_NAME) && uv sync
	@printf "[Makefile] - uv synced package.\n\n"


.PHONY: pre-commit-install
pre-commit-install:
	@sudo apt install -y python$(PYTHON_VERSION)-distutils
	@printf "[Makefile] - Installing pre-commit into the virtual environment in '$(PACKAGE_NAME)'...\n"
	uv add pre-commit
	uv run pre-commit install
	@printf "[Makefile] - Pre-commit hooks installed.\n\n"

.PHONY: pre-commit-update
pre-commit-update:
	@if [ ! -f ".pre-commit-config.yaml" ]; then \
		printf "[Makefile] - Creating default .pre-commit-config.yaml in '$(PACKAGE_NAME)'...\n"; \
		mkdir -p "$(PACKAGE_NAME)"; \
		printf "repos:\n" > ".pre-commit-config.yaml"; \
		printf "  - repo: https://github.com/pre-commit/pre-commit-hooks\n" >> ".pre-commit-config.yaml"; \
		printf "    rev: v4.5.0\n" >> ".pre-commit-config.yaml"; \
		printf "    hooks:\n" >> ".pre-commit-config.yaml"; \
		printf "      - id: trailing-whitespace\n" >> ".pre-commit-config.yaml"; \
		printf "      - id: end-of-file-fixer\n" >> ".pre-commit-config.yaml"; \
		printf "      - id: check-yaml\n" >> ".pre-commit-config.yaml"; \
	fi
	cd $(PACKAGE_NAME) && uv run pre-commit autoupdate
	@printf "[Makefile] - Pre-commit hooks updated.\n\n"

# Falta criar todos os diretorios base do seu arquetipo utilizando este arquivo aqui, defina quais são os diretórios base do seu arquetipo
# crie os nesse arquivo


#* Project setup
.PHONY: init
init:  uv-create-custom-package create-project-base-structure pre-commit-install pre-commit-update uv-sync
	@if ! grep -qxF "$(PROJECT_NAME)-$(PYTHON_VERSION)/" .gitignore 2>/dev/null; then \
		printf "[Makefile] - Adding '$(PROJECT_NAME)-$(PYTHON_VERSION)/' to .gitignore\n"; \
		echo "$(PROJECT_NAME)-$(PYTHON_VERSION)/" >> .gitignore; \
	else \
		printf "[Makefile] - Virtual environment already in .gitignore\n"; \
	fi
	@printf "[Makefile] - ***** Project setup complete *****\n"

#* Project setup
.PHONY: refresh
refresh: activate-venv uv-sync
	@printf "[Makefile] - ***** Project was refreshed *****\n"

#* Formatters
.PHONY: codestyle
codestyle:
	uv run pyupgrade --exit-zero-even-if-changed --py$(PYTHONVERSION)-plus $(shell find . -name "*.py")
	uv run isort --settings-path pyproject.toml src
	uv run black --config pyproject.toml src
	@printf "[Makefile] - Code style formatting complete.\n\n"

.PHONY: check-codestyle
check-codestyle:
	uv run isort --diff --check-only --settings-path pyproject.toml src
	uv run black --diff --check --config pyproject.toml src
	uv run darglint --verbosity 2 src tests
	@printf "[Makefile] - Code style check complete.\n\n"

.PHONY: formatting
formatting: codestyle check-codestyle
	@printf "[Makefile] - ***** Formatting complete *****\n"

#* Linting
.PHONY: test
test:
	@mkdir -p assets/images
	@PYTHONPATH=$(PYTHONPATH) uv run pytest -c pyproject.toml --cov-report=html --cov=src tests/
	uv run coverage-badge -o assets/images/coverage.svg -f
	@printf "[Makefile] - Tests and coverage complete.\n\n"

.PHONY: check
check:
	uv lock --check
	@printf "[Makefile] - UV lock check complete\n"

.PHONY: check-safety
check-safety:
	uv run safety check --full-report
	@printf "[Makefile] - Safety check complete.\n\n"

.PHONY: check-bandit
check-bandit:
	uv run bandit -vv -ll --recursive src
	@printf "[Makefile] - Bandit check complete.\n\n"

.PHONY: env-check
env-check: check check-bandit check-safety
	@printf "[Makefile] - ***** Environment check complete *****\n"


#* Docker build and push
.PHONY: docker-build
docker-build:
	@printf "[Makefile] - Building Docker image %s:%s-%s...\n" "$(APP_NAME)" "$(VERSION)" "$(TAG)"
	@docker build -t "$(ARTIFACT_REGISTRY_URI)/$(APP_NAME):$(VERSION)-$(TAG)" . --no-cache
	@printf "[Makefile] - Docker image build complete.\n"

.PHONY: docker-push
docker-push:
	@printf "[Makefile] - Pushing Docker image %s:%s-%s to Artifact Registry...\n" "$(APP_NAME)" "$(VERSION)" "$(TAG)"
	@gcloud auth configure-docker us-central1-docker.pkg.dev
	@docker push $(ARTIFACT_REGISTRY_URI)/$(APP_NAME):$(VERSION)-$(TAG)
	@printf "[Makefile] - Docker image push complete.\n"

.PHONY: docker-remove
docker-remove:
	@printf "[Makefile] - Checking if Docker is installed...\n"
	@if ! command -v docker > /dev/null 2>&1; then \
		printf "[Makefile] - Docker is not installed. Please install Docker and try again.\n"; \
		exit 1; \
	fi
	@printf "[Makefile] - Removing Docker image %s:%s-%s ...\n" "$(APP_NAME)" "$(VERSION)" "$(TAG)"
	@docker rmi -f $(APP_NAME):$(VERSION)-$(TAG)
	@printf "[Makefile] - Docker image removal complete.\n"

#* Docker system prune (optional)
.PHONY: docker-clean
docker-clean:
	@printf "[Makefile] - Running Docker system prune to clean up unused Docker objects...\n"
	@docker system prune -f
	@printf "[Makefile] - Docker system prune complete.\n"

#* Build and Distribution
.PHONY: update-local-package
update-local-package:

	pip install -e .
	@pip install dist/$(PACKAGE_NAME)-$(PACKAGE_VERSION)-py3-none-any.whl
	@printf "[Makefile] - Build complete. '.tar.gz', '.zip', and '.whl' files generated in 'dist/' directory.\n\n"
.PHONY: build-wheel
build-wheel:
	@printf "[Makefile] - Building wheel for package '%s'...\n" "$(PACKAGE_NAME)"
	uv build .
	@printf "[Makefile] - Wheel build complete. Files generated in 'dist/' directory.\n\n"

.PHONY: clean-build
clean-build:
	@rm -rf build/ dist/ *.egg-info
	@printf "[Makefile] - Build artifacts cleaned.\n\n"

.PHONY: clean-dist
clean-dist: clean-build
	@rm -rf dist/
	@printf "[Makefile] - Distribution artifacts cleaned.\n\n"

.PHONY: clean-all
clean-all: cleanup clean-dist
	@printf "[Makefile] - All artifacts cleaned.\n\n"

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	@find . -type f \( -name "__pycache__" -o -name "*.pyc" -o -name "*.pyo" \) -print0 | xargs -0 rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	@find . -name ".DS_Store" -print0 | xargs -0 rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	@find . -name ".mypy_cache" -print0 | xargs -0 rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	@find . -name ".ipynb_checkpoints" -print0 | xargs -0 rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	@find . -name ".pytest_cache" -print0 | xargs -0 rm -rf

.PHONY: build-remove
build-remove:
	@rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove
	@printf "[Makefile] - ***** Cleanup environment complete *****\n"

# Set GH Workflows Variables
.PHONY: build-push-container
build-push-container:


	@printf "[Makefile] - Setting building contaner...\n"
	docker build -t $(APP_NAME):$(TAG) .
	@printf "[Makefile] - Container built successfully.\n\n"
	@printf "[Makefile] - Pushing container to Artifact Registry...\n"
	docker tag  $(APP_NAME):$(TAG) $(ARTIFACT_REGISTRY_URI)/$(APP_NAME):$(TAG)
	docker push $(ARTIFACT_REGISTRY_URI)/$(APP_NAME):$(TAG)
	@printf "[Makefile] - Pushed container successfully.\n\n"



.PHONY: update-deployment
update-deployment: build-wheel build-push-container

	@printf "[Makefile] - Updating Kubernetes deployment...\n"
	kubectl delete secret tech-professional-coacher-secrets --ignore-not-found
	kubectl create secret generic tech-professional-coacher-secrets --from-env-file=.env
	@for file in kubernetes/${ENV}/*.yaml; do \
		envsubst < "$$file" | kubectl apply -f -; \
	done
	kubectl rollout restart deployment/$(APP_NAME)
	@printf "[Makefile] - Deployment updated successfully.\n\n"

.PHONY: install
install:
	@printf "[Makefile] - Installing package using uv...\n"
	cd src/$(PACKAGE_NAME)
	uv sync
	@printf "[Makefile] - Package installed successfully.\n\n"


#* Build and publish wheels
.PHONY: build-publish-wheels
build-publish-wheels:
	@printf "[Makefile] - Starting build and publish process for PromptRegistry...\n"
	cd src/PromptRegistry
	uv build
	uv publish
	@printf "[Makefile] - Completed build and publish for PromptRegistry.\n\n"

	@printf "[Makefile] - Starting build and publish process for Mestring...\n"
	cd src/Mestring
	uv build
	uv publish
	@printf "[Makefile] - Completed build and publish for Mestring.\n\n"

.PHONY: clean-tmp
clean-tmp:
	@rm -rf tmp/wheels
	@printf "[Makefile] - Temp folder cleaned.\n\n"
