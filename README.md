# Professional Resume Generator

A Python-based resume generation system that creates professional, multi-format resumes using ReportLab and structured JSON data. Generates PDF, DOCX, and RTF formats with consistent branding and customizable styling.

## Features

- **Multiple Resume Versions**: Generate different versions targeting specific roles (Research, Technical, Software Engineer, Consulting, Comprehensive)
- **Multi-Format Output**: PDF, DOCX, and RTF formats for maximum compatibility
- **Consistent Branding**: Green, gold, and blue color scheme across all versions
- **Structured Data**: JSON-based content management for easy customization
- **Professional Layout**: 2-page optimized design with precise typography
- **Batch Generation**: Create all resume versions with a single command

## Quick Start

### 1. Generate Resume Data
```bash
python clean_resume_generator.py
```

This creates:
- Directory structure (`inputs/` and `outputs/`)
- JSON data files for each resume version
- Configuration files with styling
- Batch generation script

### 2. Generate All Resumes
```bash
./generate_all_resumes.sh
```

Or generate individual versions:
```bash
python reportlab_resume.py --format pdf --basename dheeraj_software_engineer
python reportlab_resume.py --format all --basename dheeraj_research_focused
```

## Resume Versions

| Version | Focus | Target Audience |
|---------|--------|----------------|
| `dheeraj_research_focused` | Applied research leadership, community impact | Research organizations, NGOs, policy roles |
| `dheeraj_technical_detailed` | Data engineering, geospatial platforms | Technical teams, engineering managers |
| `dheeraj_software_engineer` | Platform development, Spark/Sedona expertise | Software engineering roles, tech companies |
| `dheeraj_consulting_minimal` | Strategic advisory, technology consulting | Consulting firms, strategy roles |
| `dheeraj_comprehensive_full` | Complete work history and technical depth | Executive roles, comprehensive review |

## Project Structure

```
resume-generator/
├── clean_resume_generator.py      # Data generation script
├── reportlab_resume.py            # Main resume generation engine
├── generate_all_resumes.sh        # Batch generation script
├── inputs/                        # JSON data and configuration
│   ├── dheeraj_research_focused/
│   │   ├── resume_data.json       # Content data
│   │   └── config.json           # Styling configuration
│   ├── dheeraj_technical_detailed/
│   ├── dheeraj_software_engineer/
│   ├── dheeraj_consulting_minimal/
│   └── dheeraj_comprehensive_full/
└── outputs/                       # Generated resumes
    ├── dheeraj_research_focused/
    │   ├── pdf/
    │   ├── docx/
    │   └── rtf/
    └── [other versions]/
```

## Data Structure & Configuration

### Resume Data JSON (`resume_data.json`)

