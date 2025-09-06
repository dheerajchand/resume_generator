# Developer Guide

## 🎯 What This Guide Covers

This guide is for developers who want to understand, modify, or extend the Resume Generator system. It covers the technical architecture, code structure, systematic design system, and how to make changes.

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface (Django)                   │
├─────────────────────────────────────────────────────────────┤
│  Views │ Templates │ Admin │ API │ User Management │ Files  │
├─────────────────────────────────────────────────────────────┤
│                Service Layer (Integration)                  │
├─────────────────────────────────────────────────────────────┤
│  Content Management │ Resume Generation │ File Processing   │
├─────────────────────────────────────────────────────────────┤
│              Functional Programming Layer                   │
├─────────────────────────────────────────────────────────────┤
│  Data Loading │ Validation │ Style Generation │ Content    │
├─────────────────────────────────────────────────────────────┤
│                    Database (SQLite)                        │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Django Layer**: Web interface, database, user management
2. **Service Layer**: Bridges Django and functional code
3. **Functional Layer**: Pure functions for data processing
4. **Database**: Stores all user data and configurations

## 📁 Project Structure

```
resume_generator/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                        # SQLite database
├── resume_generator_django/          # Django project settings
│   ├── __init__.py
│   ├── settings.py                   # Django configuration
│   ├── urls.py                       # Main URL routing
│   └── wsgi.py                       # WSGI configuration
├── resumes/                          # Main Django app
│   ├── models.py                     # Database models
│   ├── views.py                      # Web views and API
│   ├── services.py                   # Business logic
│   ├── serializers.py                # API serialization
│   ├── urls.py                       # App URL routing
│   ├── admin.py                      # Django admin interface
│   ├── apps.py                       # App configuration
│   ├── tests.py                      # Unit tests
│   └── management/                   # Custom management commands
│       └── commands/
│           └── setup_resume_system.py
├── content/                          # Content management
│   ├── base_content.json            # Base templates
│   └── role_overrides/              # Role-specific content
├── data_loader.py                    # Functional data loading
├── style_generator.py                # Functional style creation
├── data_validator.py                 # Functional validation
├── content_manager.py                # Content management
├── test_*.py                         # Test files
└── docs/                            # Documentation
```

## 🔧 Development Setup

### Prerequisites

- **Python 3.11+**: Required for the project
- **Git**: For version control
- **Text Editor**: VS Code, PyCharm, or similar
- **Terminal**: Command line interface

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/resume-generator.git
   cd resume-generator
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**:
   ```bash
   python manage.py migrate
   python manage.py setup_resume_system --create-superuser
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

### IDE Setup

#### VS Code

1. **Install Python extension**
2. **Open project folder**
3. **Select Python interpreter**: `venv/bin/python`
4. **Install recommended extensions**:
   - Python
   - Django
   - GitLens
   - Prettier

#### PyCharm

1. **Open project folder**
2. **Configure Python interpreter**: Point to `venv/bin/python`
3. **Enable Django support**: In settings
4. **Configure database**: SQLite should work automatically

## 🧩 Code Architecture

### Functional Programming Layer

#### Data Structures

```python
@dataclass
class ResumeData:
    personal_info: Dict[str, str]
    summary: str
    competencies: Dict[str, List[str]]
    experience: List[Dict[str, Any]]
    achievements: Dict[str, List[str]]
    metadata: Dict[str, Any]
```

#### Pure Functions

```python
def load_resume_data(file_path: str) -> ResumeData:
    """Load resume data from JSON file - pure function"""
    # No side effects, same input = same output
    pass

def validate_resume_data(data: ResumeData) -> ValidationResult:
    """Validate resume data - pure function"""
    # No side effects, returns validation result
    pass
```

### Django Models

#### Core Models

```python
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.JSONField(default=dict)
    # ... more fields
```

#### Relationships

```python
# One-to-One
PersonalInfo -> User

# One-to-Many
User -> Resume
User -> Experience
User -> Project

# Many-to-Many
Resume -> Competency (through CompetencyCategory)
```

### Service Layer

#### Content Management Service

```python
class ContentManagementService:
    def __init__(self):
        self.content_manager = ContentManager()
    
    def generate_resume_content(self, resume: Resume) -> Dict[str, Any]:
        """Generate content using functional approach"""
        # Uses functional modules
        # Returns structured data
        pass
```

#### Resume Generation Service

```python
class ResumeGenerationService:
    def generate_resume(self, resume: Resume, formats: List[str]) -> Dict[str, Any]:
        """Generate resume files using functional approach"""
        # Uses functional validation
        # Generates files
        # Returns file paths
        pass
