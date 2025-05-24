# Professional Resume Generator

A Python-based resume generation system that creates professional, multi-format resumes from structured JSON data. Generates PDF, DOCX, and RTF formats with configurable color schemes and precise typography for maximum impact and ATS compatibility.

## Features

- **Multiple Resume Versions**: Generate different versions targeting specific roles (Research, Technical, Software Engineer, Consulting, Comprehensive, Product Marketing)
- **Multi-Format Output**: PDF, DOCX, and RTF formats for maximum compatibility
- **Configurable Color Schemes**: Professional, Corporate Blue, Modern Tech, and custom themes
- **Structured Data**: JSON-based content management with detailed professional information
- **Professional Layout**: 2-page optimized design with precise typography and spacing
- **Batch Generation**: Create all resume versions with single commands
- **Individual Control**: Generate specific versions, formats, or combinations as needed
- **Error Handling**: Comprehensive validation and fallback configurations

## Quick Start

### 1. Install Dependencies
```bash
pip install reportlab python-docx
```

### 2. Generate All Resume Data and Versions
```bash
# Generate everything at once (recommended for first-time setup)
python generate_all_dheeraj_resumes.py
```

### 3. Individual Resume Generation
```bash
# Generate specific version
python resume_manager.py --version software --format pdf

# Generate all formats for one version
python resume_manager.py --version technical --all-formats

# List available versions
python resume_manager.py --list
```

## System Overview

The resume generation system consists of three main scripts:

| Script | Purpose | Use Case |
|--------|---------|----------|
| `resume_data_generator.py` | Creates JSON data files with professional content | Initial setup, adding new versions |
| `reportlab_resume.py` | Core resume generation engine | Direct control, custom configurations |
| `generate_all_dheeraj_resumes.py` | Batch generator for all versions | Complete regeneration, first-time setup |
| `resume_manager.py` | Individual resume control and management | Daily use, specific version updates |

## Resume Versions

The system generates six distinct resume versions, each optimized for different career focuses:

| Version | Key Focus | Target Audience | Professional Title |
|---------|-----------|-----------------|-------------------|
| `research` | Applied research leadership, community impact | Research organizations, NGOs, policy roles | Director of Research and Analysis |
| `technical` | Data engineering, geospatial platforms, big data | Technical teams, engineering managers | Senior Geospatial Data Engineer & Technical Architect |
| `software` | Platform development, full-stack engineering | Software engineering roles, tech companies | Senior Software Engineer & Geospatial Platform Architect |
| `consulting` | Strategic advisory, technology consulting | Consulting firms, strategy roles | Data Analytics & Technology Consultant |
| `comprehensive` | Complete work history and technical depth | Executive roles, comprehensive review | Research, Data Analytics & Engineering Professional |
| `marketing` | Product marketing, go-to-market strategy | Marketing roles, product management | Senior Product Marketing Manager |

## Color Schemes

The system supports multiple professional color schemes:

### Available Schemes

