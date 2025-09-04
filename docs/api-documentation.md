# API Documentation

## 🎯 Overview

This document describes the RESTful API for the Resume Generator system. The API allows you to programmatically create, manage, and generate resumes.

## 🔗 Base URL

- **Development**: `http://127.0.0.1:8000/api/`
- **Production**: `https://your-domain.com/api/`

## 🔐 Authentication

### Session Authentication (Default)

The API uses Django's session authentication by default. You need to be logged in through the web interface.

```bash
# Login through web interface first
curl -c cookies.txt -d "username=admin&password=admin123" http://127.0.0.1:8000/admin/login/

# Then use cookies for API calls
curl -b cookies.txt http://127.0.0.1:8000/api/resumes/
```

### Token Authentication (Optional)

If you enable token authentication:

```bash
# Get token
curl -X POST -d "username=admin&password=admin123" http://127.0.0.1:8000/api/auth/token/

# Use token in headers
curl -H "Authorization: Token your-token-here" http://127.0.0.1:8000/api/resumes/
```

## 📋 API Endpoints

### Resume Management

#### List All Resumes

```http
GET /api/resumes/
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "John Smith - Software Engineer",
      "description": "Resume for software engineering positions",
      "template": {
        "id": 1,
        "name": "Software Engineer - Long",
        "role": "software_engineer",
        "version": "long"
      },
      "is_generated": true,
      "generation_status": "completed",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z"
    }
  ]
}
```

#### Create New Resume

```http
POST /api/resumes/
```

**Request Body:**
```json
{
  "title": "Jane Doe - Data Scientist",
  "description": "Resume for data science positions",
  "template_id": 2
}
```

