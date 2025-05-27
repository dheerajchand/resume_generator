# Professional Resume Generator System

A comprehensive Python-based resume generation system that creates professional, multi-format resumes from structured JSON data. Generates PDF, DOCX, and RTF formats with configurable color schemes and precise typography for maximum impact and ATS compatibility.

**✨ Now supports any user - completely generic and customizable!**

## Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install reportlab python-docx
```

### 2. Run Interactive Setup
```bash
python setup_user.py
```
This walks you through personalizing the system with your information.

### 3. Generate Your Resume Data
```bash
python resume_manager.py --generate-data
```

### 4. Create Your First Resume
```bash
python resume_manager.py --version software --format pdf
```

### 5. Check What Was Generated
```bash
python resume_manager.py --list
```

**🎉 That's it!** Your personalized resume system is ready. Jump to [Advanced Usage](#advanced-usage) or keep reading for full documentation.

## Features

- **Multiple Resume Versions**: Six targeted versions (Research, Technical, Software Engineer, Consulting, Comprehensive, Product Marketing)
- **Multi-Format Output**: PDF, DOCX, and RTF formats for maximum compatibility
- **Dynamic Color Schemes**: Professional themes with custom color scheme generation tools
- **Generic User System**: Works for anyone - completely customizable personal information
- **Privacy Protection**: Personal data automatically excluded from git commits
- **Professional Layout**: 2-page optimized design with precise typography and spacing
- **Flexible Generation Options**: Individual, batch, or selective generation capabilities
- **Color Scheme Comparison**: Generate same resume with different color schemes for A/B testing
- **Nuclear Option**: Generate every possible combination (180+ files) for comprehensive testing
- **Easy Setup**: Interactive configuration for new users

## System Overview

### What This Creates For You

**Your personalized file naming:**
- `{your_name}_{version}_{color_scheme}.{extension}`
- Examples: `john_doe_software_corporate_blue.pdf`, `jane_smith_technical_modern_tech.docx`

**Your organized directory structure:**
```
resume-generator/
├── user_config.json           # Your personal settings (private)
├── inputs/                    # Your resume content (private)
│   ├── your_name_research_focused/
│   ├── your_name_software_engineer/
│   └── ... (all 6 versions)
└── outputs/                   # Your generated resumes (private)
    ├── research/corporate_blue/pdf/
    ├── software/modern_tech/pdf/
    └── ... (organized by version/color/format)
```

**Privacy protection:** Your personal information never gets committed to git thanks to `.gitignore`.

## System Architecture

| Script | Purpose | Primary Use Case |
|--------|---------|------------------|
| `setup_user.py` | **Interactive setup** - Configure system for your personal use | First-time setup, updating personal info |
| `resume_manager.py` | **Main controller** - Individual and batch resume management | Daily use, specific version generation |
| `resume_data_generator.py` | Creates structured JSON data files with your personal content | Initial setup, content updates |
| `reportlab_resume.py` | Core resume generation engine using ReportLab | Direct generation control |
| `color_scheme_generator_tool.py` | Custom color scheme creation and preview | Design customization |
| `user_config.py` | Configuration management system | Internal use (loaded by other scripts) |

## Resume Versions

The system generates six distinct resume versions, each optimized for different career focuses:

| Version Key | Professional Title (Customizable) | Target Roles | Key Emphasis |
|-------------|-----------------------------------|--------------|--------------|
| `research` | Director of Research and Analysis | Academic, NGO, Policy | Applied research leadership, community impact |
| `technical` | Senior Data Engineer & Technical Architect | Data engineering, Architecture | Big data, geospatial platforms, system design |
| `software` | Senior Software Engineer | Software engineering, Development | Full-stack development, platform engineering |
| `consulting` | Data Analytics & Technology Consultant | Consulting, Strategy | Strategic advisory, technology consulting |
| `comprehensive` | Research, Data & Engineering Professional | Executive, Senior roles | Complete career history and technical depth |
| `marketing` | Senior Product Marketing Manager | Product marketing, Go-to-market | Market research, product positioning |

## Advanced Usage

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

# Generate all versions in all formats with current color scheme (18 total files)
python resume_manager.py --everything

# ☢️ NUCLEAR OPTION: Generate EVERY version in EVERY format with EVERY color scheme (180+ files)
python resume_manager.py --nuclear
```

