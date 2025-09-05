"""
Django models for Resume Generator
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import json


class ResumeTemplate(models.Model):
    """Base resume template with role-specific customizations"""
    
    ROLE_CHOICES = [
        ('software_engineer', 'Software Engineer'),
        ('data_scientist', 'Data Scientist'),
        ('research_analyst', 'Research Analyst'),
        ('product_manager', 'Product Manager'),
        ('consultant', 'Consultant'),
        ('general', 'General'),
    ]
    
    VERSION_CHOICES = [
        ('long', 'Long (CV Style)'),
        ('short', 'Short (1-2 pages)'),
    ]
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    version = models.CharField(max_length=10, choices=VERSION_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['role', 'version']
        ordering = ['role', 'version']
    
    def __str__(self):
        return f"{self.get_role_display()} - {self.get_version_display()}"


class PersonalInfo(models.Model):
    """Personal information for resumes"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_info')
    
    # Basic Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Professional Summary
    summary = models.TextField(help_text="Professional summary or objective")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - Personal Info"


class CompetencyCategory(models.Model):
    """Competency categories (e.g., Programming Languages, Tools)"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Competency Categories"
    
    def __str__(self):
        return self.name


class Competency(models.Model):
    """Individual competencies/skills"""
    
    category = models.ForeignKey(CompetencyCategory, on_delete=models.CASCADE, related_name='competencies')
    name = models.CharField(max_length=100)
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    years_experience = models.PositiveIntegerField(default=0)
    is_highlighted = models.BooleanField(default=False, help_text="Highlight this skill")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category__order', 'order', 'name']
        unique_together = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_proficiency_level_display()})"


class Experience(models.Model):
    """Work experience entries"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    
    # Job Information
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    # Job Details
    description = models.TextField(help_text="Brief job description")
    achievements = models.JSONField(default=list, help_text="List of achievements")
    technologies = models.JSONField(default=list, help_text="Technologies used")
    
    # Ordering
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def duration(self):
        """Calculate job duration"""
        if self.is_current:
            return f"{self.start_date.year} - Present"
        elif self.end_date:
            return f"{self.start_date.year} - {self.end_date.year}"
        return f"{self.start_date.year}"


class Project(models.Model):
    """Personal or professional projects"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.JSONField(default=list)
    url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    is_highlighted = models.BooleanField(default=False)
    
    # Impact metrics
    impact_description = models.TextField(blank=True, help_text="Quantifiable impact or results")
    
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return self.name


class Education(models.Model):
    """Education entries"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    gpa_scale = models.DecimalField(max_digits=3, decimal_places=2, default=4.0)
    honors = models.CharField(max_length=200, blank=True)
    relevant_coursework = models.JSONField(default=list)
    
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.degree} from {self.institution}"


class Certification(models.Model):
    """Professional certifications"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    is_current = models.BooleanField(default=True)
    
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-issue_date', 'order']
    
    def __str__(self):
        return f"{self.name} from {self.issuer}"


class Achievement(models.Model):
    """Professional achievements and awards"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, help_text="e.g., Technical Leadership, Research, Innovation")
    date = models.DateField()
    organization = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date', 'order']
    
    def __str__(self):
        return self.title


class Resume(models.Model):
    """Generated resume instance"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    
    # Resume metadata
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Content (stored as JSON for flexibility)
    content = models.JSONField(default=dict)
    
    # File paths
    pdf_path = models.CharField(max_length=500, blank=True)
    docx_path = models.CharField(max_length=500, blank=True)
    rtf_path = models.CharField(max_length=500, blank=True)
    
    # Status
    is_generated = models.BooleanField(default=False)
    generation_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('generating', 'Generating'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def get_content_summary(self):
        """Get a summary of the resume content"""
        content = self.content
        return {
            'personal_info': content.get('personal_info', {}).get('full_name', 'Unknown'),
            'experience_count': len(content.get('experience', [])),
            'project_count': len(content.get('projects', [])),
            'competency_categories': len(content.get('competencies', {})),
        }


class ColorScheme(models.Model):
    """Color schemes for resume styling"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    colors = models.JSONField(default=dict, help_text="Color configuration as JSON")
    typography = models.JSONField(default=dict, help_text="Typography settings as JSON")
    layout = models.JSONField(default=dict, help_text="Layout settings as JSON")
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one default scheme
        if self.is_default:
            ColorScheme.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class ResumeGenerationJob(models.Model):
    """Track resume generation jobs"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generation_jobs')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='generation_jobs')
    
    job_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('queued', 'Queued'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='queued'
    )
    
    # Job parameters
    formats = models.JSONField(default=list, help_text="List of formats to generate")
    color_scheme = models.ForeignKey(ColorScheme, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Results
    result_files = models.JSONField(default=dict, help_text="Generated file paths")
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Job {self.job_id} - {self.resume.title}"