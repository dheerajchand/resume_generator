# Resume Generator Documentation

A Django-based professional identity system that generates targeted resumes in multiple formats. Content is managed through a Grappelli admin interface, organized into archetypes and instances, and delivered as PDF, DOCX, RTF, or Markdown.

## Documentation Index

| Document | Description |
|----------|-------------|
| [Architecture](architecture.md) | System overview, apps, data flow, how content moves from database to rendered PDF |
| [Data Model](data-model.md) | Every model, every field, every relationship -- the complete schema reference |
| [Admin Guide](admin-guide.md) | Using the Grappelli admin: editing content, creating archetypes, managing instances, sending resumes, tracking follow-ups |
| [Development](development.md) | Docker setup, Make commands, running locally, testing workflows |
| [Deployment](deployment.md) | Railway hosting, environment variables, database management, redeployment procedures |
| [Email Setup](email-setup.md) | Resend configuration, email templates, placeholder variables, the sending flow |
| [Resume Types](resume-types.md) | What each archetype emphasizes, how to create new ones, customization options |
| [PDF Engine](pdf-engine.md) | How `core_services.py` works, color schemes, KeepTogether architecture, multi-format generation |
| [Testing](testing.md) | Legibility tests, smoke tests, ruff linting, vulture dead-code analysis |

## Quick Start

```bash
# Clone and build
git clone <repo-url> resume_generator
cd resume_generator
make build

# Start services (Django + PostgreSQL 16)
make up

# Run migrations and load data
make migrate
make loaddata

# Open in browser
open http://localhost:8000
```

## Project Structure

```
resume_generator/
├── portfolio/                 # Professional Portfolio app
│   ├── models.py              # All content and workflow models
│   ├── admin.py               # Grappelli admin configuration
│   ├── services.py            # Data assembly services
│   ├── signals.py             # Cache invalidation
│   ├── email.py               # Resend email integration
│   └── management/commands/   # import_master_data, smoke_test_urls
├── resumes/                   # Resume generation engine
│   ├── core_services.py       # ResumeGenerator (PDF, DOCX, RTF, MD)
│   └── views.py               # Download and generation endpoints
├── generate_all_resumes.py    # Batch generation script
├── master_resume_generator.py # Legacy JSON-based builder
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Web + PostgreSQL orchestration
├── Makefile                   # Developer task runner
└── docs/                      # This documentation
```