#### Understanding `--everything` vs `--nuclear`

**`--everything` (18 files)**
- Generates all versions × all formats × **current color scheme only**
- Quick generation (few minutes)
- Perfect for job applications with your preferred color scheme

**`--nuclear` (180+ files)**
- Generates all versions × all formats × **ALL color schemes**
- Comprehensive generation (takes longer)
- Perfect for A/B testing different color schemes across all resume versions
- Includes confirmation prompt due to large number of files

```bash
# Current color scheme only (recommended for most use cases)
python resume_manager.py --everything

# Every possible combination (use when experimenting with color schemes)
python resume_manager.py --nuclear
```

#### Color Scheme Comparison and Testing
```bash
# Generate same version with multiple color schemes for comparison
python resume_manager.py --version software --color-comparison default_professional corporate_blue modern_tech
```

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

#### Cartographic Professional (Earth Tones)
```bash
python resume_manager.py --generate-data --color-scheme cartographic_professional
```
- **Best for**: GIS, geospatial, environmental, and earth sciences roles
- **Colors**: Deep Forest Green (#2D5016), Warm Sienna Brown (#A0522D), Deep Ocean Blue (#1E3A8A)

### Custom Color Scheme Creation

Generate custom color schemes using the color scheme generator tool:

```bash
# Create industry-specific schemes
python color_scheme_generator_tool.py --industry finance --name corporate_finance --preview

# Create brand-based schemes (uses your brand colors)
python color_scheme_generator_tool.py --brand '#1F4E79' '#FF6B35' --name my_company_colors --preview

# Create color theory-based schemes
python color_scheme_generator_tool.py --complementary '#228B22' --name nature_complement --preview

# Create geospatial/earth science themes
python color_scheme_generator_tool.py --brand '#2D5016' '#A0522D' '#1E3A8A' --name cartographic_professional --preview
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
| `--everything` | None | Generate all versions in all formats with current color scheme |
| `--nuclear` | None | ☢️ Generate EVERY version in EVERY format with EVERY color scheme |
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

## Customization and Extension

### Updating Your Personal Information

```bash
# Re-run setup to update your information
python setup_user.py

# Or manually edit user_config.json
```

### Adding Custom Resume Content

Edit the JSON files in your `inputs/` directories to customize:
- Professional summaries
- Skills and competencies
- Work experience
- Achievements and projects

### Creating Industry-Specific Versions

The system is designed to be easily extended. You can:
1. Add new resume versions by modifying `resume_data_generator.py`
2. Create industry-specific color schemes
3. Customize professional titles for your field

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
- **GIS and Geospatial**: `cartographic_professional`
- **Custom Branding**: Generate custom schemes with your brand colors

### Format Selection by Use Case
- **Online Applications**: PDF (universal compatibility, maintains formatting)
- **ATS Systems**: DOCX (optimized for parsing, machine-readable)
- **Print Submissions**: PDF (high-quality printing, consistent rendering)
- **Collaborative Review**: DOCX (easy editing and comments)
- **Maximum Compatibility**: RTF (cross-platform, legacy system support)

## Advanced Workflows

### Job Application Workflow
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

### Color Scheme A/B Testing
```bash
# Test corporate blue for traditional company application
python resume_manager.py --generate-data --color-scheme corporate_blue
python resume_manager.py --version software --format pdf

# Test modern tech for startup application
python resume_manager.py --generate-data --color-scheme modern_tech
python resume_manager.py --version software --format pdf

# Compare outputs and select preferred version
```

### Complete System Refresh
```bash
# Clean slate regeneration
python resume_manager.py --clean
python resume_manager.py --generate-data --color-scheme default_professional
python resume_manager.py --everything
```

## Data Structure

### User Configuration Structure (`user_config.json`)
```json
{
  "personal_info": {
    "name": "YOUR FULL NAME",
    "phone": "(XXX) XXX-XXXX",
    "email": "your.email@example.com",
    "website": "https://www.yourwebsite.com",
    "linkedin": "https://www.linkedin.com/in/yourusername/"
  },
  "file_naming": {
    "base_name": "your_name"
  },
  "directory_naming": {
    "prefix": "your_name"
  },
  "titles": {
    "research": "Director of Research and Analysis",
    "technical": "Senior Data Engineer & Technical Architect",
    "software": "Senior Software Engineer",
    "consulting": "Data Analytics & Technology Consultant",
    "comprehensive": "Research, Data & Engineering Professional",
    "marketing": "Senior Product Marketing Manager"
  },
  "resume_content": {
    "industry_focus": "technology",
    "years_experience": "10+",
    "specializations": [
      "Data Engineering",
      "Software Development",
      "System Architecture"
    ]
  }
}
```

### Resume Data Structure (`resume_data.json`)
```json
{
  "personal_info": {
    "name": "YOUR FULL NAME",
    "title": "Professional Title",
    "phone": "(XXX) XXX-XXXX",
    "email": "your.email@example.com",
    "website": "https://www.yourwebsite.com",
    "linkedin": "https://www.linkedin.com/in/yourusername/"
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

## Project Structure

```
resume-generator/
├── setup_user.py                 # Interactive user setup (run this first!)
├── resume_manager.py              # Main controller for resume generation
├── resume_data_generator.py       # Professional data generation with color schemes
├── reportlab_resume.py            # Core resume generation engine
├── color_scheme_generator_tool.py # Custom color scheme creation tool
├── user_config.py                 # Configuration management system
├── .gitignore                     # Protects your personal data
├── user_config_template.json      # Template for manual configuration
├── color_schemes/                 # Color scheme configuration files
│   ├── default_professional.json
│   ├── corporate_blue.json
│   ├── modern_tech.json
│   ├── cartographic_professional.json
│   ├── satellite_imagery.json
│   ├── terrain_mapping.json
│   ├── topographic_classic.json
│   └── [your_custom_schemes].json
├── user_config.json               # Your personal settings (private, auto-created)
├── inputs/                        # Your resume data (private, auto-created)
│   ├── your_name_research_focused/
│   │   ├── resume_data.json       # Research-focused content
│   │   └── config.json           # Color and styling configuration
│   ├── your_name_technical_detailed/
│   │   ├── resume_data.json       # Technical engineering content
│   │   └── config.json           # Configuration
│   ├── your_name_software_engineer/  # DEFAULT VERSION
│   │   ├── resume_data.json       # Software engineering content
│   │   └── config.json           # Configuration
│   ├── your_name_consulting_minimal/
│   │   ├── resume_data.json       # Consulting-focused content
│   │   └── config.json           # Configuration
│   ├── your_name_comprehensive_full/
│   │   ├── resume_data.json       # Complete work history
│   │   └── config.json           # Configuration
│   └── your_name_product_marketing/
│       ├── resume_data.json       # Product marketing content
│       └── config.json           # Configuration
└── outputs/                       # Your generated resumes (private, auto-created)
    ├── research/
    │   ├── default_professional/
    │   │   ├── pdf/your_name_research_default_professional.pdf
    │   │   ├── docx/your_name_research_default_professional.docx
    │   │   └── rtf/your_name_research_default_professional.rtf
    │   ├── cartographic_professional/
    │   │   └── pdf/your_name_research_cartographic_professional.pdf
    │   └── corporate_blue/
    ├── technical/
    │   ├── cartographic_professional/
    │   │   └── pdf/your_name_technical_cartographic_professional.pdf
    │   └── [other_color_schemes]/
    ├── software/
    ├── consulting/
    ├── comprehensive/
    └── marketing/
```

## File Naming Convention

All generated resume files follow the pattern:
**`{your_name}_{resume_type}_{color_scheme}.{extension}`**

**Examples**:
- `john_doe_software_cartographic_professional.pdf`
- `jane_smith_technical_corporate_blue.docx`
- `alex_jones_research_default_professional.rtf`
- `sam_wilson_consulting_modern_tech.pdf`

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

#### Configuration Issues
```bash
# User configuration not found
python setup_user.py

# Update existing configuration
python setup_user.py  # (will ask to overwrite)

# Manual configuration check
python -c "from user_config import UserConfig; print(UserConfig())"
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
- **Content exceeds 2 pages**: Edit JSON data files in `inputs/` directories to reduce content length
- **Colors not displaying**: Verify hex color format (#RRGGBB) in config files
- **Font rendering issues**: ReportLab uses built-in fonts; custom fonts require additional setup
- **Spacing problems**: Adjust layout parameters in config.json files
- **Personal info not showing**: Run `python setup_user.py` to verify configuration

### Performance Optimization
- **Quick iterations**: Use PDF format only during development
- **Batch operations**: Use `--everything` for complete regeneration with current color scheme
- **Storage management**: Use `--clean` periodically to manage disk space
- **Avoid nuclear option**: Only use `--nuclear` when you really need to test all color combinations

### Privacy and Security

Your personal information is automatically protected:
- `user_config.json` - Contains your personal details (private)
- `inputs/` directory - Contains your resume content (private)
- `outputs/` directory - Contains your generated resumes (private)

These are all excluded from git commits via `.gitignore`. You can safely share the repository without exposing personal information.

## Contributing and Extending

### For Developers

The system is designed to be easily extended:

1. **Adding new resume versions**: Add functions to `resume_data_generator.py`
2. **Creating new color schemes**: Use `color_scheme_generator_tool.py`
3. **Modifying output formats**: Extend `reportlab_resume.py`
4. **Adding new features**: The modular design makes it easy to add functionality

### For Users

The most common customizations:
1. **Personal content**: Edit JSON files in `inputs/` directories
2. **Professional titles**: Update `user_config.json` or re-run `setup_user.py`
3. **Color preferences**: Create custom color schemes or modify existing ones
4. **Industry focus**: Customize competencies and experience sections for your field

## Example Workflows

### New Job Search Campaign
```bash
# Update your information if needed
python setup_user.py

# Generate fresh data
python resume_manager.py --generate-data --color-scheme corporate_blue

# Create targeted resumes for different types of roles
python resume_manager.py --version software --format pdf      # For engineering roles
python resume_manager.py --version consulting --format pdf    # For advisory roles
python resume_manager.py --version technical --format pdf     # For technical lead roles

# Test different color schemes for the same role
python resume_manager.py --version software --color-comparison corporate_blue modern_tech default_professional
```

### Freelancer/Consultant Portfolio
```bash
# Generate comprehensive suite
python resume_manager.py --everything

# Create client-specific versions
python resume_manager.py --generate-data --color-scheme modern_tech
python resume_manager.py --version consulting --all-formats
```

### Academic/Research Applications
```bash
# Focus on research version with professional styling
python resume_manager.py --generate-data --color-scheme default_professional
python resume_manager.py --version research --all-formats
python resume_manager.py --version comprehensive --format pdf  # For complete history
```

---

*This professional resume generation system is designed to be a comprehensive, reusable tool for anyone seeking to create high-quality, customized resumes. The system emphasizes professional presentation, technical flexibility, and user privacy while maintaining ease of use.*