Each resume version uses a structured JSON file containing all content. Here's the complete schema:

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

  "summary": "Professional summary paragraph highlighting key expertise and experience...",

  "competencies": {
    "Programming & Development": [
      "Python: Django/GeoDjango, Flask, Pandas, PySpark, NumPy, SciKit-Learn",
      "JVM: Scala (Spark/Sedona), Java (GeoTools, enterprise applications), Groovy",
      "Web Technologies: JavaScript, React, d3.js, OpenLayers, jQuery, HTML/CSS"
    ],
    "Big Data & Geospatial Platforms": [
      "Apache Spark: PySpark, Spark SQL, Sedona (geospatial), distributed processing",
      "Geospatial Stack: PostGIS, ESRI ArcGIS, Quantum GIS, GRASS, OSGeo, SAFE FME"
    ],
    "Software Architecture & DevOps": [
      "Distributed Systems: Multi-tenant SaaS, microservices, API design, scalability",
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
        "Architected and engineered BALLISTA: GeoDjango redistricting platform serving thousands of analysts",
        "Developed DAMON: Flask/PostGIS microservice using incomplete data for boundary estimation",
        "Built scalable ETL pipelines using PySpark and Sedona processing billions of geospatial records"
      ]
    }
  ],

  "achievements": {
    "Geospatial Platform Development": [
      "Architected BALLISTA redistricting platform used by thousands of analysts nationwide",
      "Built DAMON boundary estimation system achieving accurate geospatial results"
    ],
    "Big Data & Performance Engineering": [
      "Implemented Spark/Sedona ETL optimizations achieving 57% performance improvement",
      "Built systems processing billions of spatial records with sub-hour latency"
    ]
  },

  "_metadata": {
    "version": "software_engineer",
    "created": "2025-01-20T10:30:00Z",
    "description": "Software engineer focused version emphasizing technical skills"
  }
}
```

### Configuration JSON (`config.json`)

The styling and layout configuration supports the complete green, gold, and blue branding:

```json
{
  "PRIMARY_GREEN": "#228B22",
  "SECONDARY_GOLD": "#B8860B",
  "ACCENT_BLUE": "#1F4E79",
  "LIGHT_GOLD": "#DAA520",
  "LIGHT_BLUE": "#4682B4",
  "DARK_GRAY": "#333333",
  "MEDIUM_GRAY": "#666666",
  "LIGHT_GRAY": "#999999",

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
    "version": "software_engineer",
    "created": "2025-01-20T10:30:00Z",
    "description": "Configuration for software_engineer resume version with green, gold, and blue branding"
  }
}
```

### Configuration Reference

#### Color Properties
| Property | Default | Usage | Example Colors |
|----------|---------|--------|----------------|
| `PRIMARY_GREEN` | `#228B22` | Name, primary accents, competency headers | Forest Green |
| `SECONDARY_GOLD` | `#B8860B` | Section headers, contact links | Dark Goldenrod |
| `ACCENT_BLUE` | `#1F4E79` | Job titles, highlights | Professional Blue |
| `LIGHT_GOLD` | `#DAA520` | Lighter accents, secondary elements | Goldenrod |
| `LIGHT_BLUE` | `#4682B4` | Secondary highlights, subtle accents | Steel Blue |
| `DARK_GRAY` | `#333333` | Main body text | Charcoal |
| `MEDIUM_GRAY` | `#666666` | Secondary text, company info | Medium Gray |
| `LIGHT_GRAY` | `#999999` | Tertiary text, subtle elements | Light Gray |

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
| `PARAGRAPH_SPACING` | `0.06` | Space between paragraphs (inches) |
| `LINE_SPACING` | `1.15` | Line height multiplier |
| `JOB_SPACING` | `6` | Space between job entries (points) |
| `CATEGORY_SPACING` | `4` | Space between competency categories (points) |
| `MAX_PAGES` | `2` | Maximum number of pages |
| `BULLET_CHAR` | `▸` | Character used for bullet points |

### Creating Custom Themes

#### Corporate Blue Theme Example
```json
{
  "PRIMARY_GREEN": "#2E5090",
  "SECONDARY_GOLD": "#C41E3A",
  "ACCENT_BLUE": "#1F4E79",
  "NAME_SIZE": 26,
  "TITLE_SIZE": 16,
  "PAGE_MARGIN": 0.5
}
```

#### Minimalist Theme Example
```json
{
  "PRIMARY_GREEN": "#2C3E50",
  "SECONDARY_GOLD": "#E67E22",
  "ACCENT_BLUE": "#3498DB",
  "BODY_SIZE": 10,
  "SECTION_SPACING": 0.15,
  "BULLET_CHAR": "•"
}
```

#### High Contrast Theme Example
```json
{
  "PRIMARY_GREEN": "#000000",
  "SECONDARY_GOLD": "#FF6B35",
  "ACCENT_BLUE": "#004E89",
  "DARK_GRAY": "#000000",
  "MEDIUM_GRAY": "#333333"
}
```

## Command Line Usage

### Basic Usage
```bash
python reportlab_resume.py --format [pdf|docx|rtf|all] --basename [version_name]
```

