"""
Test suite for Resume Generator Services
"""

import json
import tempfile
from pathlib import Path
from django.test import TestCase
from unittest.mock import patch, MagicMock

from .services import ResumeGenerationService, ContentManagementService
from .core_services import ResumeGenerator, highlight_quantitative_metrics
from .models import CustomUser


class ResumeGenerationServiceTests(TestCase):
    """Test the ResumeGenerationService"""
    
    def setUp(self):
        self.service = ResumeGenerationService()
    
    def test_service_initialization(self):
        """Test that service initializes correctly"""
        self.assertIsNotNone(self.service.manager)
    
    def test_get_available_versions(self):
        """Test getting available resume versions"""
        versions = self.service.get_available_versions()
        self.assertIsInstance(versions, list)
        self.assertIn('comprehensive', versions)
        self.assertIn('software_engineering', versions)
    
    def test_get_available_color_schemes(self):
        """Test getting available color schemes"""
        schemes = self.service.get_available_color_schemes()
        self.assertIsInstance(schemes, list)
        self.assertIn('default_professional', schemes)
        self.assertIn('corporate_blue', schemes)
    
    def test_get_available_formats(self):
        """Test getting available output formats"""
        formats = self.service.get_available_formats()
        self.assertIsInstance(formats, list)
        self.assertIn('pdf', formats)
        self.assertIn('docx', formats)
        self.assertIn('rtf', formats)
        self.assertIn('md', formats)


class ResumeGeneratorCoreTests(TestCase):
    """Test the core ResumeGenerator functionality"""
    
    def setUp(self):
        # Create test data file
        self.test_data = {
            "personal_info": {
                "name": "Test User",
                "contact": {
                    "email": "test@example.com",
                    "phone": "123-456-7890",
                    "website": "https://example.com",
                    "linkedin": "https://linkedin.com/in/testuser",
                    "location": "Austin, TX"
                }
            },
            "summary": "Test professional summary",
            "achievements": {
                "Impact": [
                    "Test achievement 1",
                    "Test achievement 2"
                ]
            },
            "competencies": {
                "Programming": ["Python", "JavaScript"],
                "Data": ["SQL", "NoSQL"]
            },
            "experience": [
                {
                    "title": "Senior Developer",
                    "company": "Test Company",
                    "location": "Austin, TX",
                    "dates": "2020 - Present",
                    "subtitle": "Software Development",
                    "responsibilities": [
                        "Developed test applications",
                        "Led test projects"
                    ]
                },
                {
                    "title": "Junior Developer", 
                    "company": "Previous Company",
                    "location": "Austin, TX",
                    "dates": "2018 - 2020",
                    "subtitle": "Software Development",
                    "responsibilities": [
                        "Built test features",
                        "Maintained test systems"
                    ]
                }
            ]
        }
        
        # Create temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        
        # Create test config
        self.test_config = {
            "PRIMARY_COLOR": "#2C3E50",
            "SECONDARY_COLOR": "#34495E",
            "ACCENT_COLOR": "#3498DB",
            "MUTED_COLOR": "#7F8C8D"
        }
        
        self.config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_config, self.config_file)
        self.config_file.close()
    
    def tearDown(self):
        # Clean up temp files
        Path(self.temp_file.name).unlink(missing_ok=True)
        Path(self.config_file.name).unlink(missing_ok=True)
    
    def test_generator_initialization(self):
        """Test ResumeGenerator initialization"""
        generator = ResumeGenerator(
            self.temp_file.name,
            self.config_file.name,
            'default_professional',
            'long',
            'ats'
        )
        
        self.assertEqual(generator.color_scheme, 'default_professional')
        self.assertEqual(generator.length_variant, 'long')
        self.assertEqual(generator.output_type, 'ats')
        self.assertIsNotNone(generator.data)
        self.assertIsNotNone(generator.config)
    
    def test_contact_info_parsing_nested(self):
        """Test contact info parsing with nested structure"""
        generator = ResumeGenerator(self.temp_file.name)
        personal_info = self.test_data["personal_info"]
        
        contact_info = generator._get_contact_info(personal_info)
        
        self.assertEqual(contact_info["email"], "test@example.com")
        self.assertEqual(contact_info["phone"], "123-456-7890")
        self.assertEqual(contact_info["website"], "https://example.com")
    
    def test_contact_info_parsing_flat(self):
        """Test contact info parsing with flat structure"""
        generator = ResumeGenerator(self.temp_file.name)
        
        # Create flat structure (like short resumes)
        flat_personal_info = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "123-456-7890",
            "website": "https://example.com"
        }
        
        contact_info = generator._get_contact_info(flat_personal_info)
        
        self.assertEqual(contact_info["email"], "test@example.com")
        self.assertEqual(contact_info["phone"], "123-456-7890")
        self.assertEqual(contact_info["website"], "https://example.com")
    
    def test_date_parsing_for_sorting(self):
        """Test date parsing for chronological sorting"""
        generator = ResumeGenerator(self.temp_file.name)
        
        # Test current job
        result = generator._parse_date_for_sorting("2020 - Present")
        self.assertEqual(result, (9999, 2020))
        
        # Test completed job
        result = generator._parse_date_for_sorting("2018 - 2020")
        self.assertEqual(result, (2020, 2018))
        
        # Test single year
        result = generator._parse_date_for_sorting("2019")
        self.assertEqual(result, (2019, 2019))
        
        # Test complex date
        result = generator._parse_date_for_sorting("January 2018 - December 2020")
        self.assertEqual(result, (2020, 2018))
    
    def test_experience_sorting(self):
        """Test chronological sorting of experience"""
        generator = ResumeGenerator(self.temp_file.name)
        
        experience = [
            {"title": "Job 1", "dates": "2015 - 2017"},
            {"title": "Job 2", "dates": "2020 - Present"},
            {"title": "Job 3", "dates": "2018 - 2020"}
        ]
        
        sorted_experience = generator._sort_experience_chronologically(experience)
        
        # Should be: Present job, then 2020, then 2017
        self.assertEqual(sorted_experience[0]["title"], "Job 2")  # 2020 - Present
        self.assertEqual(sorted_experience[1]["title"], "Job 3")  # 2018 - 2020
        self.assertEqual(sorted_experience[2]["title"], "Job 1")  # 2015 - 2017


