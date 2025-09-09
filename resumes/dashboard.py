"""
Grappelli dashboard configuration for Resume Generator Admin
"""

from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import ModelList, LinkList, RecentActions


class CustomIndexDashboard(Dashboard):
    """Custom dashboard for Resume Generator Admin"""
    
    def init_with_context(self, context):
        """Initialize dashboard with context"""
        
        # User Management
        self.children.append(modules.Group(
            _('User Management'),
            column=1,
            collapsible=True,
            children=[
                ModelList(
                    _('Users & Profiles'),
                    column=1,
                    models=('resumes.CustomUser', 'resumes.UserProfile', 'resumes.UserDirectory'),
                ),
                ModelList(
                    _('User Resume Data'),
                    column=1,
                    models=('resumes.UserResumeData',),
                ),
            ]
        ))
        
        # Resume Management
        self.children.append(modules.Group(
            _('Resume Management'),
            column=1,
            collapsible=True,
            children=[
                ModelList(
                    _('Resumes & Templates'),
                    column=1,
                    models=('resumes.Resume', 'resumes.ResumeTemplate', 'resumes.ColorScheme'),
                ),
                ModelList(
                    _('Generation Jobs'),
                    column=1,
                    models=('resumes.ResumeGenerationJob',),
                ),
            ]
        ))
        
        # Content Management
        self.children.append(modules.Group(
            _('Content Management'),
            column=2,
            collapsible=True,
            children=[
                ModelList(
                    _('Personal Information'),
                    column=1,
                    models=('resumes.PersonalInfo',),
                ),
                ModelList(
                    _('Experience & Projects'),
                    column=1,
                    models=('resumes.Experience', 'resumes.Project', 'resumes.Achievement'),
                ),
                ModelList(
                    _('Education & Certifications'),
                    column=1,
                    models=('resumes.Education', 'resumes.Certification'),
                ),
                ModelList(
                    _('Skills & Competencies'),
                    column=1,
                    models=('resumes.CompetencyCategory', 'resumes.Competency'),
                ),
            ]
        ))
        
        # Quick Actions
        self.children.append(modules.LinkList(
            _('Quick Actions'),
            column=2,
            children=[
                {
                    'title': _('Generate All Resumes'),
                    'url': '/admin/resumes/resume/generate_all/',
                    'external': False,
                },
                {
                    'title': _('View Generated Files'),
                    'url': '/admin/resumes/resume/files/',
                    'external': False,
                },
                {
                    'title': _('User Statistics'),
                    'url': '/admin/resumes/resume/stats/',
                    'external': False,
                },
            ]
        ))
        
        # Recent Actions
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=10,
            collapsible=False,
            column=2,
        ))
        
        # System Information
        self.children.append(modules.LinkList(
            _('System Information'),
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'https://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'https://django-grappelli.readthedocs.io/',
                    'external': True,
                },
                {
                    'title': _('Resume Generator GitHub'),
                    'url': 'https://github.com/dheerajchand/resume_generator',
                    'external': True,
                },
            ]
        ))