#### Default Professional (Green, Gold, Burgundy)
```bash
python resume_data_generator.py --color-scheme default_professional
```
- **Primary**: Forest Green (#228B22) - Name, competency headers
- **Secondary**: Dark Goldenrod (#B8860B) - Section headers, links
- **Accent**: Deep Burgundy (#722F37) - Job titles, highlights
- **Best for**: Creative, consulting, and distinctive professional roles

#### Corporate Blue (Navy, Gray, Steel Blue)
```bash
python resume_data_generator.py --color-scheme corporate_blue
```
- **Primary**: Navy Blue (#1F4E79) - Name, competency headers
- **Secondary**: Charcoal (#333333) - Section headers
- **Accent**: Steel Blue (#4682B4) - Job titles, links
- **Best for**: Traditional industries, finance, legal, enterprise roles

#### Modern Tech (Teal, Orange, Gray)
```bash
python resume_data_generator.py --color-scheme modern_tech
```
- **Primary**: Deep Teal (#2C5F5D) - Name, competency headers
- **Secondary**: Vibrant Orange (#FF6B35) - Section headers, accents
- **Accent**: Deep Teal (#2C5F5D) - Job titles
- **Best for**: Startup environments, tech companies, innovative roles

#### Elegant Purple (Purple, Gold, Gray)
```bash
python resume_data_generator.py --color-scheme elegant_purple
```
- **Primary**: Rebecca Purple (#663399) - Name, competency headers
- **Secondary**: Goldenrod (#DAA520) - Section headers, accents
- **Accent**: Rebecca Purple (#663399) - Job titles
- **Best for**: Creative roles, design positions, marketing roles

### Using Color Schemes

#### Generate Data with Specific Color Schemes
```bash
# Generate with default professional colors
python resume_data_generator.py --color-scheme default_professional

# Generate with corporate blue theme
python resume_data_generator.py --color-scheme corporate_blue

# Generate with modern tech colors
python resume_data_generator.py --color-scheme modern_tech
```

#### Generate Resumes with Different Colors
```bash
# Generate research version with corporate colors
python resume_manager.py --generate-data --color-scheme corporate_blue
python resume_manager.py --version research --format pdf

# Generate technical version with modern tech colors
python resume_manager.py --generate-data --color-scheme modern_tech
python resume_manager.py --version technical --all-formats
```

## Resume Manager - Complete Usage Guide

The `resume_manager.py` script provides granular control over resume generation:

### Basic Commands

#### Setup and Data Generation
```bash
# Check system setup
python resume_manager.py --check

# Generate resume data files
python resume_manager.py --generate-data

# Generate data with specific color scheme
python resume_manager.py --generate-data --color-scheme corporate_blue

# List available resume versions
python resume_manager.py --list
```

#### Single Resume Generation
```bash
# Generate specific version in PDF
python resume_manager.py --version software --format pdf

# Generate specific version in DOCX
python resume_manager.py --version research --format docx

# Generate specific version in RTF
python resume_manager.py --version consulting --format rtf
```

#### Multiple Format Generation
```bash
# Generate all formats for one version
python resume_manager.py --version technical --all-formats

# Generate all versions in PDF format
python resume_manager.py --all-versions --format pdf

# Generate all versions in all formats
python resume_manager.py --everything
```

#### Utility Commands
```bash
# Clean output directories
python resume_manager.py --clean

# Check system status
python resume_manager.py --check
```

### Resume Manager Examples

#### Daily Workflow Examples
```bash
# Update software engineer resume for job application
python resume_manager.py --version software --format pdf

# Create consulting version for client meeting
python resume_manager.py --version consulting --all-formats

# Generate research version for academic opportunity
python resume_manager.py --version research --format pdf
```

#### Batch Operations
```bash
# Regenerate all PDFs (fast)
python resume_manager.py --all-versions --format pdf

# Regenerate everything (comprehensive)
python resume_manager.py --everything

# Clean and regenerate specific version
python resume_manager.py --clean
python resume_manager.py --generate-data --color-scheme default_professional
python resume_manager.py --version software --all-formats
```

#### Color Scheme Testing
```bash
# Test different color schemes for same content
python resume_manager.py --generate-data --color-scheme corporate_blue
python resume_manager.py --version software --format pdf
# Review output, then try different scheme
python resume_manager.py --generate-data --color-scheme modern_tech
python resume_manager.py --version software --format pdf
```

### Resume Manager Command Reference

| Command | Options | Description |
|---------|---------|-------------|
| `--check` | None | Verify system setup and dependencies |
| `--generate-data` | `--color-scheme` | Create JSON data files with specified colors |
| `--list` | None | Show available resume versions and status |
| `--version` | `research\|technical\|software\|consulting\|comprehensive\|marketing` | Specify resume version |
| `--format` | `pdf\|docx\|rtf` | Specify output format |
| `--all-formats` | None | Generate all formats for specified version |
| `--all-versions` | None | Generate all versions in specified format |
| `--everything` | None | Generate all versions in all formats |
| `--clean` | None | Remove output directories |
| `--color-scheme` | `default_professional\|corporate_blue\|modern_tech\|elegant_purple` | Color theme selection |

## Project Structure

```
resume-generator/
├── resume_data_generator.py       # Professional data generation with color schemes
├── reportlab_resume.py            # Core resume generation engine (fixed version)
├── generate_all_dheeraj_resumes.py  # Batch generation script
├── resume_manager.py              # Individual resume control and management
├── color_schemes/                 # Predefined color scheme files
│   ├── default_professional.json  # Green, Gold, Burgundy theme
│   ├── corporate_blue.json        # Navy, Gray, Steel Blue theme
│   ├── modern_tech.json           # Teal, Orange, Gray theme
│   └── elegant_purple.json        # Purple, Gold, Gray theme
├── inputs/                        # JSON data and configuration
│   ├── dheeraj_chand_research_focused/
│   │   ├── resume_data.json       # Research-focused content
│   │   └── config.json           # Color and styling configuration
│   ├── dheeraj_chand_technical_detailed/
│   │   ├── resume_data.json       # Technical engineering content
│   │   └── config.json           # Configuration
│   ├── dheeraj_chand_software_engineer/
│   │   ├── resume_data.json       # Software engineering content (DEFAULT)
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
└── outputs/                       # Generated resumes
    ├── dheeraj_chand_research_focused/
    │   ├── pdf/resume.pdf
    │   ├── docx/resume.docx
    │   └── rtf/resume.rtf
    ├── dheeraj_chand_technical_detailed/
    ├── dheeraj_chand_software_engineer/
    ├── dheeraj_chand_consulting_minimal/
    ├── dheeraj_chand_comprehensive_full/
    └── dheeraj_chand_product_marketing/
```

## Data Structure & Configuration

### Resume Data JSON (`resume_data.json`)

Each resume version uses structured JSON containing complete professional information:

```json
{
  "personal_info": {
    "name": "DHEERAJ CHAND",
    "title": "Senior Software Engineer & Geospatial Platform Architect",
    "phone": "(202) 550-7110",
    "email": "Dheeraj.Chand@gmail.com",
    "website": "https://www.dheerajchand.com",
    "linkedin": "https://www.linkedin.com/in/dheerajchand/"
  },

  "summary": "Senior Software Engineer with 20+ years building scalable geospatial data platforms, web applications, and distributed analytical systems. Expert in full-stack development with deep specialization in Apache Spark/Sedona for big data geospatial processing...",

  "competencies": {
    "Programming & Development": [
      "Python: Django/GeoDjango, Flask, Pandas, PySpark, NumPy, SciKit-Learn",
      "JVM: Scala (Spark/Sedona), Java (GeoTools, enterprise applications), Groovy",
      "Web Technologies: JavaScript, React, d3.js, OpenLayers, jQuery, HTML/CSS"
    ],
    "Big Data & Geospatial Platforms": [
      "Apache Spark: PySpark, Spark SQL, Sedona (geospatial), distributed processing",
      "Geospatial Stack: PostGIS, ESRI ArcGIS, Quantum GIS, GRASS, OSGeo, SAFE FME",
      "Cloud Platforms: AWS (EC2, RDS, S3), Snowflake, Google Cloud, Microsoft Azure"
    ],
    "Software Architecture & DevOps": [
      "Distributed Systems: Multi-tenant SaaS, microservices, API design, scalability",
      "Geospatial Applications: Spatial algorithms, boundary estimation, clustering",
      "DevOps: Docker, Vagrant, CI/CD (GitLab, GitHub), Celery, Airflow, nginx"
    ]
  },

  "experience": [
    {
      "title": "PARTNER & SENIOR SOFTWARE ENGINEER",
      "company": "Siege Analytics, Austin, TX",
      "dates": "2005 – Present",
      "subtitle": "Geospatial Platform Architecture and Full-Stack Development",
      "responsibilities": [
        "Architected and engineered BALLISTA: GeoDjango redistricting platform serving thousands of analysts with real-time collaborative editing, Census integration, and legal compliance analysis",
        "Developed DAMON: Flask/PostGIS microservice using incomplete data for boundary estimation without machine learning, processing geographies at national scale",
        "Built scalable ETL pipelines using PySpark and Sedona processing billions of geospatial records with sub-hour latency requirements"
      ]
    },
    {
      "title": "DATA PRODUCTS MANAGER",
      "company": "Helm/Murmuration, Austin, TX",
      "dates": "2021 – 2023",
      "subtitle": "Enterprise Geospatial Data Platform Development and Team Leadership",
      "responsibilities": [
        "Led engineering team of 11 developers building enterprise-scale geospatial data platform for political organizing and issue advocacy",
        "Designed multi-tenant data warehouse integrating Census, Bureau of Labor Statistics, and National Council of Educational Statistics using Spark/PySpark",
        "Modernized legacy ETL systems using Scala/Spark and dbt, achieving 57% performance improvement in geospatial data processing"
      ]
    }
  ],

  "achievements": {
    "Geospatial Platform Development": [
      "Architected BALLISTA redistricting platform used by thousands of analysts nationwide with real-time collaborative editing and Census integration",
      "Built DAMON boundary estimation system achieving accurate geospatial results without machine learning using advanced PostGIS algorithms",
      "Developed SimCrisis econometric simulation platform with NetLogo multi-agent modeling and GeoDjango web interface"
    ],
    "Big Data & Performance Engineering": [
      "Implemented Spark/Sedona ETL optimizations achieving 57% performance improvement in geospatial data processing pipelines",
      "Built systems processing billions of spatial records with sub-hour latency using distributed Spark clusters on AWS",
      "Developed fraud detection algorithms processing multi-terabyte campaign finance datasets with real-time PostGIS spatial analysis"
    ]
  },

  "_metadata": {
    "version": "software_engineer",
    "created": "2025-01-20T15:30:00Z",
    "description": "Software engineer focused version emphasizing technical skills and platform development"
  }
}
```

### Configuration JSON (`config.json`)

Color scheme and styling configuration:

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
  "BULLET_CHAR": "▸",

  "_metadata": {
    "scheme_name": "default_professional",
    "created": "2025-01-20T15:30:00Z",
    "description": "Default professional color scheme for Dheeraj Chand resume"
  }
}
```

### Configuration Reference

#### Color Role Properties
| Property | Usage | Default (Professional) | Corporate Blue | Modern Tech |
|----------|-------|----------------------|----------------|-------------|
| `NAME_COLOR` | Header name | Forest Green (#228B22) | Navy Blue (#1F4E79) | Deep Teal (#2C5F5D) |
| `TITLE_COLOR` | Professional title | Dark Goldenrod (#B8860B) | Charcoal (#333333) | Vibrant Orange (#FF6B35) |
| `SECTION_HEADER_COLOR` | Section headers | Dark Goldenrod (#B8860B) | Charcoal (#333333) | Vibrant Orange (#FF6B35) |
| `JOB_TITLE_COLOR` | Job position titles | Deep Burgundy (#722F37) | Steel Blue (#4682B4) | Deep Teal (#2C5F5D) |
| `COMPETENCY_HEADER_COLOR` | Skill category headers | Forest Green (#228B22) | Navy Blue (#1F4E79) | Deep Teal (#2C5F5D) |
| `SUBTITLE_COLOR` | Job subtitles | Forest Green (#228B22) | Navy Blue (#1F4E79) | Deep Teal (#2C5F5D) |
| `LINK_COLOR` | Website, LinkedIn links | Dark Goldenrod (#B8860B) | Steel Blue (#4682B4) | Vibrant Orange (#FF6B35) |

#### Typography Properties
| Property | Default | Description |
|----------|---------|-------------|
| `FONT_MAIN` | `Helvetica` | Primary font family |
| `FONT_BOLD` | `Helvetica-Bold` | Bold text font |
| `FONT_ITALIC` | `Helvetica-Oblique` | Italic text font |
| `NAME_SIZE` | `24` | Name header font size (points) |
| `TITLE_SIZE` | `14` | Professional title font size |
| `SECTION_HEADER_SIZE` | `12` | Section header font size |
| `JOB_TITLE_SIZE` | `11` | Job title font size |
| `BODY_SIZE` | `9` | Body text font size |
| `CONTACT_SIZE` | `9` | Contact information font size |

#### Layout Properties
| Property | Default | Description |
|----------|---------|-------------|
| `PAGE_MARGIN` | `0.6` | Page margins in inches |
| `SECTION_SPACING` | `0.12` | Space between sections (inches) |
| `LINE_SPACING` | `1.15` | Line height multiplier |
| `JOB_SPACING` | `6` | Space between job entries (points) |
| `BULLET_CHAR` | `▸` | Character used for bullet points |

## Command Line Usage

### Core Resume Generation
```bash
# Basic usage
python reportlab_resume.py --format [pdf|docx|rtf|all] --basename [version_name]

# Generate PDF for software engineer version
python reportlab_resume.py --format pdf --basename dheeraj_chand_software_engineer

# Generate all formats for research version
python reportlab_resume.py --format all --basename dheeraj_chand_research_focused

# Use custom directories
python reportlab_resume.py --format pdf --basename dheeraj_chand_software_engineer --input-dir ./custom/inputs --output-dir ./custom/outputs
```

### Batch Generation Commands
```bash
# Generate all versions with all formats (18 total files)
python generate_all_dheeraj_resumes.py

# Generate with specific color scheme first
python resume_data_generator.py --color-scheme corporate_blue
python generate_all_dheeraj_resumes.py
```

### Resume Manager Commands (Recommended)
```bash
# Setup and data generation
python resume_manager.py --generate-data --color-scheme default_professional
python resume_manager.py --check
python resume_manager.py --list

# Individual resume generation
python resume_manager.py --version software --format pdf
python resume_manager.py --version research --all-formats
python resume_manager.py --all-versions --format pdf

# Complete regeneration
python resume_manager.py --clean
python resume_manager.py --everything
```

## Workflow Examples

### Job Application Workflow
```bash
# For a software engineering position
python resume_manager.py --version software --format pdf

# For a data engineering role
python resume_manager.py --version technical --format pdf

# For a research position
python resume_manager.py --version research --format pdf

# For a consulting opportunity
python resume_manager.py --version consulting --all-formats
```

### Color Scheme Testing Workflow
```bash
# Test corporate blue for traditional company
python resume_manager.py --generate-data --color-scheme corporate_blue
python resume_manager.py --version software --format pdf

# Test modern tech for startup
python resume_manager.py --generate-data --color-scheme modern_tech
python resume_manager.py --version software --format pdf

# Compare results and choose preferred scheme
```

### Complete System Regeneration
```bash
# Clean slate regeneration
python resume_manager.py --clean
python resume_manager.py --generate-data --color-scheme default_professional
python resume_manager.py --everything
```

## Customization

### Adding New Resume Versions

1. **Create data function** in `resume_data_generator.py`:
```python
def create_new_version_data():
    """Create data for new version"""
    data = {
        'personal_info': {
            'name': 'DHEERAJ CHAND',
            'title': 'New Professional Title',
            # ... rest of personal info
        },
        'summary': 'New version summary...',
        # ... rest of content
    }
    return data
```

2. **Add to main function**:
```python
# In main() function
new_version_data = create_new_version_data()
new_version_config = create_config_file("new_version", color_scheme)
save_resume_data("dheeraj_chand_new_version", new_version_data, new_version_config)
```

3. **Update resume manager** to include new version in `self.versions` dictionary.

### Custom Color Schemes

Create custom color scheme files in the `color_schemes/` directory:

```json
{
  "scheme_name": "custom_theme",
  "colors": {
    "NAME_COLOR": "#your_primary_color",
    "TITLE_COLOR": "#your_secondary_color",
    "SECTION_HEADER_COLOR": "#your_secondary_color",
    "JOB_TITLE_COLOR": "#your_accent_color",
    "ACCENT_COLOR": "#your_accent_color",
    "COMPETENCY_HEADER_COLOR": "#your_primary_color",
    "SUBTITLE_COLOR": "#your_primary_color",
    "LINK_COLOR": "#your_secondary_color"
  },
  "typography": {
    "NAME_SIZE": 26,
    "BODY_SIZE": 10
  }
}
```

### Content Strategy by Version

#### Research Focused Version (`research`)
- **Target**: Academic institutions, research organizations, NGOs
- **Emphasis**: Applied research leadership, community impact, evidence-based decision making
- **Key Skills**: Research methodology, statistical analysis, stakeholder communication
- **Experience Focus**: Community partnerships, policy analysis, expert testimony

#### Technical Detailed Version (`technical`)
- **Target**: Data engineering teams, technical architecture roles
- **Emphasis**: Big data processing, geospatial platforms, system architecture
- **Key Skills**: Apache Spark/Sedona, GIS technology stack, performance optimization
- **Experience Focus**: ETL pipelines, distributed systems, technical leadership

#### Software Engineer Version (`software`) - DEFAULT
- **Target**: Software engineering roles, platform development positions
- **Emphasis**: Full-stack development, scalable system architecture, platform engineering
- **Key Skills**: Python/Django, JavaScript/React, distributed systems, DevOps
- **Experience Focus**: Platform development (BALLISTA, DAMON), team leadership, production systems

#### Consulting Minimal Version (`consulting`)
- **Target**: Consulting firms, strategic advisory roles, client-facing positions
- **Emphasis**: Strategic planning, technology consulting, business transformation
- **Key Skills**: Project management, stakeholder communication, technology selection
- **Experience Focus**: Client relationships, strategic initiatives, technology modernization

#### Comprehensive Full Version (`comprehensive`)
- **Target**: Executive roles, complete career review, senior positions
- **Emphasis**: Complete career progression, balanced technical and leadership experience
- **Key Skills**: Full technology stack, research and engineering, strategic planning
- **Experience Focus**: 20+ year career arc, all major platforms and achievements

#### Product Marketing Version (`marketing`)
- **Target**: Product marketing roles, go-to-market positions, marketing strategy
- **Emphasis**: Market research, customer insights, product positioning, competitive analysis
- **Key Skills**: Market intelligence, customer segmentation, messaging development
- **Experience Focus**: Product launches, market research, customer development, competitive positioning

## Technical Highlights

### Key Technologies Showcased
- **Apache Spark/Sedona**: Big data geospatial processing at billion-record scale
- **GIS Technology Stack**: ESRI ArcGIS, OSGeo (QGIS, GRASS), SAFE FME integration
- **Programming**: Python (Django/GeoDjango, PySpark), Scala, JavaScript, SQL
- **Platforms**: AWS, Snowflake, PostgreSQL/PostGIS, MongoDB
- **Specific Projects**: BALLISTA, DAMON, SimCrisis, RACSO platforms

### Performance Metrics
- Processing billions of geospatial records with sub-hour latency
- 57% ETL performance improvements through Spark/Sedona optimization
- 88% improvement in analytical targeting efficacy
- Multi-terabyte fraud detection system implementations
- Platform serving thousands of concurrent analysts

### Professional Experience Highlights
- **20+ years** comprehensive data and software engineering experience
- **Partner at Siege Analytics** (2005-Present) - Data, technology and strategy consulting
- **Team Leadership** - Managed engineering teams up to 11 professionals
- **Platform Architecture** - Designed multi-tenant SaaS platforms used by thousands
- **Research Integration** - Applied research projects focused on economic mobility and community development

## Dependencies

### Required Python Packages
```bash
pip install reportlab>=3.5.0
pip install python-docx>=0.8.11  # For DOCX generation
```

### System Requirements
- Python 3.7+
- ReportLab library (PDF generation)
- python-docx (DOCX generation)
- Standard library modules: json, pathlib, argparse, subprocess, datetime

### Optional Dependencies
- For RTF generation: Built-in (no additional packages required)
- For custom fonts: Additional ReportLab font setup

## Output Examples

Each resume version generates three high-quality formats:

### PDF Output
- **Quality**: High-resolution, print-ready format
- **Compatibility**: Universal compatibility, ATS-friendly
- **Usage**: Job applications, professional printing, digital distribution

### DOCX Output
- **Quality**: Microsoft Word compatible, fully editable
- **Compatibility**: ATS-optimized, recruiter-friendly
- **Usage**: Easy customization, collaborative review, ATS systems

### RTF Output
- **Quality**: Rich Text Format, cross-platform compatible
- **Compatibility**: Opens in Word, Pages, Google Docs
- **Usage**: Maximum compatibility, legacy systems

## Troubleshooting

### Common Issues and Solutions

#### Setup Issues
```bash
# Missing dependencies
pip install reportlab python-docx

# Permission errors
chmod +x generate_all_dheeraj_resumes.py
python resume_manager.py --check

# Python version compatibility
python --version  # Ensure 3.7+
```

#### Generation Issues
```bash
# Missing input data
python resume_manager.py --generate-data
python resume_manager.py --list

# Configuration problems
python resume_manager.py --check
python resume_manager.py --clean
python resume_manager.py --generate-data --color-scheme default_professional

# Format-specific issues
python resume_manager.py --version software --format pdf  # Try PDF first
python resume_manager.py --version software --format docx  # Then DOCX
```

#### Content Issues
- **Content exceeds 2 pages**: Edit JSON data to reduce content length
- **Color not appearing**: Verify hex color format in config.json (#RRGGBB)
- **Font issues**: ReportLab uses built-in fonts; custom fonts require additional setup
- **Spacing problems**: Adjust layout parameters in config.json

### Debug Mode
Enable detailed logging by examining script output:
```bash
python resume_manager.py --check  # System diagnostic
python reportlab_resume.py --format pdf --basename dheeraj_chand_software_engineer  # Direct generation
```

### Performance Optimization
- **Faster generation**: Use PDF format only for quick iterations
- **Batch optimization**: Use `generate_all_dheeraj_resumes.py` for complete regeneration
- **Storage management**: Use `python resume_manager.py --clean` to manage disk space

## Development and Extension

### Adding Custom Features

#### New Color Schemes
1. Create JSON file in `color_schemes/` directory
2. Add scheme to `PredefinedSchemes` class in `resume_data_generator.py`
3. Update command-line options and documentation

#### New Resume Sections
1. Add section data to JSON structure in `resume_data_generator.py`
2. Implement rendering method in `reportlab_resume.py`
3. Update template and styling as needed

#### Custom Formatting
1. Modify `_create_styles()` method in `reportlab_resume.py`
2. Adjust layout parameters in configuration files
3. Test across all resume versions

### Version Control Best Practices
- Keep JSON data files in version control
- Track configuration changes for color schemes
- Document custom modifications for maintenance

### Testing New Versions
```bash
# Test individual components
python resume_manager.py --version software --format pdf
python resume_manager.py --check

# Test batch processing
python generate_all_dheeraj_resumes.py

# Test color schemes
python resume_manager.py --generate-data --color-scheme modern_tech
python resume_manager.py --version software --format pdf
```

## Professional Usage Guidelines

### Resume Version Selection
- **Software Engineering Roles**: Use `software` version (comprehensive technical depth)
- **Data Engineering Positions**: Use `technical` version (big data and geospatial focus)
- **Research Opportunities**: Use `research` version (applied research and community impact)
- **Consulting Engagements**: Use `consulting` version (strategic advisory focus)
- **Executive Positions**: Use `comprehensive` version (complete career overview)
- **Product/Marketing Roles**: Use `marketing` version (go-to-market expertise)

### Color Scheme Selection
- **Traditional Industries** (Finance, Legal, Healthcare): `corporate_blue`
- **Creative and Consulting Roles**: `default_professional`
- **Tech Startups and Innovation**: `modern_tech`
- **Design and Marketing Positions**: `elegant_purple`

### Format Selection by Use Case
- **Online Applications**: PDF (universal compatibility)
- **ATS Systems**: DOCX (optimized parsing)
- **Print Submissions**: PDF (high quality)
- **Collaborative Review**: DOCX (easy editing)
- **Maximum Compatibility**: RTF (cross-platform)

---

*This resume generation system showcases 20+ years of expertise in data engineering, geospatial platforms, and software development with emphasis on Apache Spark/Sedona, ESRI/OSGeo technologies, and production-scale platform development. The system generates professional resumes optimized for different career focuses while maintaining consistent quality and branding.*