```

## 🔨 Making Changes

### Adding New Resume Templates

1. **Create template in database**:
   ```python
   ResumeTemplate.objects.create(
       name="New Template",
       role="new_role",
       version="long",
       description="Description of new template"
   )
   ```

2. **Add content template**:
   ```python
   # In content_manager.py
   def get_content_template(self, role: str, version: str) -> ContentTemplate:
       if role == "new_role":
           return ContentTemplate(
               role="new_role",
               version=version,
               summary="Role-specific summary",
               competencies={...},
               experience=[],
               achievements={}
           )
   ```

3. **Update admin interface**:
   ```python
   # In admin.py
   @admin.register(ResumeTemplate)
   class ResumeTemplateAdmin(admin.ModelAdmin):
       list_display = ['name', 'role', 'version', 'is_active']
       list_filter = ['role', 'version', 'is_active']
   ```

### Adding New Color Schemes

1. **Create color scheme**:
   ```python
   ColorScheme.objects.create(
       name="New Color Scheme",
       description="Description",
       colors={
           'NAME_COLOR': '#FF5733',
           'TITLE_COLOR': '#33FF57',
           # ... more colors
       },
       typography={
           'FONT_MAIN': 'Arial',
           'NAME_SIZE': 24,
           # ... more typography
       }
   )
   ```

2. **Update style generator**:
   ```python
   # In style_generator.py
   def create_color_scheme_styles(colors: Dict[str, str]) -> Dict[str, ParagraphStyle]:
       # Add new color scheme logic
       pass
   ```

### Adding New Competency Categories

1. **Create category**:
   ```python
   CompetencyCategory.objects.create(
       name="New Category",
       description="Description",
       order=10
   )
   ```

2. **Add competencies**:
   ```python
   category = CompetencyCategory.objects.get(name="New Category")
   Competency.objects.create(
       category=category,
       name="New Skill",
       proficiency_level="intermediate",
       years_experience=2
   )
   ```

### Adding New File Formats

1. **Create generator function**:
   ```python
   def generate_tex(self, resume: Resume, content: Dict[str, Any], 
                   config_data: ConfigData, output_dir: str) -> str:
       """Generate LaTeX file"""
       # Implementation
       pass
   ```

2. **Update generation service**:
   ```python
   def _generate_single_format(self, resume: Resume, content: Dict[str, Any], 
                              config_data: ConfigData, format_type: str) -> Optional[str]:
       if format_type == 'tex':
           return self._generate_tex(resume, content, config_data, output_dir)
   ```

3. **Update models**:
   ```python
   class Resume(models.Model):
       # ... existing fields
       tex_path = models.CharField(max_length=500, blank=True)
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test resumes.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

#### Unit Tests

```python
def test_resume_creation():
    """Test resume creation"""
    user = User.objects.create_user('testuser')
    template = ResumeTemplate.objects.create(
        name="Test Template",
        role="general",
        version="long"
    )
    
    resume = Resume.objects.create(
        user=user,
        template=template,
        title="Test Resume"
    )
    
    assert resume.title == "Test Resume"
    assert resume.user == user
```

#### Integration Tests

```python
def test_resume_generation():
    """Test complete resume generation"""
    # Create test data
    # Generate resume
    # Verify files are created
    # Check content is correct
    pass
```

#### Functional Tests

```python
def test_placeholder_validation():
    """Test placeholder detection"""
    data = ResumeData(
        personal_info={'name': 'Your Name'},  # Placeholder
        summary='Test summary',
        # ... other fields
    )
    
    result = validate_resume_data(data)
    assert not result.is_valid
    assert 'placeholder' in str(result.errors)
```

## 🚀 Deployment

### Development Deployment

1. **Use Django's built-in server**:
   ```bash
   python manage.py runserver
   ```

2. **Access at**: http://127.0.0.1:8000/

### Production Deployment

#### Using Docker

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

2. **Build and run**:
   ```bash
   docker build -t resume-generator .
   docker run -p 8000:8000 resume-generator
   ```

#### Using Heroku

1. **Create Procfile**:
   ```
   web: python manage.py runserver 0.0.0.0:$PORT
   ```

2. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## 🔍 Debugging

### Common Issues

#### Database Issues

```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py setup_resume_system --create-superuser
```

#### Import Issues

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install missing packages
pip install -r requirements.txt
```

#### Permission Issues

```bash
# Fix file permissions
chmod +x manage.py
chmod -R 755 .
```

### Debugging Tools

#### Django Debug Toolbar

1. **Install**:
   ```bash
   pip install django-debug-toolbar
   ```

2. **Add to settings**:
   ```python
   INSTALLED_APPS = [
       # ... other apps
       'debug_toolbar',
   ]
   ```

#### Logging

```python
import logging
logger = logging.getLogger(__name__)

def some_function():
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
```

## 📚 API Reference

### Endpoints

#### Resume Management

- `GET /api/resumes/` - List all resumes
- `POST /api/resumes/` - Create new resume
- `GET /api/resumes/{id}/` - Get resume details
- `PUT /api/resumes/{id}/` - Update resume
- `DELETE /api/resumes/{id}/` - Delete resume

#### Content Management

- `GET /api/personal-info/` - Get personal information
- `PUT /api/personal-info/` - Update personal information
- `POST /api/experiences/` - Add experience
- `POST /api/projects/` - Add project

#### File Generation

- `POST /api/resumes/{id}/generate/` - Generate resume files
- `GET /api/resumes/{id}/download/{format}/` - Download file

### Authentication

```python
# Session authentication (default)
# No additional headers needed

