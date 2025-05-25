# Professional Resume Generator System

A comprehensive Python-based resume generation system that creates professional, multi-format resumes from structured JSON data. Generates PDF, DOCX, and RTF formats with configurable color schemes and precise typography for maximum impact and ATS compatibility.

## Features

- **Multiple Resume Versions**: Six targeted versions (Research, Technical, Software Engineer, Consulting, Comprehensive, Product Marketing)
- **Multi-Format Output**: PDF, DOCX, and RTF formats for maximum compatibility
- **Dynamic Color Schemes**: Professional themes with custom color scheme generation tools
- **Structured Data Management**: JSON-based content with automated data generation
- **Professional Layout**: 2-page optimized design with precise typography and spacing
- **Flexible Generation Options**: Individual, batch, or selective generation capabilities
- **Color Scheme Comparison**: Generate same resume with different color schemes for A/B testing
- **Comprehensive Management**: Full lifecycle management from data generation to final output

## Quick Start

### 1. Install Dependencies
```bash
pip install reportlab python-docx
```

### 2. Initialize System and Generate Data
```bash
# Check system setup
python resume_manager.py --check

# Generate all resume data with default color scheme
python resume_manager.py --generate-data

# List available versions and status
python resume_manager.py --list
```

### 3. Generate Your First Resume
```bash
# Generate the default software engineer version in PDF
python resume_manager.py --version software --format pdf

# Generate all formats for a specific version
python resume_manager.py --version software --all-formats

# Generate all versions in PDF format
python resume_manager.py --all-versions --format pdf
```

## System Architecture

The resume generation system consists of five main components:

| Script | Purpose | Primary Use Case |
|--------|---------|------------------|
| `resume_manager.py` | **Main controller** - Individual and batch resume management | Daily use, specific version generation |
| `resume_data_generator.py` | Creates structured JSON data files with professional content | Initial setup, content updates |
| `reportlab_resume.py` | Core resume generation engine using ReportLab | Direct generation control |
| `color_scheme_generator_tool.py` | Custom color scheme creation and preview | Design customization |
| `generate_all_resumes.py` | Legacy batch generator | Complete system regeneration |

## Resume Versions

The system generates six distinct resume versions, each optimized for different career focuses:

| Version Key | Professional Title | Target Roles | Key Emphasis |
|-------------|-------------------|--------------|--------------|
| `research` | Director of Research and Analysis | Academic, NGO, Policy | Applied research leadership, community impact |
| `technical` | Senior Geospatial Data Engineer & Technical Architect | Data engineering, Architecture | Big data, geospatial platforms, system design |
| `software` | Senior Software Engineer & Geospatial Platform Architect | Software engineering, Development | Full-stack development, platform engineering |
| `consulting` | Data Analytics & Technology Consultant | Consulting, Strategy | Strategic advisory, technology consulting |
| `comprehensive` | Research, Data Analytics & Engineering Professional | Executive, Senior roles | Complete career history and technical depth |
| `marketing` | Senior Product Marketing Manager | Product marketing, Go-to-market | Market research, product positioning |

## Color Schemes

### Built-in Professional Themes

