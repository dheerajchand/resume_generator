# Professional Resume Generator

What began as a simple need to generate a few resumes has evolved into a comprehensive Django-based resume generation system that creates professional resumes in multiple formats (PDF, DOCX, RTF, Markdown) with customizable color schemes, role-specific content, and both long and short versions for every use case.

## 🚀 Features

- **Multiple Output Formats**: PDF, DOCX, RTF, and Markdown
- **8 Professional Color Schemes**: Default Professional, Corporate Blue, Modern Tech, Modern Clean, Satellite Imagery, Terrain Mapping, Cartographic Professional, and Topographic Classic
- **8 Resume Categories**: Comprehensive, Polling/Research/Redistricting, Marketing, Data Analysis & Visualization, Data Engineering, Product, Software Engineering, and GIS
- **2 Length Variants**: Long (3 pages) and Short (2 pages) for every category
- **Systematic Design System**: Consistent spacing, typography, and color hierarchy
- **Font Theme System**: ATS-friendly typography with distinctive variations per theme
- **High Quality Output**: Optimized for maximum quality within service size limits
- **Django Web Interface**: Full web application with REST API
- **Heroku Ready**: Configured for easy deployment to Heroku
- **Functional Architecture**: Clean, maintainable code with functional programming principles

## 📁 Project Structure

```
resume_generator/
├── resume_generator_django/          # Django project settings
├── resumes/                          # Main Django app
│   ├── core_services.py             # Core resume generation logic
│   ├── models.py                    # Database models
│   ├── views.py                     # API views
│   ├── serializers.py               # DRF serializers
│   ├── management/commands/         # Django management commands
│   └── content/                     # Content templates
├── inputs/                          # Resume data files
│   ├── dheeraj_chand_comprehensive_full/           # Long version
│   ├── dheeraj_chand_comprehensive_full_abbreviated/ # Short version
│   ├── dheeraj_chand_polling_research_redistricting/
│   ├── dheeraj_chand_polling_research_redistricting_abbreviated/
│   ├── dheeraj_chand_marketing/
│   ├── dheeraj_chand_marketing_abbreviated/
│   ├── dheeraj_chand_data_analysis_visualization/
│   ├── dheeraj_chand_data_analysis_visualization_abbreviated/
│   ├── dheeraj_chand_data_engineering/
│   ├── dheeraj_chand_data_engineering_abbreviated/
│   ├── dheeraj_chand_product/
│   ├── dheeraj_chand_product_abbreviated/
│   ├── dheeraj_chand_software_engineering/
│   ├── dheeraj_chand_software_engineering_abbreviated/
│   ├── dheeraj_chand_gis/
│   └── dheeraj_chand_gis_abbreviated/
├── outputs/                         # Generated resumes
├── color_schemes/                   # Color scheme definitions
├── docs/                           # Documentation
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku deployment
├── runtime.txt                     # Python version
└── README.md                       # This file
```

## 🛠️ Installation

### Local Development

1. **Clone the repository**
```bash
   git clone <repository-url>
   cd resume_generator
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
```bash
   python manage.py migrate
   ```

5. **Start development server**
```bash
   python manage.py runserver
   ```

### Heroku Deployment

1. **Install Heroku CLI**
```bash
   # Follow instructions at https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
```bash
   heroku create your-resume-generator
   ```

3. **Set environment variables**
```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. **Deploy**
```bash
   git push heroku main
   heroku run python manage.py migrate
   ```

## 🎯 Usage

### Command Line Interface

#### Generate All Resumes (Nuclear Option)
```bash
python manage.py generate_all_resumes --confirm
```

This generates all combinations:
- 8 resume categories × 2 length variants × 8 color schemes × 4 formats = 512 files

#### Generate Specific Resume
```bash
python manage.py generate_resume --version comprehensive --color-scheme corporate_blue --format pdf
```

### Django Management Commands

#### Available Commands
- `generate_all_resumes`: Generate all resume combinations
- `setup_resume_system`: Initialize the system with sample data

### Web Interface

The Django app provides a REST API for resume generation:

#### API Endpoints
- `GET /api/resumes/` - List all resumes
- `POST /api/resumes/generate/` - Generate new resume
- `GET /api/resumes/{id}/download/` - Download generated resume

#### Example API Usage
```bash
# Generate a resume
curl -X POST http://localhost:8000/api/resumes/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "version": "comprehensive",
    "color_scheme": "corporate_blue",
    "format": "pdf"
  }'