# Token authentication (if enabled)
headers = {
    'Authorization': 'Token your-token-here'
}
```

## 🎨 Systematic Design System

### Overview

The Resume Generator uses a completely systematic design system with no hardcoded values. All spacing, typography, colors, and positioning are defined in `resume_generator_django/resume_generator/constants.py`.

### Spacing System

```python
# Systematic spacing scale (0.05, 0.1, 0.25, 0.5, 0.75, 1, 2, 4 units)
SPACE_MULTIPLIER_TINY = 0.05      # For very tight layouts (tagline-to-bullets)
SPACE_MULTIPLIER_MINIMAL = 0.1    # Minimal spacing (company-to-tagline, tagline-to-responsibilities)
SPACE_MULTIPLIER_SMALL = 0.25     # Small spacing (between bullets)
SPACE_MULTIPLIER_MEDIUM = 0.5     # Medium spacing
SPACE_MULTIPLIER_LARGE = 0.75     # Large spacing
```

### Font Theme System

```python
# Font themes for each color scheme - ATS-friendly typography
FONT_THEMES = {
    'modern_tech': {
        'primary': 'Helvetica-Bold',     # Bold for headers
        'secondary': 'Courier',          # Monospace for body text - tech feel
        'accent': 'Helvetica-Bold',      # Bold for job titles
        'technical': 'Courier',          # Monospace for code/data
        'fallback': 'Helvetica'
    },
    # ... other themes
}

# Font size variations by theme for distinctive typography
FONT_SIZE_THEMES = {
    'modern_tech': {
        'section_header': 16,    # Much larger for tech emphasis
        'company': 14,           # Much larger for tech companies
        'job_title': 13,         # Much larger for tech roles
        'body': 8,               # Much smaller for more content
        # ... other sizes
    }
}
```

### Typography System

```python
# Systematic font hierarchy (8, 9, 10, 11, 12, 14pt)
FONT_SIZE_8 = 8    # Footer text
FONT_SIZE_9 = 9    # Small text
FONT_SIZE_10 = 10  # Bullet points
FONT_SIZE_11 = 11  # Body text, job titles
FONT_SIZE_12 = 12  # Company names, section headers
FONT_SIZE_14 = 14  # Large headers
```

### Color System

```python
# 4-color hierarchy used consistently across all color schemes
COLOR_MAPPINGS = {
    'primary': 'COMPANY_COLOR',      # Company names, section headers
    'secondary': 'DARK_TEXT_COLOR',  # Body text
    'accent': 'ACCENT_COLOR',        # Links, highlights
    'muted': 'MEDIUM_TEXT_COLOR'     # Job titles, bullet points
}
```

### Positioning System

```python
# All positioning values centralized
PAGE_LEFT_MARGIN = 0.6 * inch
PAGE_RIGHT_MARGIN = 7.5 * inch
HEADER_LEFT_X = 0.6 * inch
HEADER_TOP_Y = 10.5 * inch
# ... and many more
```

### Perfect Spacing Consistency

- **Company → JobTitle**: `SPACE_MULTIPLIER_MINIMAL` (0.1)
- **JobTitle → Responsibilities**: `SPACE_MULTIPLIER_MINIMAL` (0.1) [IDENTICAL]
- **Responsibilities → Responsibilities**: `SPACE_MULTIPLIER_SMALL` (0.25)

### Adding New Constants

1. **Add to constants.py**:
```python
NEW_CONSTANT = value
```

2. **Import in core_services.py**:
```python
from resume_generator_django.resume_generator.constants import (
    # ... existing imports
    NEW_CONSTANT,
)
```

3. **Use systematically**:
```python
# Replace hardcoded values with constants
spaceAfter=get_spacing_constant('base') * NEW_CONSTANT
```

## 🎯 Best Practices

### Code Organization

1. **Keep functions pure**: No side effects
2. **Use type hints**: Better code documentation
3. **Write tests**: Test everything
4. **Document code**: Clear docstrings
5. **Follow PEP 8**: Python style guide

### Database Design

1. **Use appropriate field types**: CharField vs TextField
2. **Add indexes**: For frequently queried fields
3. **Use foreign keys**: For relationships
4. **Validate data**: At model and form level

### Security

1. **Validate input**: Never trust user input
2. **Use CSRF protection**: For forms
3. **Authenticate users**: For protected views
4. **Sanitize output**: Prevent XSS attacks

## 🚀 Contributing

### Getting Started

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes**: Follow best practices
4. **Write tests**: For new functionality
5. **Submit pull request**: With description

### Code Review Process

1. **Automated tests**: Must pass
2. **Code review**: By maintainers
3. **Documentation**: Update if needed
4. **Merge**: After approval

## 📞 Support

- **GitHub Issues**: For bug reports and feature requests
- **Email**: dev@resumegenerator.com
- **Documentation**: This guide and others in `/docs`

---

**Remember**: This is a living document. If you find something unclear or outdated, please let us know!
