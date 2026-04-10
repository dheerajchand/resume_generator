# Resume Types (Archetypes)

Archetypes are the central organizing concept in the Resume Generator. Each archetype defines a domain-specific resume narrative by selecting which content to include, how much to show, and how to present it.

---

## How Archetypes Work

An archetype is not a template in the traditional sense — it does not define layout or formatting. Instead, it acts as a **content filter and organizer**:

1. **Selects content** — Which positions, achievements, projects, and skill categories to include.
2. **Orders content** — Each selected item has a `sort_order` specific to this archetype, independent of the item's default order.
3. **Controls density** — Settings like `max_responsibilities_per_job` and `max_achievements` limit how much detail is shown.
4. **Chooses presentation** — Flags like `show_project_technical_details` and `competency_detail_level` control which fields are rendered.
5. **Provides narrative** — The ProfessionalSummary gives each archetype a unique opening paragraph.

The same underlying content (positions, skills, etc.) can appear across multiple archetypes, presented differently each time.

---

## Archetype Configuration Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | String | Human-readable archetype name |
| `slug` | String | URL-safe identifier, used in URLs and file names |
| `description` | Text | Internal description of what this archetype emphasizes |
| `is_electoral` | Boolean | Flags this as an electoral/political consulting archetype. May trigger special formatting or content selection. |
| `max_achievements` | Integer | Maximum number of achievements to display. Achievements beyond this count are omitted. |
| `max_responsibilities_per_job` | Integer | Maximum bullet points shown per position. Responsibilities beyond this count are omitted. |
| `siege_analytics_max` | Integer | Maximum items for the Siege Analytics section, if applicable |
| `show_project_technical_details` | Boolean | When `True`, shows the `technical_description` field on projects. When `False`, only the general `description` and `impact` are shown. |
| `competency_detail_level` | Varies | Controls whether the `detail` field on Skills is displayed. Higher levels show more skill detail. |

---

## Content Relationships

Each archetype connects to content via many-to-many through-tables:

### Positions (ArchetypePosition)
- **What**: Which work experience entries to include.
- **Sort order**: Independent of the position's default `sort_order`. You might put a GIS role first in a geospatial archetype but third in a data science archetype.
- **Responsibilities**: Each position brings all its responsibilities, truncated to `max_responsibilities_per_job`.

### Achievements (ArchetypeAchievement)
- **What**: Which standalone achievements to highlight.
- **Sort order**: Archetype-specific.
- **Truncation**: Only the first `max_achievements` are shown (after sorting).

### Projects (ArchetypeProject)
- **What**: Which portfolio projects to feature.
- **Sort order**: Archetype-specific.
- **Detail level**: Controlled by `show_project_technical_details`.

### Skill Categories (ArchetypeSkillCategory)
- **What**: Which skill groupings to include.
- **Sort order**: Archetype-specific.
- **Detail level**: Controlled by `competency_detail_level`.
- **Skills within categories**: All skills in a selected category are included, in their category-level sort order.

### Professional Summary
- **What**: A one-to-one summary paragraph.
- **Purpose**: The opening statement at the top of the resume, tailored to this archetype's domain.
- **Override**: ResumeInstances can override this with `summary_override`.

---

## Designing an Archetype

When creating a new archetype, think about:

### 1. Target Audience
Who will read this resume? A hiring manager at a tech company? A political campaign? A GIS consultancy? The audience determines which content to emphasize.

### 2. Content Selection
- **Positions**: Include roles most relevant to this domain. Omit unrelated positions.
- **Achievements**: Choose achievements that demonstrate domain expertise.
- **Projects**: Feature projects that showcase relevant technical skills.
- **Skills**: Select skill categories that match the job requirements.

### 3. Density Controls
- **Data-heavy roles** (data science, engineering): Higher `max_responsibilities_per_job` (5-7) to show technical depth.
- **Executive/consulting roles**: Lower `max_responsibilities_per_job` (3-4) with more emphasis on impact.
- **Achievements**: 3-5 is typical. More for senior roles, fewer for focused applications.

