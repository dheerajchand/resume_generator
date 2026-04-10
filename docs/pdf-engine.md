# PDF Engine & Document Generation

The resume generation engine lives in `resumes/core_services.py` and is responsible for rendering resume data into PDF, DOCX, RTF, and Markdown formats. The `ResumeGenerator` class is the primary interface.

---

## ResumeGenerator Class

### Overview

`ResumeGenerator` takes a flat data dictionary (produced by `portfolio/services.py`) and renders it into the requested format with a specified color scheme.

### Input: Data Dictionary

The data dictionary is assembled by `build_resume_data_from_db()` in `portfolio/services.py`. It contains:

- **Personal info**: name, title, email, phone, website, location, slogan, logo URL, footer text.
- **Professional summary**: The summary paragraph.
- **Positions**: List of positions, each with a list of responsibilities.
- **Achievements**: List of achievement texts.
- **Projects**: List of projects with descriptions and technologies.
- **Skills**: List of skill categories, each with a list of skills.
- **Archetype metadata**: Configuration values (max counts, display flags).

### Output Formats

| Format | Library | Extension | Description |
|--------|---------|-----------|-------------|
| PDF | ReportLab | `.pdf` | Full-featured layout with color schemes, headers, footers, and KeepTogether page-break control |
| DOCX | python-docx | `.docx` | Microsoft Word format with styled paragraphs and headings |
| RTF | PyRTF3 | `.rtf` | Rich Text Format for broad compatibility |
| Markdown | String templates | `.md` | Plain-text Markdown suitable for GitHub, plain-text emails, etc. |

---

## PDF Generation (ReportLab)

PDF is the primary and most full-featured output format.

### Page Layout

- **Page size**: Letter (8.5" x 11") or A4.
- **Margins**: Configured for professional appearance (typically 0.5"-0.75" on all sides).
- **Header**: Contains name, title, contact information, and optionally a logo.
- **Footer**: Contains footer text from PersonalInfo and page numbers.
- **Body**: Structured sections for summary, experience, achievements, projects, and skills.

### KeepTogether Architecture

ReportLab's `KeepTogether` flowable is used extensively to prevent awkward page breaks. The system wraps logical content groups so they are not split across pages:

#### Position Blocks
Each position is wrapped in a `KeepTogether` block that includes:
- Position header (title, company, location, dates)
- Subtitle (if present)
- All responsibility bullet points for that position

If the entire block does not fit on the current page, ReportLab moves the whole block to the next page.

#### Project Blocks
Each project is similarly wrapped:
- Project name and dates
- Description text
- Impact statement
- Technical details (if enabled)
- Technology list

#### Achievement Blocks
Achievements are typically short enough to fit individually, but the entire achievements section header and first few items are kept together to avoid orphaned headers.

#### Skill Category Blocks
Each skill category and its skills are kept together.

### Why KeepTogether Matters

Without `KeepTogether`, ReportLab would break content at any point that exceeds the page boundary. This could result in:
- A position header on page 1 with its responsibilities on page 2.
- A project name separated from its description.
- A section header with no content below it (orphaned header).

`KeepTogether` prevents all of these by treating each logical unit as atomic.

### Font Configuration

The PDF engine uses specific fonts configured in the ReportLab canvas. System fonts must be available in the Docker container. The Dockerfile installs required font packages.

---

## Color Schemes

Eight color schemes are available, each defining a coordinated palette for headers, text, accents, and backgrounds.

### Available Schemes

| Slug | Name | Character |
|------|------|-----------|
| `default_professional` | Default Professional | Clean, traditional black/dark gray with subtle blue accents |
| `corporate_blue` | Corporate Blue | Navy and steel blue, formal corporate aesthetic |
| `modern_tech` | Modern Tech | Contemporary palette with tech-industry-appropriate colors |
| `modern_clean` | Modern Clean | Minimalist design with generous whitespace and muted tones |
| `satellite_imagery` | Satellite Imagery | Earth tones inspired by satellite/remote sensing imagery |
| `terrain_mapping` | Terrain Mapping | Topographic greens and browns from terrain visualization |
| `cartographic_professional` | Cartographic Professional | Muted cartographic palette — professional and distinctive |
| `topographic_classic` | Topographic Classic | Classic USGS-style topographic map colors |

### Color Scheme Structure

Each scheme defines colors for:

| Element | Description |
|---------|-------------|
| **Header background** | Background color for the resume header section |
| **Header text** | Text color for name, title in the header |
| **Section headers** | Color for section titles (Experience, Skills, etc.) |
| **Body text** | Primary body text color |
| **Accent** | Used for links, highlights, subtle decorative elements |
| **Line/rule** | Horizontal rules separating sections |
| **Bullet** | Bullet point color |

### Choosing a Color Scheme

- **`default_professional`** — Safe for any industry. When in doubt, use this.
- **`corporate_blue`** — Finance, consulting, enterprise.
- **`modern_tech`** — Startups, tech companies, engineering roles.
- **`modern_clean`** — Design-conscious organizations, product roles.
- **`satellite_imagery` / `terrain_mapping` / `cartographic_professional` / `topographic_classic`** — GIS, geospatial, environmental science, cartography. These schemes signal domain expertise through visual language.

---

## Length Variants

Length variants control content truncation before rendering.

| Variant | Target Pages | Truncation Strategy |
|---------|-------------|---------------------|
| `long` | Full (typically 4-8 pages) | No truncation. All content selected by the archetype is included, subject to `max_*` limits. |
| `short` | 3-4 pages | Moderate truncation. Reduces number of positions, responsibilities per position, achievements, and projects. |
| `brief` | 1-2 pages | Aggressive truncation. Only the highest-priority items (lowest `sort_order`) survive. |

### Truncation Logic

Length truncation is handled by `master_resume_generator.py` (legacy module, still in use for this purpose). The process:

1. Receives the full data dictionary from `build_resume_data_from_db()`.
2. Applies length-specific limits:
   - **Positions**: `long` keeps all, `short` keeps ~4-5, `brief` keeps ~2-3.
   - **Responsibilities per position**: Further reduced from `max_responsibilities_per_job`.
   - **Achievements**: Reduced from `max_achievements`.
   - **Projects**: Reduced proportionally.
3. Returns the trimmed data dictionary.
4. The trimmed data is passed to `ResumeGenerator` for rendering.

**Important**: Truncation respects `sort_order`. Items with lower sort_order values are retained first. This is why sort ordering matters — it determines survival priority.

---

## DOCX Generation

DOCX output uses the `python-docx` library:

- Creates a Word document with styled headings and paragraphs.
- Applies heading styles for section names.
- Uses bullet-point paragraph styles for responsibilities.
- Does not support the full color scheme system (Word style-dependent).
- Suitable for situations where the recipient needs to edit the resume.

---

## RTF Generation

RTF output uses `PyRTF3`:

- Generates Rich Text Format documents.
- Broad compatibility with word processors.
- Basic formatting: bold, italic, bullet points.
- Limited color scheme support.

---

## Markdown Generation

Markdown output is generated via string templates:

- Pure text with Markdown formatting.
- Headers (`#`, `##`, `###`) for sections.
- Lists (`-`) for responsibilities, achievements, technologies.
- Bold (`**`) for position titles and company names.
- No color scheme (plain text).
- Useful for plain-text emails, GitHub profiles, or further processing.

---

## Generation Flow

```
portfolio/services.py                  master_resume_generator.py
build_resume_data_from_db(slug)  ──>  apply_length_truncation(data, variant)
         │                                       │
         │ full data dict                        │ trimmed data dict
         ▼                                       ▼
                    resumes/core_services.py
                    ResumeGenerator.generate(data, format, color)
                              │
                    ┌─────────┼──────────┐──────────┐
                    ▼         ▼          ▼          ▼
                   PDF      DOCX       RTF        MD
                (ReportLab) (docx)   (PyRTF3)  (strings)
                    │         │          │          │
                    ▼         ▼          ▼          ▼
                 bytes     bytes      bytes      text
```

---

## Extending the Engine

### Adding a New Color Scheme

1. Define the color palette in `core_services.py` (follow the existing scheme structure).
2. Add the scheme slug to the available choices.
3. Test with all archetypes and length variants.

### Adding a New Output Format

1. Add a new method to `ResumeGenerator` (e.g., `generate_html()`).
2. Register the format type in the view layer.
3. Add the format to the download form's dropdown.
4. Update `generate_all_resumes.py` to include the new format in batch generation.

### Modifying Page Layout

1. Adjust margins, fonts, and spacing in the PDF generation methods.
2. Test across multiple archetypes — layout changes affect all resumes.
3. Pay special attention to KeepTogether blocks — margin changes can cause content to overflow.
