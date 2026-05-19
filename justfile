export COMPOSE_FILE := "docker-compose.local.yml"

## Just does not yet manage signals for subprocesses reliably, which can lead to unexpected behavior.
## Exercise caution before expanding its usage in production environments.
## For more information, see https://github.com/casey/just/issues/2473 .


# Default command to list all available commands.
default:
    @just --list

# build: Build python image.
build *args:
    @echo "Building python image..."
    @docker compose build {{args}}

# up: Start up containers.
up:
    @echo "Starting up containers..."
    @docker compose up -d --remove-orphans

# down: Stop containers.
down:
    @echo "Stopping containers..."
    @docker compose down

# prune: Remove containers and their volumes.
prune *args:
    @echo "Killing containers and removing volumes..."
    @docker compose down -v {{args}}

# logs: View container logs
logs *args:
    @docker compose logs -f {{args}}

# manage: Executes `manage.py` command.
manage +args:
    @docker compose run --rm django python ./manage.py {{args}}

# restart: Restart containers.
restart:
    @echo "Restarting containers..."
    @docker compose restart

# pytest: Run pytest.
pytest *args:
    @docker compose run --rm django pytest {{args}}

# pytest-cov: Run pytest with coverage report and fail below 80%.
pytest-cov *args:
    @docker compose run --rm django coverage run -m pytest {{args}}
    @docker compose run --rm django coverage report --fail-under=80

# isort: Sort Python imports. Usage: just isort [path]
isort *args:
    @docker compose run --rm django uv run isort {{ if args == "" { "." } else { args } }}

# flake8: Run flake8 lint. Usage: just flake8 [path]
flake8 *args:
    @docker compose run --rm django uv run flake8 {{ if args == "" { "." } else { args } }}

# lint: Run import sorting and flake8. Usage: just lint [path]
lint *args:
    @docker compose run --rm django uv run isort {{ if args == "" { "." } else { args } }}
    @docker compose run --rm django uv run flake8 {{ if args == "" { "." } else { args } }}