### 4. Presentation Flags
- **Technical audiences**: `show_project_technical_details = True`, higher `competency_detail_level`.
- **Business audiences**: `show_project_technical_details = False`, lower `competency_detail_level`.
- **Electoral/political**: `is_electoral = True` may trigger domain-specific formatting.

### 5. Professional Summary
Write a summary paragraph that:
- Opens with your professional identity in the context of this domain.
- Highlights 2-3 key strengths relevant to the target audience.
- Mentions years of experience or notable accomplishments.
- Closes with what you bring to the role.

---

## Creating a New Archetype Step-by-Step

### Step 1: Plan

Before touching the admin, decide:
- [ ] Archetype name and slug
- [ ] Which positions to include and in what order
- [ ] Which achievements to feature
- [ ] Which projects to showcase
- [ ] Which skill categories to include
- [ ] Max responsibilities per job
- [ ] Max achievements
- [ ] Whether to show technical project details
- [ ] Competency detail level
- [ ] Professional summary text

### Step 2: Create the Archetype Record

1. Go to **Portfolio > Resume Archetypes > Add**.
2. Fill in name, slug, description.
3. Set all configuration fields.
4. Click **Save and continue editing**.

### Step 3: Add Content

After saving, the inline sections appear:

1. **Add positions**: Click "Add another Archetype Position" for each role. Select the position and set `sort_order` (0 = first).
2. **Add achievements**: Same pattern. Set `sort_order`.
3. **Add projects**: Same pattern. Set `sort_order`.
4. **Add skill categories**: Same pattern. Set `sort_order`.

### Step 4: Write the Summary

1. In the **Professional Summary** inline, write the summary text.
2. Click **Save**.

### Step 5: Test

1. Go to `http://localhost:8000/` (or the production URL).
2. Select your new archetype from the dropdown.
3. Choose a length variant, color scheme, and format.
4. Download and review.
5. Iterate on content selection and summary until satisfied.

---

## Length Variants and Archetypes

Each archetype can be generated in three length variants:

| Variant | Target | What Happens |
|---------|--------|-------------|
| `long` | Full content | All selected content is included, respecting max limits |
| `short` | 3-4 pages | Content is truncated: fewer positions, fewer responsibilities, fewer projects |
| `brief` | 1-2 pages | Aggressive truncation: only the most important items survive |

Length truncation is handled by `master_resume_generator.py` and applies uniformly — it trims from the bottom of each sorted list. This means your `sort_order` values directly determine what survives truncation: lower sort_order items appear first and are more likely to be retained in shorter variants.

**Tip**: Put your most impactful content at `sort_order = 0` so it always appears, even in the `brief` variant.

---

## Archetype vs. Instance

| Concept | Archetype | Instance |
|---------|-----------|----------|
| **Purpose** | Define a domain narrative | Target a specific opportunity |
| **Content selection** | Chooses positions, achievements, etc. | Inherits from archetype |
| **Summary** | ProfessionalSummary (general to domain) | Can override with `summary_override` |
| **Recipient** | None | Links to a specific Recipient |
| **Tracking** | No tracking | Follow-up dates, status, generation records |
| **Email** | Cannot email directly | Can be emailed via admin action |

Think of archetypes as reusable templates and instances as specific applications of those templates.

---

## Best Practices

1. **Start with 3-5 archetypes** covering your main professional domains. You can always add more.
2. **Reuse content across archetypes** — the same position can appear in multiple archetypes with different sort orders.
3. **Write domain-specific summaries** — generic summaries waste the most valuable real estate on the resume.
4. **Test all three length variants** — ensure the `brief` variant still tells a coherent story.
5. **Review sort orders carefully** — they determine both display order and truncation priority.
6. **Use `text_neutral` on responsibilities** when a bullet point is too domain-specific for a general archetype.
