# Development Guide

## Prerequisites

- **Docker** and **Docker Compose** (v2+)
- **Make** (included on macOS and most Linux distributions)
- **Git**

Optional (for running outside Docker):
- Python 3.11+
- PostgreSQL 16

---

## Quick Start with Docker

```bash
# 1. Clone the repository
git clone <repo-url> resume_generator
cd resume_generator

# 2. Build the Docker image
make build

# 3. Start services (Django web server + PostgreSQL 16)
make up

# 4. Run database migrations
make migrate

# 5. Load seed data from master JSON
make loaddata

# 6. Create a superuser for admin access
make shell
# Inside the container:
python manage.py createsuperuser
# Then exit the shell

# 7. Open in browser
open http://localhost:8000        # Public download form
open http://localhost:8000/admin/ # Admin interface
```

---

## Makefile Commands

The Makefile is the primary interface for development tasks. Every command is designed to run inside Docker.

### Core Commands

| Command | Description |
|---------|-------------|
| `make build` | Build the Docker image from the Dockerfile |
| `make up` | Start all services in the foreground (web + PostgreSQL) |
| `make down` | Stop and remove all containers |
| `make shell` | Open a bash shell inside the running web container |

### Database Commands

| Command | Description |
|---------|-------------|
| `make migrate` | Run `python manage.py migrate` inside the container |
| `make loaddata` | Run `import_master_data` management command to load JSON seed data into the database |

### Generation Commands

| Command | Description |
|---------|-------------|
| `make generate` | Run `generate_all_resumes.py` — generates all format/length/color combinations for all archetypes, writes output files and a README |

### Quality Commands

| Command | Description |
|---------|-------------|
| `make test` | Run the pytest test suite |
| `make lint` | Run ruff linter on the codebase |
| `make deadcode` | Run vulture to detect unused/dead code |
| `make smoketest` | Run the `smoke_test_urls` management command — hits every public URL and checks for 200 responses |

### Maintenance Commands

| Command | Description |
|---------|-------------|
| `make clean` | Remove generated output files and temporary artifacts |

---

## Docker Architecture

### docker-compose.yml

Two services:

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `web` | Built from `./Dockerfile` | 8000 | Django development server |
| `db` | `postgres:16` | 5432 | PostgreSQL database |

The web service depends on `db` and waits for it to be ready before starting.

### Dockerfile

- Based on a Python 3.11+ image.
- Installs system dependencies (for ReportLab PDF generation, PostgreSQL client libraries).
- Copies the project and installs Python dependencies from `requirements.txt`.
- Exposes port 8000.
- Default command runs Django's development server.

### Volumes

- The project directory is mounted into the container for live code reloading.
- PostgreSQL data is persisted in a named Docker volume so it survives container restarts.

---

## Running Without Docker

If you prefer running directly on your machine:

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up PostgreSQL
# Create a database and user, then set DATABASE_URL:
export DATABASE_URL="postgresql://user:password@localhost:5432/resume_generator"

# 4. Set required environment variables
export SECRET_KEY="your-secret-key-here"
export DEBUG=True
export DJANGO_SETTINGS_MODULE="config.settings"  # or your settings module path
export ALLOWED_HOSTS="localhost,127.0.0.1"

# 5. Run migrations
python manage.py migrate

# 6. Load data
python manage.py import_master_data

# 7. Create superuser
python manage.py createsuperuser

# 8. Run the development server
python manage.py runserver
```

---

## Project Layout

```
resume_generator/
├── portfolio/                     # Professional Portfolio app
│   ├── __init__.py
│   ├── models.py                  # All content and workflow models
│   ├── admin.py                   # Grappelli admin configuration
│   ├── services.py                # build_resume_data_from_db(), get_archetype_metadata()
│   ├── signals.py                 # Cache invalidation on post_save
│   ├── email.py                   # send_resume_email() via Resend
│   ├── apps.py                    # AppConfig
│   ├── urls.py                    # App URL patterns
│   └── management/
│       └── commands/
│           ├── import_master_data.py   # JSON → DB import
│           └── smoke_test_urls.py      # URL smoke tests
├── resumes/                       # Resume generation engine
│   ├── __init__.py
│   ├── core_services.py           # ResumeGenerator class
│   ├── views.py                   # Download/generation views
│   ├── urls.py                    # App URL patterns
│   └── templates/                 # HTML templates (download form)
├── generate_all_resumes.py        # Batch generation script
├── master_resume_generator.py     # Legacy JSON-based data builder
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── manage.py
├── pytest.ini / pyproject.toml    # Test configuration
└── docs/                          # Documentation (you are here)
```

---

## Development Workflow

### Making Content Changes

1. Edit content in the Django admin (see [Admin Guide](admin-guide.md)).
2. Cache invalidation happens automatically via signals.
3. Download a resume from `/` to verify changes.

### Making Code Changes

1. Edit code locally — Docker volume mount enables live reloading.
2. If you change models:
   ```bash
   make shell
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Run quality checks:
   ```bash
   make lint      # ruff
   make deadcode  # vulture
   make test      # pytest
   make smoketest # URL checks
   ```

### Adding a New Model

1. Define the model in `portfolio/models.py`.
2. Create and run migrations:
   ```bash
   make shell
   python manage.py makemigrations portfolio
   python manage.py migrate
   ```
3. Register in `portfolio/admin.py` with appropriate inlines and fieldsets.
4. If the model affects resume content, add a `post_save` signal in `portfolio/signals.py` for cache invalidation.
5. Update `portfolio/services.py` if the data needs to flow into resume generation.
6. Update tests.

### Adding a New Archetype

No code changes needed — archetypes are data, not code:

1. Go to the admin.
2. Create a new ResumeArchetype with appropriate settings.
3. Add positions, achievements, projects, and skill categories via inlines.
4. Write a ProfessionalSummary.
5. Test by downloading from the public form.

---

## Environment Variables

For local development, these are the minimum required environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | — | Django secret key |
| `DEBUG` | No | `False` | Enable debug mode |
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `DJANGO_SETTINGS_MODULE` | Yes | — | Python path to settings module |
| `ALLOWED_HOSTS` | Yes | — | Comma-separated list of allowed hostnames |
| `RESEND_API_KEY` | No | — | Required only for email sending |
| `FROM_EMAIL` | No | — | Required only for email sending |
| `REDIS_URL` | No | — | Optional Redis URL for caching |

When running with Docker Compose, most of these are configured in the `docker-compose.yml` file or a `.env` file.

---

## Common Issues

### Database connection refused
The PostgreSQL container may not be ready yet. Wait a few seconds and try again, or check `docker compose logs db`.

### Migrations out of sync
If you pull changes that include new migrations:
```bash
make migrate
```

### Port 8000 already in use
Another process is using port 8000. Either stop it or change the port in `docker-compose.yml`.

### ReportLab font issues
If PDF generation fails with font errors, ensure the Docker image has the required system fonts installed. Check the Dockerfile for font package installations.