```

## 🎨 Color Schemes

The system includes 8 professional color schemes with systematic color hierarchy:

1. **Default Professional** - Classic green and gold
2. **Corporate Blue** - Professional blue tones
3. **Modern Tech** - Contemporary tech colors
4. **Modern Clean** - Minimalist modern design
5. **Satellite Imagery** - Earth observation inspired
6. **Terrain Mapping** - Topographic map colors
7. **Cartographic Professional** - GIS professional theme
8. **Topographic Classic** - Traditional mapping colors

Each color scheme uses a systematic 4-color hierarchy:
- **Primary**: Section headers, company names, main competency categories
- **Secondary**: Body text, person's name
- **Accent**: Sub-competencies, contact information
- **Muted**: Bullet points, job titles, subtitles

## 📝 Resume Categories

Eight different resume categories are available, each with both long (3-page) and short (2-page) versions:

### 1. [Comprehensive](outputs/comprehensive/) - Complete Professional Profile
Complete professional profile with full work history spanning 15+ years across research, data engineering, and software development. Includes all major accomplishments, technical skills, and leadership experience.

### 2. [Polling/Research/Redistricting](outputs/polling_research_redistricting/) - Survey Methodology & Redistricting
Specialized for political polling, market research, and redistricting analysis roles. Highlights survey methodology expertise, expert testimony experience, and redistricting software development including Ballista Redistricting platform.

### 3. [Marketing](outputs/marketing/) - Market Intelligence & Strategy
Focused on market intelligence, consumer insights, and go-to-market strategy. Emphasizes data-driven marketing decisions, campaign optimization, and revenue generation through marketing analytics.

### 4. [Data Analysis & Visualization](outputs/data_analysis_visualization/) - Statistical Analysis & Data Visualization
Combines statistical analysis, machine learning, and data visualization expertise. Perfect for data scientist, analyst, and visualization specialist roles requiring both analytical and visual communication skills.

### 5. [Data Engineering](outputs/data_engineering/) - Data Infrastructure & Big Data
Specialized for data engineering, platform architecture, and big data processing roles. Highlights experience with Apache Spark, Snowflake, AWS, and building scalable data pipelines processing millions of records.

### 6. [Product](outputs/product/) - Product Management & Platform Development
Focused on product management, platform development, and technical architecture. Emphasizes cross-functional team leadership, product strategy, and technical decision-making experience.

### 7. [Software Engineering](outputs/software_engineering/) - Full-Stack Development
Highlights software engineering experience including Drupal (versions 4-10), GeoDjango, Flask, and cloud-based applications. Perfect for full-stack developer and software engineer positions.

### 8. [GIS](outputs/gis/) - Geospatial Analysis & Mapping
Specialized for GIS analyst, cartographer, and geospatial developer roles. Emphasizes ESRI Arc Suite, SAFE Systems, and OSGeo technology stack experience across all career positions.

### Length Variants

- **Long Versions (3 pages)**: Complete work history with detailed accomplishments, all key achievements and competencies, comprehensive job descriptions
- **Short Versions (2 pages)**: Focused on key achievements and recent experience, condensed job descriptions, streamlined competencies

## 📁 Finding Your Resumes

All generated resumes are located in the `outputs/` directory, organized by category and color scheme:

### Directory Structure
```
outputs/
├── comprehensive/                    # Complete professional profile
│   ├── long/                        # 3-page versions
│   │   ├── default_professional/
│   │   ├── corporate_blue/
│   │   ├── modern_tech/
│   │   └── ... (8 color schemes)
│   └── short/                       # 2-page versions
│       ├── default_professional/
│       ├── corporate_blue/
│       └── ... (8 color schemes)
├── polling_research_redistricting/  # Survey methodology & redistricting
├── marketing/                       # Market intelligence & strategy
├── data_analysis_visualization/    # Statistical analysis & data visualization
├── data_engineering/               # Data infrastructure & big data
├── product/                        # Product management & platform development
├── software_engineering/           # Full-stack development
└── gis/                           # Geospatial analysis & mapping
```

### File Naming Convention
Each resume follows this naming pattern:
`dheeraj_chand_[category]_[length]_[color_scheme].[format]`

**Examples:**
- `dheeraj_chand_comprehensive_long_default_professional.pdf`
- `dheeraj_chand_polling_research_redistricting_short_corporate_blue.docx`
- `dheeraj_chand_marketing_long_modern_tech.md`

### Quick Access

#### Most Popular Formats
- **[Comprehensive Long](outputs/comprehensive/long/default_professional/)** - Complete 3-page professional profile
- **[Comprehensive Short](outputs/comprehensive/short/corporate_blue/)** - ATS-friendly 2-page version
- **[Data Analysis & Visualization Long](outputs/data_analysis_visualization/long/modern_tech/)** - Statistical analysis & visualization expertise
- **[Data Engineering Long](outputs/data_engineering/long/modern_tech/)** - Big data & infrastructure focus

#### Role-Specific Resumes
- **[Research & Polling](outputs/polling_research_redistricting/long/default_professional/)** - Survey methodology & redistricting
- **[Marketing & Strategy](outputs/marketing/long/corporate_blue/)** - Market intelligence & consumer insights
- **[Product Management](outputs/product/long/modern_clean/)** - Product strategy & platform development
- **[Software Engineering](outputs/software_engineering/long/modern_tech/)** - Full-stack development & Drupal expertise
- **[GIS & Mapping](outputs/gis/long/cartographic_professional/)** - Geospatial analysis & ESRI/OSGeo stack

#### All Categories
- [Comprehensive](outputs/comprehensive/) - Complete professional profile
- [Polling/Research/Redistricting](outputs/polling_research_redistricting/) - Survey methodology & redistricting
- [Marketing](outputs/marketing/) - Market intelligence & strategy
- [Data Analysis & Visualization](outputs/data_analysis_visualization/) - Statistical analysis & data visualization
- [Data Engineering](outputs/data_engineering/) - Data infrastructure & big data
- [Product](outputs/product/) - Product management & platform development
- [Software Engineering](outputs/software_engineering/) - Full-stack development
- [GIS](outputs/gis/) - Geospatial analysis & mapping

## 🌟 What Makes These Resumes Special

### Professional Impact
- **Presidential Campaign Experience**: Polling for presidential, gubernatorial, congressional, and senatorial campaigns affecting millions of dollars in spending decisions
- **Massive Data Scale**: Built data warehouses processing millions of records with millions of columns for electoral analytics
- **Cost Savings**: Engineered FLEEM system saving PAC nearly $1 million annually in polling costs
- **Expert Testimony**: Regular source on public opinion for journalists, elected officials, and NGO leadership
- **Court Cases**: Redistricting analysis used in court cases with rigorous methodology

### Technical Excellence
- **Space-Efficient Design**: Optimized layout maximizing content while maintaining readability
- **ATS-Friendly Format**: Clean structure that passes Applicant Tracking Systems
- **Systematic Spacing**: Perfectly consistent spacing throughout all documents
- **Professional Typography**: ATS-friendly fonts with strategic visual hierarchy
- **Multiple Formats**: PDF, DOCX, RTF, and Markdown for any application system

### Content Highlights
- **21 Years Experience**: Comprehensive career spanning research, data engineering, and software development
- **Team Leadership**: Managed teams of 6-11 engineers, designers, and analysts
- **Platform Development**: Created redistricting software used by thousands of analysts nationwide
- **Democratic Party Impact**: Built first collaborative poll of polls used by the Democratic Party
- **Revenue Generation**: Delivered $4.9M additional revenue through marketing optimization

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (for Heroku)

### Design System

The system uses a systematic design approach with centralized constants:

- **Spacing System**: Consistent spacing hierarchy using `SPACE_BASE` unit
- **Typography System**: Font size hierarchy (8-14pt range)
- **Color System**: 4-color hierarchy (Primary, Secondary, Accent, Muted)
- **Layout System**: Consistent margins and positioning across all pages

### Customizing Content

Resume content is stored in JSON files in the `inputs/` directory. Each resume version has:
- `resume_data.json`: Personal information, experience, education, etc.
- `config.json`: Color scheme and formatting options

### Adding New Color Schemes

1. Create a new JSON file in `color_schemes/`
2. Define color values for all required keys following the 4-color hierarchy
3. The system will automatically detect and use the new scheme

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run specific tests:
```bash
python manage.py test resumes.tests.test_core_services
```

## 📊 Performance

- **Generation Speed**: ~2-3 seconds per resume
- **Memory Usage**: ~50MB for full generation
- **Total Generated Files**: 512 files (8 categories × 2 lengths × 4 formats × 8 color schemes)
- **File Sizes**: 
  - PDF: ~12KB (optimized for all services)
  - DOCX: ~39KB (excellent compatibility)
  - RTF: 20-60KB
  - Markdown: 5-15KB

## 🎨 Design System Features

### Systematic Spacing
- **Perfect Spacing Consistency**: Company-to-tagline distance = Tagline-to-responsibilities distance
- **Systematic Spacing Scale**: TINY (0.05) → MINIMAL (0.1) → SMALL (0.25) → MEDIUM (0.5) → LARGE (0.75)
- **Job Unit Spacing**: Optimized spacing between different job entries (reduced for better page utilization)
- **Component Spacing**: Minimal spacing within job units for clean appearance
- **Header Bar Positioning**: Dynamic positioning based on content (GitHub presence)
- **Margin System**: Calculated margins ensure consistent content positioning across all pages
- **No Double Spacing**: Eliminated extra spacers that caused inconsistent spacing

### Font Theme System
- **ATS-Friendly Typography**: Uses only ReportLab built-in fonts for maximum compatibility
- **Theme-Specific Variations**: Each color scheme has distinctive font combinations
- **Strategic Font Usage**: Bold for headers, regular for body, monospace for technical content
- **Font Size Variations**: Dramatic size differences for visual distinction
- **Professional Appearance**: Maintains readability while adding personality

### Typography Hierarchy
- **Section Headers**: 12pt bold for major sections
- **Company Names**: 12pt bold for company names
- **Job Titles**: 11pt for job titles
- **Body Text**: 11pt for main content
- **Bullet Points**: 10pt for bulleted lists
- **Footer Text**: 9pt for page numbers and links

### Color System
- **4-Color Hierarchy**: Primary, Secondary, Accent, Muted
- **Consistent Application**: Same color roles across all color schemes
- **Accessibility**: High contrast ratios for readability

### Document Structure & Links

#### First Page Header
- **Left Side**: Email, Phone, GitHub (stacked vertically)
  - Email: Accent color, clickable mailto link
  - Phone: Accent color, clickable tel link with +1 country code
  - GitHub: Link color, clickable to GitHub profile
- **Right Side**: Full name (large, bold) + Austin, TX location
  - Name: Primary color, 28pt bold
  - Location: Muted color, clickable OpenStreetMap link with coordinates
- **Header Bar**: Muted color, positioned under left content

#### Recurring Page Headers
- **Left**: Name (all caps, bold, primary color)
- **Center**: Email (accent color, clickable)
- **Right**: Phone + GitHub (stacked, both clickable)
  - Phone: Accent color, tel link
  - GitHub: Link color, smaller font

#### Footer
- **Left**: Website + LinkedIn (pipe separated)
  - Labels in accent color, links in respective brand colors
  - Website: Clickable to personal site
  - LinkedIn: Clickable to LinkedIn profile (LinkedIn blue)
- **Right**: Page number (accent color)
- **Footer Bar**: Muted color, separates from content

#### Content Colors
- **Section Headers**: Primary color, bold, 12pt
- **Company Names**: Primary color, bold, 12pt
- **Job Titles**: Muted color, 11pt
- **Body Text**: Secondary color, 11pt
- **Bullet Points**: Muted color, 10pt

#### Core Competencies (Special 3-Color Hierarchy)
- **Main Categories**: Primary color, bold (e.g., "Research and Analytics:")
- **Sub-categories**: Accent color, italic (e.g., "Statistical Analysis")
- **Details**: Muted color, parentheses (e.g., "(R, Python, SQL)")
- **Format**: Inline paragraph with semicolon separators for compact presentation

#### Key Achievements (Structured Format)
- **Category Headers**: Primary color, bold (e.g., "Software Development")
- **Achievement Bullets**: Muted color, bullet points
- **Spacing**: Consistent subheader-to-bullets spacing

## 🚀 Deployment

### Heroku Configuration

The app is pre-configured for Heroku deployment with:
- `Procfile` for web process
- `runtime.txt` for Python version
- `requirements.txt` for dependencies
- Environment variable configuration
- Static file handling with WhiteNoise

### Production Checklist

- [ ] Set `SECRET_KEY` environment variable
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure static file serving
- [ ] Set up logging
- [ ] Configure email settings

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- `getting-started.md` - Quick start guide
- `user-manual.md` - Detailed user guide
- `developer-guide.md` - Developer documentation
- `api-documentation.md` - API reference
- `troubleshooting.md` - Common issues and solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting guide
- Review the documentation
- Open an issue on GitHub

## 🎉 Acknowledgments

- ReportLab for PDF generation
- python-docx for Word document generation
- Django for the web framework
- All contributors and users

---

**Generated using Resume Generator System** - A comprehensive solution for professional resume creation.