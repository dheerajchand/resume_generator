# Data Model Reference

All models live in `portfolio/models.py`. This document covers every model, every field, and every relationship.

## Entity Relationship Overview

```
PersonalInfo (singleton)
    └── SocialLink (1:N)

Position (content)
    └── Responsibility (1:N)

Achievement (content, standalone)

Project (content)
    └── ProjectTechnology (1:N)

SkillCategory (content)
    └── Skill (1:N)

ResumeArchetype (structure)
    ├── M2M → Position (through ArchetypePosition)
    ├── M2M → Achievement (through ArchetypeAchievement)
    ├── M2M → Project (through ArchetypeProject)
    ├── M2M → SkillCategory (through ArchetypeSkillCategory)
    └── ProfessionalSummary (1:1)

Recipient (workflow, standalone)

ResumeInstance (workflow)
    ├── FK → ResumeArchetype
    ├── FK → Recipient
    └── GenerationRecord (1:N)

EmailTemplate (workflow, standalone)
```

---

## Content Models

### PersonalInfo

Singleton model containing the resume owner's identity and branding information. Only one row should exist.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Full name as it appears on resumes |
| `title` | CharField | Professional title / headline (e.g., "Senior Data Scientist & GIS Specialist") |
| `email` | EmailField | Contact email address |
| `phone` | CharField | Contact phone number |
| `website` | URLField | Personal or professional website URL |
| `location` | CharField | Full location string used internally |
| `location_display` | CharField | Formatted location for display on resumes (e.g., "Washington, DC Metro Area") |
| `slogan` | CharField | Professional tagline or slogan |
| `logo_url` | URLField | URL to a logo image for PDF headers |
| `footer_text` | TextField | Text rendered in the PDF footer |

**Admin**: Displayed as a singleton — the admin enforces that only one PersonalInfo record exists.

---

### SocialLink

Links to social media and professional profiles, associated with PersonalInfo.

| Field | Type | Description |
|-------|------|-------------|
| `personal_info` | ForeignKey → PersonalInfo | Parent record |
| `platform` | CharField | Platform name (e.g., "LinkedIn", "GitHub", "Twitter") |
| `url` | URLField | Full URL to the profile |
| `sort_order` | IntegerField | Display ordering (lower numbers appear first) |

**Admin**: Inline on the PersonalInfo admin page, sortable by `sort_order`.

---

### Position

A professional role held at an organization. Positions are the backbone of the experience section.

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | Job title (e.g., "Lead Data Scientist") |
| `company` | CharField | Employer or organization name |
| `location` | CharField | City, state, or "Remote" |
| `dates` | CharField | Date range string (e.g., "January 2020 – Present") |
| `subtitle` | CharField | Optional subtitle or team/division name |
| `is_current` | BooleanField | Whether this is a currently-held position |
| `sort_order` | IntegerField | Default display ordering (lower = first). Archetypes can override this via through-tables. |

**Relationships**: Has many `Responsibility` children.

---

### Responsibility

A bullet point describing work performed in a Position.

| Field | Type | Description |
|-------|------|-------------|
| `position` | ForeignKey → Position | Parent position |
| `text` | TextField | The responsibility text as displayed on resumes |
| `text_neutral` | TextField | A neutralized/generalized version of the text (used when domain-specific language should be softened) |
| `sort_order` | IntegerField | Display ordering within the position |

**Usage**: Archetypes control how many responsibilities appear per position via `max_responsibilities_per_job`. The `text_neutral` variant can be selected when the archetype targets a general audience.

---

### Achievement

A standalone professional achievement or award, not tied to a specific position.

| Field | Type | Description |
|-------|------|-------------|
| `slug` | SlugField | URL-safe identifier (e.g., `published-research-paper`) |
| `text` | TextField | Full achievement description |
| `sort_order` | IntegerField | Default display ordering |

**Usage**: Archetypes select which achievements to include and can limit the count via `max_achievements`.

---

### Project

