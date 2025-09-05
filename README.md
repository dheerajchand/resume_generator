# Professional Resume Generator

A comprehensive Django-based resume generation system that creates professional resumes in multiple formats (PDF, DOCX, RTF, Markdown) with customizable color schemes and role-specific content.

## 🚀 Features

- **Multiple Output Formats**: PDF, DOCX, RTF, and Markdown
- **7 Professional Color Schemes**: Default, Corporate Blue, Modern Tech, Satellite Imagery, Terrain Mapping, Cartographic Professional, and Topographic Classic
- **6 Resume Versions**: Research, Technical, Comprehensive, Consulting, Software, and Marketing
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
│   ├── dheeraj_chand_comprehensive_full/
│   ├── dheeraj_chand_consulting_minimal/
│   ├── dheeraj_chand_product_marketing/
│   ├── dheeraj_chand_research_focused/
│   ├── dheeraj_chand_software_engineer/
│   └── dheeraj_chand_technical_detailed/
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
- 6 resume versions × 7 color schemes × 4 formats = 168 files

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

The system includes 7 professional color schemes:

1. **Default Professional** - Classic green and gold
2. **Corporate Blue** - Professional blue tones
3. **Modern Tech** - Contemporary tech colors
4. **Satellite Imagery** - Earth observation inspired
5. **Terrain Mapping** - Topographic map colors
6. **Cartographic Professional** - GIS professional theme
7. **Topographic Classic** - Traditional mapping colors

## 📝 Resume Versions

Six different resume versions are available:

1. **Research** - Academic and research focused
2. **Technical** - Technical skills emphasized
3. **Comprehensive** - Full detailed resume
4. **Consulting** - Business consulting focused
5. **Software** - Software engineering focused
6. **Marketing** - Product marketing focused

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (for Heroku)

### Customizing Content

Resume content is stored in JSON files in the `inputs/` directory. Each resume version has:
- `resume_data.json`: Personal information, experience, education, etc.
- `config.json`: Color scheme and formatting options

### Adding New Color Schemes

1. Create a new JSON file in `color_schemes/`
2. Define color values for all required keys
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
- **File Sizes**: 
  - PDF: 50-100KB
  - DOCX: 30-80KB
  - RTF: 20-60KB
  - Markdown: 5-15KB

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