DOCKER_COMPOSE ?= docker compose

FRONTEND = frontend
BACKEND = backend
DB = database

.DEFAULT_GOAL := docker-help

.PHONY: docker-help docker-up docker-build docker-down docker-restart docker-logs clean docker-clean-data docker-rebuild-frontend docker-rebuild-backend docker-rebuild-db docker-build-up

docker-help:  ## Show the list of available commands
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

docker-up:  ## Up all containers
	$(DOCKER_COMPOSE) up -d

docker-build:  ## Build all containers
	$(DOCKER_COMPOSE) build

docker-build-up: ## Build and up all containers
	$(MAKE) docker-build
	$(MAKE) docker-up

docker-down:  ## Stop and remove containers (without volumes)
	$(DOCKER_COMPOSE) down

docker-restart:  ## Restart all conainers
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d

docker-logs:  ## Show the logs of all services
	$(DOCKER_COMPOSE) logs -f

docker-rebuild-frontend:  ## Rebuild frontend
	$(DOCKER_COMPOSE) build $(FRONTEND)

docker-rebuild-backend:  ## Rebuild backend
	$(DOCKER_COMPOSE) build $(BACKEND)

docker-rebuild-db:  ## Reabuild database
	$(DOCKER_COMPOSE) build $(DB)

docker-clean-data:  ## Stop and remove volume и .pgdata
	$(DOCKER_COMPOSE) down -v
	rm -rf /.pgdata
