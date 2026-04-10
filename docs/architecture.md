# Architecture

## System Overview

The Resume Generator is a Django application that manages professional identity content in a PostgreSQL database and renders it into multiple document formats on demand. It is designed around three concepts:

1. **Content** — Professional data (positions, achievements, projects, skills) stored as normalized Django models.
2. **Archetypes** — Domain-specific templates that select and order subsets of content for a particular professional narrative (e.g., "Data Science," "GIS/Geospatial," "Electoral Consulting").
3. **Instances** — Targeted versions of an archetype created for a specific recipient, opportunity, or job posting, with optional overrides.

## Apps

### `portfolio/` — Professional Portfolio

The primary app. Owns all content models, the admin interface, data assembly services, cache invalidation signals, and email delivery.

| Module | Responsibility |
|--------|---------------|
| `models.py` | All Django models: content (PersonalInfo, Position, Achievement, Project, Skill), structure (ResumeArchetype, through-tables, ProfessionalSummary), workflow (Recipient, ResumeInstance, GenerationRecord, EmailTemplate) |
| `admin.py` | Grappelli admin classes with sortable inlines, custom actions (Send Resume), fieldset organization |
| `services.py` | `build_resume_data_from_db()` assembles a flat dictionary from related models; `get_archetype_metadata()` returns archetype configuration |
| `signals.py` | `post_save` signal handlers that invalidate cached resume data when any content model changes |
| `email.py` | `send_resume_email()` generates the resume, renders the email template, sends via Resend API, logs a GenerationRecord |
| `management/commands/import_master_data.py` | Imports a master JSON file into the database, creating or updating all content models |
| `management/commands/smoke_test_urls.py` | Hits every public URL and asserts 200 status codes |

### `resumes/` — Resume Generation Engine

The rendering layer. Takes assembled data dictionaries and produces documents.

| Module | Responsibility |
|--------|---------------|
| `core_services.py` | `ResumeGenerator` class: PDF generation via ReportLab, DOCX via python-docx, RTF via PyRTF3, Markdown via string templates. Handles color schemes, length variants, KeepTogether page-break logic. |
| `views.py` | Three view functions: `download_form` (public), `generate_on_demand` (public POST), `generate_instance` (authenticated) |

### Supporting Files

| File | Purpose |
|------|---------|
| `generate_all_resumes.py` | Batch script: iterates all archetypes, generates all format/length/color combinations, writes to `output/`, generates a README |
| `master_resume_generator.py` | Legacy JSON-based data builder. Still used for length-variant truncation logic (trimming content to fit page targets). |

## Data Flow

Content flows through the system in a pipeline:

```
┌──────────────────────────────────────────────────────────────┐
│                     Django Admin (Grappelli)                 │
│  User edits PersonalInfo, Positions, Achievements, Projects, │
│  Skills, Archetypes, Recipients, Instances                   │
└──────────────────────┬───────────────────────────────────────┘
                       │ save
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                     PostgreSQL 16                             │
│  Normalized content tables with M2M through-tables           │
└──────────────────────┬───────────────────────────────────────┘
                       │ post_save signal
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                  Cache Invalidation (signals.py)             │
│  Clears cached resume data so next request gets fresh content│
└──────────────────────────────────────────────────────────────┘

                       │ request
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                  portfolio/services.py                        │
│  build_resume_data_from_db(archetype_slug)                   │
│  - Fetches PersonalInfo singleton                            │
│  - Loads archetype + related positions, achievements,        │
│    projects, skills via through-tables (respecting sort_order)│
│  - Loads ProfessionalSummary                                 │
│  - Returns flat dictionary                                   │
└──────────────────────┬───────────────────────────────────────┘
                       │ data dict
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              master_resume_generator.py (optional)           │
│  Applies length truncation for short/brief variants          │
└──────────────────────┬───────────────────────────────────────┘
                       │ trimmed data dict
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                resumes/core_services.py                       │
│  ResumeGenerator.generate(data, format, color_scheme)        │
│  - PDF: ReportLab with KeepTogether blocks, color scheme     │
│  - DOCX: python-docx with styled paragraphs                 │
│  - RTF: PyRTF3                                               │
│  - MD: String-templated Markdown                             │
└──────────────────────┬───────────────────────────────────────┘
                       │ binary/text output
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   Delivery                                    │
│  - HTTP StreamingResponse (download)                         │
│  - Email attachment via Resend (send action)                 │
│  - File on disk (batch generation)                           │
└──────────────────────────────────────────────────────────────┘
```

## Three Generation Flows

### 1. Public Download (No Authentication)

```
User visits / → selects archetype, length, color, format → POST /generate/
→ build_resume_data_from_db() → ResumeGenerator → StreamingHttpResponse
```

- No login required.
- Available at the root URL.
- User picks from dropdowns and clicks download.

### 2. Instance Download (Authenticated)

```
Admin creates ResumeInstance → GET /download/instance/<id>/
→ build_resume_data_from_db(archetype) + summary_override → ResumeGenerator → StreamingHttpResponse
```

- Requires Django login.
- Uses the archetype attached to the instance.
- Applies `summary_override` from the instance if present.

### 3. Email Send (Admin Action)

```
Admin selects ResumeInstance(s) in admin → "Send Resume" action
→ generate PDF → render EmailTemplate → Resend API → log GenerationRecord → set follow_up_date
```

- Triggered from the Django admin list view.
- Generates PDF, attaches it to an email.
- Uses the EmailTemplate system for subject/body.
- Logs every send as a GenerationRecord.
- Automatically sets follow-up tracking fields.

## Caching Strategy

Cache invalidation is handled by Django signals in `portfolio/signals.py`. Every content model (PersonalInfo, Position, Responsibility, Achievement, Project, Skill, etc.) has a `post_save` signal that clears cached data. This ensures:

- Edits in admin are immediately reflected in generated resumes.
- No stale content is served from cache.
- Redis is optional (`REDIS_URL` environment variable). Without it, Django's default cache backend is used.

## Request Lifecycle

1. **Request arrives** at a view in `resumes/views.py`.
2. **View extracts parameters**: archetype slug, format type, color scheme, length variant.
3. **`build_resume_data_from_db()`** queries the database, assembling all content for the archetype into a flat dictionary.
4. **Length truncation** (if not "long"): `master_resume_generator.py` trims positions, responsibilities, achievements, and projects to fit the target page count.
5. **`ResumeGenerator`** renders the data into the requested format with the chosen color scheme.
6. **Response** streams the generated file to the client.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Django 5.x |
| Admin Interface | Grappelli (django-grappelli) |
| Database | PostgreSQL 16 |
| PDF Generation | ReportLab |
| DOCX Generation | python-docx |
| RTF Generation | PyRTF3 |
| Email | Resend (Python SDK) |
| Caching | Redis (optional) / Django default |
| Containerization | Docker + docker-compose |
| Hosting | Railway |
| Linting | ruff |
| Dead Code | vulture |
| Testing | pytest |