class QuantitativeMetricsHighlightingTests(TestCase):
    """Test the quantitative metrics highlighting functionality"""
    
    def test_highlight_dollar_amounts(self):
        """Test highlighting of dollar amounts"""
        text = "Saved organizations $4.7M through optimization"
        result = highlight_quantitative_metrics(text, "md")
        self.assertIn("**$4.7M**", result)
    
    def test_highlight_percentages(self):
        """Test highlighting of percentages"""
        text = "Improved accuracy from 23% to 64%"
        result = highlight_quantitative_metrics(text, "md")
        self.assertIn("**23%**", result)
        self.assertIn("**64%**", result)
    
    def test_highlight_large_numbers(self):
        """Test highlighting of large numbers"""
        text = "Processed 12,847 records"
        result = highlight_quantitative_metrics(text, "md")
        self.assertIn("**12,847**", result)
    
    def test_highlight_margin_of_error(self):
        """Test highlighting of margin of error"""
        text = "Reduced margin of error from ±4.2% to ±2.1%"
        result = highlight_quantitative_metrics(text, "md")
        self.assertIn("**±4.2%**", result)
        self.assertIn("**±2.1%**", result)
    
    def test_pdf_format_highlighting(self):
        """Test PDF format highlighting with color"""
        text = "Generated $4.7M in revenue"
        result = highlight_quantitative_metrics(text, "pdf", "#FF0000")
        self.assertIn('<font color="#FF0000"><b>$4.7M</b></font>', result)
    
    def test_docx_format_highlighting(self):
        """Test DOCX format highlighting with markers"""
        text = "Achieved 87% accuracy"
        result = highlight_quantitative_metrics(text, "docx")
        self.assertIn("**METRIC_HIGHLIGHT_START**87%**METRIC_HIGHLIGHT_END**", result)


class ContentManagementTests(TestCase):
    """Test content management functionality"""
    
    def setUp(self):
        self.service = ContentManagementService()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_service_initialization(self):
        """Test that content management service initializes correctly"""
        self.assertEqual(self.service.inputs_dir, Path("inputs"))