A portfolio project with rich description fields supporting multiple narrative angles.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Project name |
| `dates` | CharField | Project timeframe |
| `description` | TextField | General project description |
| `impact` | TextField | Business or social impact statement |
| `technical_description` | TextField | Technical implementation details |
| `business_description` | TextField | Business context and outcomes |
| `spatial_description` | TextField | Geospatial or geographic aspects (specific to GIS-oriented archetypes) |
| `sort_order` | IntegerField | Default display ordering |

**Relationships**: Has many `ProjectTechnology` children.

**Usage**: Archetypes control which description fields are shown via `show_project_technical_details` and related settings.

---

### ProjectTechnology

A technology or tool used in a Project.

| Field | Type | Description |
|-------|------|-------------|
| `project` | ForeignKey → Project | Parent project |
| `name` | CharField | Technology name (e.g., "PostGIS", "React", "scikit-learn") |
| `sort_order` | IntegerField | Display ordering |

**Admin**: Inline on the Project admin page.

---

### SkillCategory

A grouping of related skills (e.g., "Programming Languages", "GIS Tools", "Statistical Methods").

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Category name |
| `slug` | SlugField | URL-safe identifier |
| `sort_order` | IntegerField | Display ordering |

**Relationships**: Has many `Skill` children.

---

### Skill

An individual skill within a category.

| Field | Type | Description |
|-------|------|-------------|
| `category` | ForeignKey → SkillCategory | Parent category |
| `name` | CharField | Skill name (e.g., "Python", "QGIS", "Bayesian Inference") |
| `detail` | CharField | Optional detail or proficiency note |
| `sort_order` | IntegerField | Display ordering within the category |

**Usage**: The `competency_detail_level` field on ResumeArchetype controls whether `detail` is shown.

---

## Structure Models

### ResumeArchetype

The central organizing concept. An archetype defines a domain-specific resume template by selecting which content to include and how to present it.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Human-readable name (e.g., "Data Science", "GIS/Geospatial", "Electoral Consulting") |
| `slug` | SlugField | URL-safe identifier used in URLs and file names |
| `description` | TextField | What this archetype emphasizes and who it targets |
| `is_electoral` | BooleanField | Whether this archetype is for electoral/political consulting work |
| `max_achievements` | IntegerField | Maximum number of achievements to display |
| `max_responsibilities_per_job` | IntegerField | Maximum bullet points per position |
| `siege_analytics_max` | IntegerField | Maximum items for the Siege Analytics section (if applicable) |
| `show_project_technical_details` | BooleanField | Whether to show `technical_description` on projects |
| `competency_detail_level` | CharField/IntegerField | Controls skill detail display: whether to show the `detail` field on Skills |

**Many-to-Many Relationships** (all via through-tables with `sort_order`):

| Relationship | Through Table | Description |
|-------------|---------------|-------------|
| `positions` | ArchetypePosition | Which positions to include and in what order |
| `achievements` | ArchetypeAchievement | Which achievements to include and in what order |
| `projects` | ArchetypeProject | Which projects to include and in what order |
| `skill_categories` | ArchetypeSkillCategory | Which skill categories to include and in what order |

Each through-table has:
- `archetype` — ForeignKey → ResumeArchetype
- The related content model FK (e.g., `position` → Position)
- `sort_order` — IntegerField controlling display order within this archetype

---

### ProfessionalSummary

A one-to-one summary paragraph for an archetype. Each archetype has exactly one professional summary.

| Field | Type | Description |
|-------|------|-------------|
| `archetype` | OneToOneField → ResumeArchetype | Parent archetype |
| `text` | TextField | The professional summary paragraph displayed at the top of the resume |

**Admin**: Inline on the ResumeArchetype admin page.

---

## Workflow Models

### Recipient

A person or organization to whom a resume is being sent. Standalone — not tied to an archetype.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Recipient's full name |
| `company` | CharField | Recipient's organization |
| `role` | CharField | Recipient's job title or role |
| `email` | EmailField | Recipient's email address (used for sending) |
| `job_url` | URLField | URL to the job posting or opportunity |
| `job_title` | CharField | Title of the position being applied for |
| `relationship_type` | CharField | Nature of the relationship (e.g., "recruiter", "hiring manager", "referral") |
| `linkedin_url` | URLField | Recipient's LinkedIn profile URL |
| `notes` | TextField | Free-text notes about the recipient or opportunity |