### Options
- `--format`: Output format (pdf, docx, rtf, or all)
- `--basename`: Resume version name (corresponds to input directory)
- `--input-dir`: Custom input directory path
- `--output-dir`: Custom output directory path
- `--config`: Custom configuration file path (new feature)

### Examples
```bash
# Generate PDF for software engineer version
python reportlab_resume.py --format pdf --basename dheeraj_software_engineer

# Generate all formats for research version
python reportlab_resume.py --format all --basename dheeraj_research_focused

# Use custom directories
python reportlab_resume.py --format pdf --basename custom_version --input-dir ./custom/inputs --output-dir ./custom/outputs

# Use custom configuration
python reportlab_resume.py --format pdf --basename dheeraj_software_engineer --config ./custom_config.json
```

## Customization

### Content Customization

Edit the `resume_data.json` files in each version's input directory. The JSON structure includes:

#### Personal Information
```json
"personal_info": {
  "name": "YOUR NAME",
  "title": "Your Professional Title",
  "phone": "Your Phone",
  "email": "your.email@domain.com",
  "website": "https://yourwebsite.com",
  "linkedin": "https://www.linkedin.com/in/yourprofile/"
}
```

#### Professional Summary
```json
"summary": "Your professional summary highlighting key expertise, years of experience, and major accomplishments..."
```

#### Core Competencies (Organized by Category)
```json
"competencies": {
  "Technical Skills": [
    "Skill 1: Specific technologies, frameworks, or tools",
    "Skill 2: Programming languages with specific libraries",
    "Skill 3: Platforms and systems with experience details"
  ],
  "Leadership & Management": [
    "Team leadership and mentoring experience",
    "Project management and delivery track record"
  ]
}
```

#### Experience Entries
```json
"experience": [
  {
    "title": "JOB TITLE IN CAPS",
    "company": "Company Name, City, State",
    "dates": "Start Date – End Date",
    "subtitle": "Brief role focus or department description",
    "responsibilities": [
      "Achievement-focused bullet point with metrics where possible",
      "Technical accomplishment highlighting specific technologies used",
      "Leadership or impact statement with quantifiable results"
    ]
  }
]
```

#### Key Achievements (Grouped by Impact Area)
```json
"achievements": {
  "Technical Innovation": [
    "Specific platform or system you built with usage metrics",
    "Performance improvements with percentage gains"
  ],
  "Leadership & Scale": [
    "Team size and management accomplishments",
    "Process improvements and efficiency gains"
  ]
}
```

### Styling Customization

Create custom theme files or edit existing `config.json` files:

#### Quick Color Updates
```json
{
  "PRIMARY_GREEN": "#your_primary_color",
  "SECONDARY_GOLD": "#your_secondary_color",
  "ACCENT_BLUE": "#your_accent_color"
}
```

#### Font Size Adjustments
```json
{
  "NAME_SIZE": 26,        // Larger name
  "BODY_SIZE": 10,        // Larger body text
  "SECTION_HEADER_SIZE": 13  // Larger section headers
}
```

#### Layout Modifications
```json
{
  "PAGE_MARGIN": 0.5,      // Smaller margins = more content
  "SECTION_SPACING": 0.15, // More space between sections
  "LINE_SPACING": 1.2,     // More line height
  "BULLET_CHAR": "•"       // Different bullet style
}
```

### Usage with Custom Configurations

#### Using a Custom Theme File
```bash
# Create a custom theme
cat > themes/corporate_blue.json << EOF
{
  "PRIMARY_GREEN": "#2E5090",
  "SECONDARY_GOLD": "#C41E3A",
  "ACCENT_BLUE": "#1F4E79",
  "NAME_SIZE": 26,
  "PAGE_MARGIN": 0.5
}
EOF

# Generate resume with custom theme
python reportlab_resume.py --format pdf --basename dheeraj_software_engineer --config themes/corporate_blue.json
```

