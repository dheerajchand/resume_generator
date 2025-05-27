#!/usr/bin/env python3
"""
User Configuration Management System
Handles loading and managing user-specific settings for the resume generator
"""

import json
from pathlib import Path
from datetime import datetime

class UserConfig:
    """Manages user configuration for the resume generation system"""
    
    def __init__(self, config_file="user_config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self):
        """Load user configuration from JSON file"""
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"User configuration file '{self.config_file}' not found.\n"
                f"Please run 'python setup_user.py' to create your configuration."
            )
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config
        except Exception as e:
            raise ValueError(f"Error loading user configuration: {e}")
    
    def save_config(self, config_data):
        """Save configuration to file"""
        config_data['_metadata'] = {
            'created': datetime.now().isoformat(),
            'version': '1.0',
            'description': 'User configuration for Professional Resume Generator'
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    @property
    def name(self):
        """Get user's full name"""
        return self.config['personal_info']['name']
    
    @property
    def phone(self):
        """Get user's phone number"""
        return self.config['personal_info']['phone']
    
    @property
    def email(self):
        """Get user's email address"""
        return self.config['personal_info']['email']
    
    @property
    def website(self):
        """Get user's website URL"""
        return self.config['personal_info']['website']
    
    @property
    def linkedin(self):
        """Get user's LinkedIn URL"""
        return self.config['personal_info']['linkedin']
    
    @property
    def file_base_name(self):
        """Get base name for file naming (e.g., 'john_doe')"""
        return self.config['file_naming']['base_name']
    
    @property
    def directory_prefix(self):
        """Get prefix for directory naming (e.g., 'john_doe')"""
        return self.config['directory_naming']['prefix']
    
    def get_title(self, version_key):
        """Get professional title for a specific resume version"""
        return self.config['titles'].get(version_key, f"Professional {version_key.title()}")
    
    def get_personal_info(self):
        """Get complete personal info dictionary for resume data"""
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'linkedin': self.linkedin
        }
    
    def get_version_directory_name(self, version_key):
        """Get full directory name for a resume version"""
        version_names = {
            'research': 'research_focused',
            'technical': 'technical_detailed',
            'comprehensive': 'comprehensive_full',
            'consulting': 'consulting_minimal',
            'software': 'software_engineer',
            'marketing': 'product_marketing'
        }
        version_suffix = version_names.get(version_key, version_key)
        return f"{self.directory_prefix}_{version_suffix}"
    
    def get_output_filename(self, version_key, color_scheme, file_extension):
        """Generate output filename following naming convention"""
        return f"{self.file_base_name}_{version_key}_{color_scheme}.{file_extension}"
    
    @classmethod
    def create_default_config(cls):
        """Create a default configuration template"""
        return {
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
    
    def validate_config(self):
        """Validate that configuration has all required fields"""
        required_fields = [
            ['personal_info', 'name'],
            ['personal_info', 'email'],
            ['file_naming', 'base_name'],
            ['directory_naming', 'prefix']
        ]
        
        missing_fields = []
        for field_path in required_fields:
            current = self.config
            try:
                for key in field_path:
                    current = current[key]
                if not current or current.strip() == "":
                    missing_fields.append('.'.join(field_path))
            except KeyError:
                missing_fields.append('.'.join(field_path))
        
        if missing_fields:
            raise ValueError(
                f"Missing required configuration fields: {', '.join(missing_fields)}\n"
                f"Please run 'python setup_user.py' to update your configuration."
            )
    
    def __str__(self):
        """String representation for debugging"""
        return f"UserConfig(name='{self.name}', base_name='{self.file_base_name}')"