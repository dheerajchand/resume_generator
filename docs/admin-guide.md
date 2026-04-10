# Admin Guide

The Resume Generator uses [Grappelli](https://django-grappelli.readthedocs.io/) as its Django admin theme. Grappelli provides a polished UI with sortable inlines, collapsible fieldsets, and improved navigation.

## Accessing the Admin

- **Local**: `http://localhost:8000/admin/`
- **Production**: `https://dheeraj-chands-resume-generator-production.up.railway.app/admin/`

Log in with your Django superuser credentials. If you need to create one:

```bash
make shell
# then inside the container:
python manage.py createsuperuser
```

## Admin Sections Overview

The admin sidebar organizes models into logical groups under the **Portfolio** app:

| Section | Models |
|---------|--------|
| Personal Identity | PersonalInfo, SocialLink |
| Experience | Position, Responsibility |
| Accomplishments | Achievement |
| Portfolio | Project, ProjectTechnology |
| Skills | SkillCategory, Skill |
| Resume Structure | ResumeArchetype, ProfessionalSummary |
| Workflow | Recipient, ResumeInstance, GenerationRecord |
| Email | EmailTemplate |

---

## Editing Content

### Personal Information

1. Navigate to **Portfolio > Personal Info**.
2. There is only one record (singleton pattern). Click it to edit.
3. Update name, title, contact details, location, slogan, logo URL, or footer text.
4. **SocialLinks** appear as sortable inlines below. Drag to reorder, or set `sort_order` values.
5. Click **Save**.

### Positions (Work Experience)

1. Navigate to **Portfolio > Positions**.
2. Click **Add Position** or click an existing one.
3. Fill in title, company, location, dates, optional subtitle.
4. Check **Is current** for your present role.
5. Set `sort_order` to control default ordering (lower numbers appear first).
6. **Responsibilities** appear as sortable inlines:
   - `text` — The main bullet point.
   - `text_neutral` — A de-emphasized variant for general-audience archetypes.
   - `sort_order` — Order within this position.
7. Click **Save**.

### Achievements

1. Navigate to **Portfolio > Achievements**.
2. Each achievement has a `slug` (auto-generated from text if left blank), `text`, and `sort_order`.
3. Write achievement text as a complete sentence or bullet point.

### Projects

1. Navigate to **Portfolio > Projects**.
2. Each project supports multiple description angles:
   - `description` — General overview.
   - `impact` — Business/social impact.
   - `technical_description` — Implementation details (shown when archetype has `show_project_technical_details = True`).
   - `business_description` — Business context.
   - `spatial_description` — Geographic/GIS aspects.
3. **ProjectTechnologies** appear as sortable inlines. Add the tools and technologies used.

### Skills

1. Navigate to **Portfolio > Skill Categories** to manage groupings.
2. Each category has a `name`, `slug`, and `sort_order`.
3. Click into a category to see its **Skills** as sortable inlines.
4. Each skill has:
   - `name` — The skill name.
   - `detail` — Optional proficiency or context note (shown based on archetype's `competency_detail_level`).
   - `sort_order` — Order within the category.

---

## Creating and Managing Archetypes

Archetypes are the heart of the system. Each one defines a domain-specific resume narrative.

### Creating a New Archetype

1. Navigate to **Portfolio > Resume Archetypes**.
2. Click **Add Resume Archetype**.
3. Fill in:
   - `name` — Human-readable (e.g., "Machine Learning Engineer").
   - `slug` — URL-safe identifier (e.g., `machine-learning-engineer`). Auto-generated if left blank.
   - `description` — What this archetype emphasizes.
   - `is_electoral` — Check if this is for political/electoral work.
4. Configure display limits:
   - `max_achievements` — How many achievements to show.
   - `max_responsibilities_per_job` — How many bullet points per position.
   - `siege_analytics_max` — Items for the Siege Analytics section.
   - `show_project_technical_details` — Whether to include `technical_description` on projects.
   - `competency_detail_level` — Whether to show skill `detail` fields.
5. Click **Save and continue editing** to access the relationship inlines.

### Adding Content to an Archetype

After saving the archetype, you will see inline sections for:

#### Positions
- Click **Add another Archetype Position**.
- Select the Position from the dropdown.
- Set `sort_order` to control the order within this archetype.
- Repeat for each position you want to include.

#### Achievements
- Click **Add another Archetype Achievement**.
- Select the Achievement and set `sort_order`.

#### Projects
- Click **Add another Archetype Project**.
- Select the Project and set `sort_order`.

#### Skill Categories
- Click **Add another Archetype Skill Category**.
- Select the SkillCategory and set `sort_order`.

#### Professional Summary
- The **Professional Summary** inline appears at the bottom (or top, depending on admin configuration).
- Write the summary paragraph that will appear at the top of resumes generated from this archetype.

### Sorting Content

Grappelli's sortable inlines let you drag-and-drop items to reorder them. The `sort_order` field updates automatically. You can also set sort_order values manually.

**Key principle**: The sort order on through-tables (e.g., ArchetypePosition) overrides the default sort order on the content model (e.g., Position.sort_order). This means the same position can appear in different order across different archetypes.

---

## Creating Instances

Instances are targeted resumes for specific recipients and opportunities.

### Step 1: Create a Recipient

1. Navigate to **Portfolio > Recipients**.
2. Click **Add Recipient**.
3. Fill in:
   - `name` — The person's name.
   - `company` — Their organization.
   - `role` — Their job title.
   - `email` — Their email address (required for sending).
   - `job_url` — Link to the job posting.
   - `job_title` — Title of the role you are applying for.
   - `relationship_type` — How you know them (recruiter, hiring manager, referral, etc.).
   - `linkedin_url` — Their LinkedIn profile.
   - `notes` — Any context about the opportunity.
4. Click **Save**.

### Step 2: Create a Resume Instance

1. Navigate to **Portfolio > Resume Instances**.
2. Click **Add Resume Instance**.
3. Fill in:
   - `name` — Descriptive label (e.g., "Acme Corp — Senior Data Scientist").
   - `archetype` — Select which archetype to use as the base.
   - `recipient` — Select the recipient.
   - `summary_override` — Optional. If filled in, this replaces the archetype's ProfessionalSummary for this instance only.
   - `subject_override` — Optional. Overrides the email subject line.
   - `notes` — Internal notes.
4. Leave follow-up fields blank — they are auto-managed.
5. Click **Save**.

---

## Sending Resumes via Email

The admin provides a custom action to send resumes directly from the interface.

### Sending

1. Navigate to **Portfolio > Resume Instances**.
2. Select one or more instances using the checkboxes.
3. From the **Action** dropdown, select **Send Resume**.
4. Click **Go**.

### What Happens When You Send

1. The system generates a PDF using the instance's archetype and settings.
2. It selects the EmailTemplate (the instance's `subject_override` takes precedence, then the default template).
3. The email is sent via the Resend API with the PDF attached.
4. A `GenerationRecord` is created with `was_emailed = True`.
5. The instance's `follow_up_date` is automatically set (typically 5-7 days out).
6. The instance's `follow_up_status` is updated.

### Requirements

- The recipient must have an email address.
- `RESEND_API_KEY` and `FROM_EMAIL` must be configured in environment variables.
- At least one EmailTemplate must exist (with `is_default = True`).

---

## Tracking Follow-ups

### Viewing Follow-up Status

1. Navigate to **Portfolio > Resume Instances**.
2. The list view shows `follow_up_date` and `follow_up_status` columns.
3. Filter by status to find instances needing follow-up.

### Updating Follow-ups

1. Click into a Resume Instance.
2. Update:
   - `follow_up_status` — Change to reflect current state.
   - `follow_up_notes` — Record what happened.
   - `follow_up_date` — Set a new follow-up date if needed.
3. Click **Save**.

---

## Viewing Generation History

1. Navigate to **Portfolio > Generation Records**.
2. Each record shows:
   - Which instance was generated.
   - The archetype slug, format, color scheme, and length variant.
   - When it was generated.
   - Whether it was emailed.
3. This provides a complete audit trail of every resume generated and sent.

---

## Tips

- **Use "Save and continue editing"** when building archetypes — you need to save before the inline through-table forms appear.
- **Drag to sort** in Grappelli inlines — this is faster than manually entering sort_order numbers.
- **Preview before sending** — Use the instance download endpoint (`/download/instance/<id>/`) to review a PDF before emailing it.
- **Bulk operations** — Select multiple instances and use admin actions to send resumes in batch.
- **Cache invalidation is automatic** — After editing any content, the next resume generation will use the updated data. No manual cache clearing needed.