#### Testing Different Styles
```bash
# Generate same content with different themes
python reportlab_resume.py --format pdf --basename dheeraj_software_engineer --config themes/minimalist.json
python reportlab_resume.py --format pdf --basename dheeraj_software_engineer --config themes/high_contrast.json
python reportlab_resume.py --format pdf --basename dheeraj_software_engineer --config themes/corporate.json
```

### Content Strategy by Version

#### Research Focused Version
- Emphasize applied research leadership and community impact
- Highlight collaboration with NGOs, elected officials, community organizations
- Focus on evidence-based decision making and social outcomes
- Include specific research methodologies and statistical analysis

#### Technical Detailed Version
- Showcase data engineering expertise and architectural decisions
- Emphasize big data processing capabilities (Spark/Sedona, billions of records)
- Highlight GIS technology integration (ESRI, OSGeo, SAFE FME)
- Include specific performance metrics and optimization achievements

#### Software Engineer Version
- Focus on platform development and scalable system architecture
- Highlight specific applications built (BALLISTA, DAMON, SimCrisis)
- Emphasize full-stack development capabilities
- Include team leadership and mentoring experience

#### Consulting Minimal Version
- Strategic advisory focus with diverse client portfolio
- Emphasize business impact and transformation outcomes
- Highlight technology selection and architecture consulting
- Focus on long-term client relationships and strategic planning

#### Comprehensive Full Version
- Complete career progression with all technical details
- Balanced view of research, engineering, and leadership capabilities
- Comprehensive skill inventory across all technology stacks
- Full context for career evolution and expertise development

## Technical Highlights

### Key Technologies Showcased
- **Apache Spark/Sedona**: Big data geospatial processing
- **GIS Technology Stack**: ESRI ArcGIS, OSGeo (QGIS, GRASS), SAFE FME
- **Programming**: Python (Django/GeoDjango, PySpark), Scala, JavaScript
- **Platforms**: AWS, Snowflake, PostgreSQL/PostGIS
- **Specific Projects**: BALLISTA, DAMON, SimCrisis, RACSO platforms

### Performance Metrics
- Processing billions of geospatial records
- 57% ETL performance improvements
- 88% improvement in analytical targeting efficacy
- Sub-hour latency requirements at scale

## Dependencies

### Python Packages
```bash
pip install reportlab
pip install python-docx  # For DOCX generation
```

### System Requirements
- Python 3.7+
- ReportLab library
- python-docx (optional, for Word document generation)

## Output Examples

Each resume version generates:
- **PDF**: High-quality, print-ready format
- **DOCX**: Microsoft Word compatible, ATS-friendly
- **RTF**: Rich Text Format, opens in Pages/Word

## Development Notes

### Adding New Resume Versions
1. Create new data function in `clean_resume_generator.py`
2. Add version to `resume_versions` list
3. Update `main()` function to generate the new version
4. Re-run the data generator

### Color Scheme Updates
All versions use the same color palette defined in `create_config_file()`. Update this function to change the global color scheme.

### Layout Modifications
Adjust spacing, fonts, and layout parameters in the `ResumeConfig` class or individual `config.json` files.

## Troubleshooting

### Common Issues
1. **Missing Dependencies**: Install reportlab and python-docx
2. **Permission Errors**: Ensure write permissions for output directories
3. **Font Issues**: ReportLab uses built-in fonts; custom fonts require additional setup
4. **Large Content**: Content may exceed 2-page limit; edit content or adjust spacing

### Debug Mode
Add debug flags to see detailed directory creation and file processing:
```bash
python reportlab_resume.py --format pdf --basename test_version --debug
```

## Contributing

To extend functionality:
1. Fork the repository
2. Create feature branch
3. Add new resume versions or formatting options
4. Test with sample data
5. Submit pull request

## License

This project is designed for personal professional use. Customize as needed for your resume generation requirements.

---

*Generated resumes showcase 20+ years of expertise in data engineering, geospatial platforms, and software development with emphasis on Apache Spark/Sedona, ESRI/OSGeo technologies, and production-scale platform development.*