---

### ResumeInstance

A targeted resume created for a specific recipient and opportunity. Combines an archetype with a recipient and optional overrides.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Descriptive name for this instance (e.g., "Acme Corp Data Science Role") |
| `archetype` | ForeignKey → ResumeArchetype | Which archetype to use as the base |
| `recipient` | ForeignKey → Recipient | Who this resume is for |
| `summary_override` | TextField | If set, replaces the archetype's ProfessionalSummary for this instance |
| `subject_override` | CharField | If set, replaces the email subject line for this instance |
| `notes` | TextField | Internal notes about this instance |
| `follow_up_date` | DateField | When to follow up (auto-set after sending) |
| `follow_up_status` | CharField | Tracking status (e.g., "pending", "sent", "responded") |
| `follow_up_notes` | TextField | Notes about follow-up interactions |

**Relationships**: Has many `GenerationRecord` children.

---

### GenerationRecord

An audit log entry created every time a resume is generated or emailed for an instance.

| Field | Type | Description |
|-------|------|-------------|
| `instance` | ForeignKey → ResumeInstance | The instance that was generated |
| `archetype_slug` | CharField | Archetype slug at the time of generation (denormalized for history) |
| `format_type` | CharField | Output format: `pdf`, `docx`, `rtf`, or `md` |
| `output_type` | CharField | How it was delivered (e.g., "download", "email") |
| `color_scheme` | CharField | Which color scheme was used |
| `length_variant` | CharField | Which length variant: `long`, `short`, or `brief` |
| `generated_at` | DateTimeField | Timestamp of generation (auto-set) |
| `was_emailed` | BooleanField | Whether this generation was sent via email |

**Purpose**: Provides a complete audit trail. You can see exactly what was sent, when, in what format, and to whom.

---

### EmailTemplate

Reusable email templates for sending resumes. Supports placeholder variables.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Human-readable template name |
| `slug` | SlugField | URL-safe identifier |
| `subject_template` | CharField | Email subject with placeholder variables |
| `body_template` | TextField | Email body with placeholder variables |
| `is_default` | BooleanField | Whether this is the default template (only one should be default) |

**Placeholders**: See [Email Setup](email-setup.md) for the full list of available template variables.

---

## Through-Table Summary

All archetype-to-content relationships use explicit through-tables to support custom sort ordering per archetype. This means the same Position can appear in multiple archetypes at different sort positions.

| Through Table | Left FK | Right FK | Extra Fields |
|--------------|---------|----------|--------------|
| ArchetypePosition | ResumeArchetype | Position | `sort_order` |
| ArchetypeAchievement | ResumeArchetype | Achievement | `sort_order` |
| ArchetypeProject | ResumeArchetype | Project | `sort_order` |
| ArchetypeSkillCategory | ResumeArchetype | SkillCategory | `sort_order` |

## Model Diagram (Text)

```
┌─────────────────┐     ┌─────────────────┐
│  PersonalInfo   │────<│   SocialLink     │
│  (singleton)    │     │                  │
└─────────────────┘     └─────────────────┘

┌─────────────────┐     ┌─────────────────┐
│    Position     │────<│  Responsibility  │
└────────┬────────┘     └─────────────────┘
         │
         │ M2M (through)
         │
┌────────┴────────┐     ┌─────────────────┐
│ ResumeArchetype │────<│ ProfessionalSumm │
│                 │     └─────────────────┘
│                 │──M2M──> Achievement
│                 │──M2M──> Project ────< ProjectTechnology
│                 │──M2M──> SkillCategory ────< Skill
└────────┬────────┘
         │
         │ FK
         │
┌────────┴────────┐     ┌─────────────────┐
│ ResumeInstance  │────>│   Recipient      │
│                 │     └─────────────────┘
│                 │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────┴────────┐
│GenerationRecord │
└─────────────────┘

┌─────────────────┐
│  EmailTemplate  │  (standalone, referenced by send logic)
└─────────────────┘
```