#### Default Professional (Green, Gold, Burgundy)
```bash
python resume_manager.py --generate-data --color-scheme default_professional
```
- **Best for**: Creative, consulting, and distinctive professional roles
- **Colors**: Forest Green (#228B22), Dark Goldenrod (#B8860B), Deep Burgundy (#722F37)

#### Corporate Blue (Navy, Gray, Steel Blue)
```bash
python resume_manager.py --generate-data --color-scheme corporate_blue
```
- **Best for**: Traditional industries, finance, legal, enterprise roles
- **Colors**: Navy Blue (#1F4E79), Charcoal (#333333), Steel Blue (#4682B4)

#### Modern Tech (Teal, Orange, Gray)
```bash
python resume_manager.py --generate-data --color-scheme modern_tech
```
- **Best for**: Startup environments, tech companies, innovative roles
- **Colors**: Deep Teal (#2C5F5D), Vibrant Orange (#FF6B35)

### Custom Color Scheme Creation

Generate custom color schemes using the color scheme generator tool:

```bash
# Create industry-specific schemes
python color_scheme_generator_tool.py --industry finance --name corporate_finance --preview

# Create brand-based schemes
python color_scheme_generator_tool.py --brand '#1F4E79' '#FF6B35' --name custom_brand --preview

# Create color theory-based schemes
python color_scheme_generator_tool.py --complementary '#228B22' --name nature_complement --preview
```

## Resume Manager - Complete Usage Guide

### Essential Commands

#### System Setup and Data Management
```bash
# Check system configuration and dependencies
python resume_manager.py --check

# Generate resume data with default professional color scheme
python resume_manager.py --generate-data

# Generate data with specific color scheme
python resume_manager.py --generate-data --color-scheme corporate_blue

# List all available versions, color schemes, and status
python resume_manager.py --list

# Clean output directories
python resume_manager.py --clean
```

#### Individual Resume Generation
```bash
# Generate specific version in PDF format
python resume_manager.py --version software --format pdf

# Generate specific version in DOCX format
python resume_manager.py --version research --format docx

# Generate specific version in RTF format
python resume_manager.py --version consulting --format rtf
```

#### Batch Generation Operations
```bash
# Generate all formats (PDF, DOCX, RTF) for one version
python resume_manager.py --version technical --all-formats

# Generate all versions in PDF format
python resume_manager.py --all-versions --format pdf

# Generate all versions in all formats (18 total files)
python resume_manager.py --everything
```

#### Color Scheme Comparison and Testing
```bash
# Generate same version with multiple color schemes for comparison
python resume_manager.py --version software --color-comparison default_professional corporate_blue modern_tech
```

### Advanced Workflows

#### Job Application Workflow
```bash
# For software engineering positions
python resume_manager.py --version software --format pdf

# For data engineering roles
python resume_manager.py --version technical --format pdf

# For research positions
python resume_manager.py --version research --format pdf

# For consulting opportunities
python resume_manager.py --version consulting --all-formats
```

#### Color Scheme A/B Testing
```bash
# Test corporate blue for traditional company application
python resume_manager.py --generate-data --color-scheme corporate_blue
python resume_manager.py --version software --format pdf

# Test modern tech for startup application
python resume_manager.py --generate-data --color-scheme modern_tech
python resume_manager.py --version software --format pdf

# Compare outputs and select preferred version
```

#### Complete System Refresh
```bash
# Clean slate regeneration
python resume_manager.py --clean
python resume_manager.py --generate-data --color-scheme default_professional
python resume_manager.py --everything
```

## Command Reference

### Resume Manager Options

| Command | Arguments | Description |
|---------|-----------|-------------|
| `--check` | None | Verify system setup and dependencies |
| `--generate-data` | `--color-scheme SCHEME` | Create JSON data files with specified colors |
| `--list` | None | Show available resume versions and current status |
| `--version` | `research\|technical\|software\|consulting\|comprehensive\|marketing` | Specify target resume version |
| `--format` | `pdf\|docx\|rtf` | Specify output format (default: pdf) |
| `--all-formats` | None | Generate all formats for specified version |
| `--all-versions` | None | Generate all versions in specified format |
| `--everything` | None | Generate all versions in all formats |
| `--color-comparison` | `SCHEME1 SCHEME2 ...` | Generate version with multiple color schemes |
| `--clean` | `[VERSION] [SCHEME]` | Remove output directories (optional: specific targets) |

### Color Scheme Generator Options

| Command | Arguments | Description |
|---------|----------|-------------|
| `--monochromatic` | `HEX_COLOR` | Generate monochromatic scheme from base color |
| `--complementary` | `HEX_COLOR` | Generate complementary color scheme |
| `--triadic` | `HEX_COLOR` | Generate triadic color scheme |
| `--industry` | `finance\|legal\|healthcare\|technology\|consulting\|creative\|education\|nonprofit` | Generate industry-appropriate scheme |
| `--brand` | `HEX_COLOR1 HEX_COLOR2 [HEX_COLOR3]` | Generate scheme from brand colors |
| `--name` | `SCHEME_NAME` | Required name for the color scheme |
| `--preview` | None | Show color preview before saving |

## Project Structure

```
resume-generator/
├── resume_manager.py              # Main controller for resume generation
├── resume_data_generator.py       # Professional data generation with color schemes
├── reportlab_resume.py            # Core resume generation engine
├── color_scheme_generator_tool.py # Custom color scheme creation tool
├── generate_all_resumes.py        # Legacy batch generation script
├── color_schemes/                 # Color scheme configuration files
│   ├── default_professional.json
│   ├── corporate_blue.json
│   ├── modern_tech.json
│   └── [custom_schemes].json
├── inputs/                        # Generated JSON data and configurations
│   ├── dheeraj_chand_research_focused/
│   │   ├── resume_data.json       # Research-focused content
│   │   └── config.json           # Color and styling configuration
│   ├── dheeraj_chand_technical_detailed/
│   │   ├── resume_data.json       # Technical engineering content
│   │   └── config.json           # Configuration
│   ├── dheeraj_chand_software_engineer/  # DEFAULT VERSION
│   │   ├── resume_data.json       # Software engineering content
│   │   └── config.json           # Configuration
│   ├── dheeraj_chand_consulting_minimal/
│   │   ├── resume_data.json       # Consulting-focused content
│   │   └── config.json           # Configuration
│   ├── dheeraj_chand_comprehensive_full/
│   │   ├── resume_data.json       # Complete work history
│   │   └── config.json           # Configuration
│   └── dheeraj_chand_product_marketing/
│       ├── resume_data.json       # Product marketing content
│       └── config.json           # Configuration
└── outputs/                       # Generated resumes (organized by version/scheme/format)
    ├── research/
    │   └── default_professional/
    │       ├── pdf/research_default_professional.pdf
    │       ├── docx/research_default_professional.docx
    │       └── rtf/research_default_professional.rtf
    ├── technical/
    ├── software/
    ├── consulting/
    ├── comprehensive/
    └── marketing/
```

## Data Structure

### Resume Data Structure (`resume_data.json`)
```json
{
  "personal_info": {
    "name": "DHEERAJ CHAND",
    "title": "Professional Title",
    "phone": "(202) 550-7110",
    "email": "Dheeraj.Chand@gmail.com",
    "website": "https://www.dheerajchand.com",
    "linkedin": "https://www.linkedin.com/in/dheerajchand/"
  },
  "summary": "Professional summary paragraph...",
  "competencies": {
    "Category Name": [
      "Skill or competency item",
      "Another skill item"
    ]
  },
  "experience": [
    {
      "title": "JOB TITLE",
      "company": "Company Name, Location",
      "dates": "Start Date – End Date",
      "subtitle": "Optional job subtitle",
      "responsibilities": [
        "Responsibility or achievement bullet point",
        "Another responsibility bullet point"
      ]
    }
  ],
  "achievements": {
    "Achievement Category": [
      "Specific achievement or impact",
      "Another achievement"
    ]
  }
}
```

### Color Configuration Structure (`config.json`)
```json
{
  "NAME_COLOR": "#228B22",
  "TITLE_COLOR": "#B8860B",
  "SECTION_HEADER_COLOR": "#B8860B",
  "JOB_TITLE_COLOR": "#722F37",
  "ACCENT_COLOR": "#722F37",
  "COMPETENCY_HEADER_COLOR": "#228B22",
  "SUBTITLE_COLOR": "#228B22",
  "LINK_COLOR": "#B8860B",
  "DARK_TEXT_COLOR": "#333333",
  "MEDIUM_TEXT_COLOR": "#666666",
  "LIGHT_TEXT_COLOR": "#999999",

  "FONT_MAIN": "Helvetica",
  "FONT_BOLD": "Helvetica-Bold",
  "FONT_ITALIC": "Helvetica-Oblique",

  "NAME_SIZE": 24,
  "TITLE_SIZE": 14,
  "SECTION_HEADER_SIZE": 12,
  "JOB_TITLE_SIZE": 11,
  "BODY_SIZE": 9,
  "CONTACT_SIZE": 9,

  "PAGE_MARGIN": 0.6,
  "SECTION_SPACING": 0.12,
  "PARAGRAPH_SPACING": 0.06,
  "LINE_SPACING": 1.15,
  "JOB_SPACING": 6,
  "CATEGORY_SPACING": 4,
  "MAX_PAGES": 2,
  "BULLET_CHAR": "▸"
}
```

## Customization and Extension

### Adding New Resume Versions

1. **Create data function** in `resume_data_generator.py`:
```python
def create_new_version_data():
    """Create data for new version"""
    return {
        'personal_info': {
            'name': 'DHEERAJ CHAND',
            'title': 'New Professional Title',
            # ... personal details
        },
        'summary': 'Targeted professional summary...',
        'competencies': {
            'Category': ['Skills list']
        },
        'experience': [
            # Job experience entries
        ],
        'achievements': {
            'Category': ['Achievement list']
        }
    }
```

2. **Update main generation function** to include new version
3. **Add to resume manager** `self.versions` dictionary

### Creating Custom Color Schemes

Use the color scheme generator tool for professional results:

```bash
# Industry-based schemes
python color_scheme_generator_tool.py --industry healthcare --name medical_professional --preview

# Brand color schemes
python color_scheme_generator_tool.py --brand '#FF0000' '#0000FF' --name company_colors --preview

# Color theory schemes
python color_scheme_generator_tool.py --triadic '#8B4513' --name earth_tones --preview
```

## Professional Usage Guidelines

### Resume Version Selection Strategy
- **Software Engineering**: `software` - Comprehensive technical platform development
- **Data Engineering**: `technical` - Big data, geospatial systems, architecture
- **Research Roles**: `research` - Applied research, community impact, methodology
- **Consulting**: `consulting` - Strategic advisory, technology transformation
- **Executive Positions**: `comprehensive` - Complete career overview
- **Product Marketing**: `marketing` - Go-to-market, customer insights, positioning

### Color Scheme Selection by Industry
- **Traditional Industries** (Banking, Legal, Healthcare): `corporate_blue`
- **Creative and Consulting**: `default_professional`
- **Technology and Startups**: `modern_tech`
- **Custom Branding**: Generate custom schemes with brand colors

### Format Selection by Use Case
- **Online Applications**: PDF (universal compatibility, maintains formatting)
- **ATS Systems**: DOCX (optimized for parsing, machine-readable)
- **Print Submissions**: PDF (high-quality printing, consistent rendering)
- **Collaborative Review**: DOCX (easy editing and comments)
- **Maximum Compatibility**: RTF (cross-platform, legacy system support)

## Troubleshooting

### Common Issues and Solutions

#### Setup Problems
```bash
# Missing dependencies
pip install reportlab python-docx

# System check
python resume_manager.py --check

# Permission issues (Unix/Linux)
chmod +x *.py
```

#### Generation Issues
```bash
# Missing input data
python resume_manager.py --generate-data
python resume_manager.py --list

# Clean and regenerate
python resume_manager.py --clean
python resume_manager.py --generate-data --color-scheme default_professional
python resume_manager.py --version software --format pdf
```

#### Content and Formatting Issues
- **Content exceeds 2 pages**: Edit JSON data files to reduce content length
- **Colors not displaying**: Verify hex color format (#RRGGBB) in config files
- **Font rendering issues**: ReportLab uses built-in fonts; custom fonts require additional setup
- **Spacing problems**: Adjust layout parameters in config.json files

### Performance Optimization
- **Quick iterations**: Use PDF format only during development
- **Batch operations**: Use `--everything` for complete regeneration
- **Storage management**: Use `--clean` periodically to manage disk space

## Technical Highlights

### Professional Experience Showcased
- **20+ years** comprehensive data engineering and software development
- **Apache Spark/Sedona**: Billion-record geospatial processing expertise
- **Platform Architecture**: Multi-tenant SaaS platforms (BALLISTA, DAMON, SimCrisis)
- **Technology Integration**: ESRI, OSGeo, SAFE FME geospatial technology stacks
- **Team Leadership**: Engineering teams up to 11 professionals
- **Performance Engineering**: 57% ETL improvements, 88% targeting efficacy gains

### Key Technologies and Achievements
- **Programming**: Python (Django/GeoDjango, PySpark), Scala (Spark), JavaScript, SQL
- **Platforms**: AWS, Snowflake, PostgreSQL/PostGIS, MongoDB, distributed systems
- **Geospatial**: Advanced PostGIS algorithms, spatial clustering, boundary estimation
- **Big Data**: Multi-terabyte processing, real-time analytics, fraud detection systems

---

*This professional resume generation system demonstrates expertise in data engineering, geospatial platforms, and full-stack software development with emphasis on scalable system architecture and production platform development.*