**Response:**
```json
{
  "id": 3,
  "title": "Jane Doe - Data Scientist",
  "description": "Resume for data science positions",
  "template": {
    "id": 2,
    "name": "Data Scientist - Long",
    "role": "data_scientist",
    "version": "long"
  },
  "is_generated": false,
  "generation_status": "pending",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

#### Get Resume Details

```http
GET /api/resumes/{id}/
```

**Response:**
```json
{
  "id": 1,
  "title": "John Smith - Software Engineer",
  "description": "Resume for software engineering positions",
  "template": {
    "id": 1,
    "name": "Software Engineer - Long",
    "role": "software_engineer",
    "version": "long"
  },
  "content": {
    "personal_info": {
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "(555) 123-4567",
      "website": "https://johnsmith.com",
      "linkedin": "https://linkedin.com/in/johnsmith",
      "github": "https://github.com/johnsmith",
      "location": "San Francisco, CA"
    },
    "summary": "Experienced software engineer with 5+ years of experience...",
    "competencies": {
      "Programming Languages": ["Python", "JavaScript", "TypeScript"],
      "Frameworks": ["Django", "React", "FastAPI"]
    },
    "experience": [
      {
        "title": "Senior Software Engineer",
        "company": "Tech Company Inc",
        "location": "San Francisco, CA",
        "dates": "2020-2023",
        "description": "Led development of scalable web applications",
        "achievements": [
          "Built microservices architecture serving 100,000+ users",
          "Implemented CI/CD pipeline reducing deployment time by 70%"
        ],
        "technologies": ["Python", "Django", "PostgreSQL", "React"]
      }
    ],
    "projects": [
      {
        "name": "E-commerce Platform",
        "description": "Full-stack e-commerce solution",
        "technologies": ["Python", "Django", "React", "PostgreSQL"],
        "url": "https://example.com",
        "github_url": "https://github.com/johnsmith/ecommerce",
        "impact": "Generated $1M+ in revenue"
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Science in Computer Science",
        "institution": "University of California, Berkeley",
        "location": "Berkeley, CA",
        "dates": "2016-2020",
        "gpa": "3.8/4.0",
        "honors": "Magna Cum Laude"
      }
    ],
    "certifications": [
      {
        "name": "AWS Certified Solutions Architect",
        "issuer": "Amazon Web Services",
        "date": "2022",
        "credential_id": "AWS-123456",
        "url": "https://aws.amazon.com/certification/"
      }
    ],
    "achievements": {
      "Technical Leadership": [
        "Led team of 5 developers",
        "Mentored 3 junior developers"
      ],
      "Project Success": [
        "Delivered 10+ successful projects",
        "Improved system performance by 50%"
      ]
    }
  },
  "is_generated": true,
  "generation_status": "completed",
  "pdf_path": "/media/generated_resumes/1/john_smith_software_engineer.pdf",
  "docx_path": "/media/generated_resumes/1/john_smith_software_engineer.docx",
  "rtf_path": "/media/generated_resumes/1/john_smith_software_engineer.rtf",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

#### Update Resume

```http
PUT /api/resumes/{id}/
```

**Request Body:**
```json
{
  "title": "John Smith - Senior Software Engineer",
  "description": "Updated resume for senior positions",
  "template_id": 1
}
```

#### Delete Resume

```http
DELETE /api/resumes/{id}/
```

**Response:**
```json
{
  "message": "Resume deleted successfully"
}
```

### Content Management

#### Get Personal Information

```http
GET /api/personal-info/
```

**Response:**
```json
{
  "full_name": "John Smith",
  "email": "john@example.com",
  "phone": "(555) 123-4567",
  "website": "https://johnsmith.com",
  "linkedin": "https://linkedin.com/in/johnsmith",
  "github": "https://github.com/johnsmith",
  "location": "San Francisco, CA",
  "summary": "Experienced software engineer with 5+ years of experience..."
}
```

#### Update Personal Information

```http
PUT /api/personal-info/
```

**Request Body:**
```json
{
  "full_name": "John Smith",
  "email": "john@example.com",
  "phone": "(555) 123-4567",
  "website": "https://johnsmith.com",
  "linkedin": "https://linkedin.com/in/johnsmith",
  "github": "https://github.com/johnsmith",
  "location": "San Francisco, CA",
  "summary": "Updated professional summary..."
}
```

#### Add Experience

```http
POST /api/experiences/
```

**Request Body:**
```json
{
  "title": "Senior Software Engineer",
  "company": "Tech Company Inc",
  "location": "San Francisco, CA",
  "start_date": "2020-01-01",
  "end_date": "2023-12-31",
  "is_current": false,
  "description": "Led development of scalable web applications",
  "achievements": [
    "Built microservices architecture serving 100,000+ users",
    "Implemented CI/CD pipeline reducing deployment time by 70%"
  ],
  "technologies": ["Python", "Django", "PostgreSQL", "React"]
}
```

**Response:**
```json
{
  "success": true,
  "id": 1,
  "message": "Experience added successfully"
}
```

#### Add Project

```http
POST /api/projects/
```

**Request Body:**
```json
{
  "name": "E-commerce Platform",
  "description": "Full-stack e-commerce solution with payment integration",
  "technologies": ["Python", "Django", "React", "PostgreSQL", "Stripe"],
  "url": "https://example.com",
  "github_url": "https://github.com/johnsmith/ecommerce",
  "start_date": "2023-01-01",
  "is_current": true,
  "is_highlighted": true,
  "impact_description": "Generated $1M+ in revenue for the company"
}
```

**Response:**
```json
{
  "success": true,
  "id": 1,
  "message": "Project added successfully"
}
```

#### Update Competencies

```http
POST /api/competencies/update/
```

**Request Body:**
```json
{
  "competency_ids": [1, 2, 3, 4, 5]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Competencies updated"
}
```

### File Generation

#### Generate Resume Files

```http
POST /api/resumes/{id}/generate/
```

**Request Body:**
```json
{
  "formats": ["pdf", "docx", "rtf"],
  "color_scheme_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "Resume generated successfully",
  "files": {
    "pdf": "/media/generated_resumes/1/john_smith_software_engineer.pdf",
    "docx": "/media/generated_resumes/1/john_smith_software_engineer.docx",
    "rtf": "/media/generated_resumes/1/john_smith_software_engineer.rtf"
  }
}
```

#### Download Resume File

```http
GET /api/resumes/{id}/download/{format}/
```

**Parameters:**
- `format`: `pdf`, `docx`, or `rtf`

**Response:**
- File download (binary content)

### Templates and Configuration

#### List Templates

```http
GET /api/templates/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Software Engineer - Long",
    "role": "software_engineer",
    "version": "long",
    "description": "Comprehensive software engineer resume with full experience details",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Software Engineer - Short",
    "role": "software_engineer",
    "version": "short",
    "description": "Concise software engineer resume (1-2 pages)",
    "is_active": true
  }
]
```

#### List Color Schemes

```http
GET /api/color-schemes/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Professional Blue",
    "description": "Clean, professional blue color scheme",
    "colors": {
      "NAME_COLOR": "#1F4E79",
      "TITLE_COLOR": "#2E5090",
      "SECTION_HEADER_COLOR": "#2E5090",
      "JOB_TITLE_COLOR": "#4682B4",
      "ACCENT_COLOR": "#4682B4"
    },
    "typography": {
      "FONT_MAIN": "Helvetica",
      "FONT_BOLD": "Helvetica-Bold",
      "NAME_SIZE": 24,
      "TITLE_SIZE": 14
    },
    "is_default": true,
    "is_active": true
  }
]
```

## 📊 Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

## 🔍 Error Responses

### Validation Error

```json
{
  "error": "Validation failed",
  "details": {
    "title": ["This field is required."],
    "email": ["Enter a valid email address."]
  }
}
```

### Authentication Error

```json
{
  "error": "Authentication required",
  "message": "Please log in to access this resource"
}
```

### Not Found Error

```json
{
  "error": "Not found",
  "message": "Resume with ID 999 does not exist"
}
```

## 🧪 Example Usage

### Complete Workflow

```bash
# 1. Login (get session cookie)
curl -c cookies.txt -d "username=admin&password=admin123" \
  http://127.0.0.1:8000/admin/login/

# 2. Create a new resume
curl -b cookies.txt -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "API Test Resume", "description": "Test resume via API", "template_id": 1}' \
  http://127.0.0.1:8000/api/resumes/

# 3. Add personal information
curl -b cookies.txt -X PUT \
  -H "Content-Type: application/json" \
  -d '{"full_name": "API Test User", "email": "test@example.com", "phone": "(555) 123-4567"}' \
  http://127.0.0.1:8000/api/personal-info/

# 4. Add experience
curl -b cookies.txt -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "Software Engineer", "company": "Test Company", "location": "Test City", "start_date": "2020-01-01", "description": "Test experience"}' \
  http://127.0.0.1:8000/api/experiences/

# 5. Generate resume
curl -b cookies.txt -X POST \
  -H "Content-Type: application/json" \
  -d '{"formats": ["pdf", "docx"], "color_scheme_id": 1}' \
  http://127.0.0.1:8000/api/resumes/1/generate/

# 6. Download PDF
curl -b cookies.txt -O \
  http://127.0.0.1:8000/api/resumes/1/download/pdf/
```

### Python Client Example

```python
import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:8000/api"

# Session for authentication
session = requests.Session()

# Login
login_data = {
    "username": "admin",
    "password": "admin123"
}
session.post("http://127.0.0.1:8000/admin/login/", data=login_data)

# Create resume
resume_data = {
    "title": "Python API Resume",
    "description": "Resume created via Python API",
    "template_id": 1
}
response = session.post(f"{BASE_URL}/resumes/", json=resume_data)
resume = response.json()
resume_id = resume["id"]

# Add personal information
personal_info = {
    "full_name": "Python API User",
    "email": "python@example.com",
    "phone": "(555) 123-4567",
    "location": "Python City, PC",
    "summary": "Experienced Python developer with API expertise"
}
session.put(f"{BASE_URL}/personal-info/", json=personal_info)

# Add experience
experience = {
    "title": "Python Developer",
    "company": "API Company Inc",
    "location": "API City, AC",
    "start_date": "2020-01-01",
    "end_date": "2023-12-31",
    "description": "Developed RESTful APIs using Python and Django",
    "achievements": [
        "Built API serving 1M+ requests per day",
        "Implemented automated testing reducing bugs by 80%"
    ],
    "technologies": ["Python", "Django", "FastAPI", "PostgreSQL"]
}
session.post(f"{BASE_URL}/experiences/", json=experience)

# Generate resume
generate_data = {
    "formats": ["pdf", "docx"],
    "color_scheme_id": 1
}
session.post(f"{BASE_URL}/resumes/{resume_id}/generate/", json=generate_data)

# Download PDF
pdf_response = session.get(f"{BASE_URL}/resumes/{resume_id}/download/pdf/")
with open("resume.pdf", "wb") as f:
    f.write(pdf_response.content)

print("Resume generated and downloaded successfully!")
```

## 🔧 Rate Limiting

The API has rate limiting to prevent abuse:

- **Default**: 1000 requests per hour per user
- **File Generation**: 10 requests per hour per user
- **Bulk Operations**: 100 requests per hour per user

## 📚 SDKs and Libraries

### Python

```python
# Install
pip install requests

# Use
import requests
# See Python example above
```

### JavaScript/Node.js

```javascript
// Install
npm install axios

// Use
const axios = require('axios');

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  withCredentials: true  // For session authentication
});

// Create resume
const resume = await api.post('/resumes/', {
  title: 'JavaScript API Resume',
  description: 'Resume created via JavaScript API',
  template_id: 1
});
```

### cURL

```bash
# See examples above
```

## 🆘 Support

- **API Issues**: Create a GitHub issue
- **Documentation**: Check this guide
- **Email**: api@resumegenerator.com

---

**Note**: This API is under active development. Some endpoints may change. Check the changelog for updates.
