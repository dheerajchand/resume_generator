#!/usr/bin/env python3
"""
Django Services for Resume Generation
Simplified services that use the core_services module
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.db import transaction

from .models import Resume, ResumeTemplate, PersonalInfo, Experience, Project, Education, Certification, Achievement, ColorScheme
from .serializers import ResumeSerializer

# Import our core services
from .core_services import ResumeGenerator, ResumeManager


class ResumeGenerationService:
    """Service for generating resumes using the core services"""
    
    def __init__(self):
        self.manager = ResumeManager()
    
    def generate_resume(self, version: str, color_scheme: str, format_type: str, output_dir: str = "outputs") -> Dict[str, Any]:
        """Generate a single resume"""
        try:
            success = self.manager.generate_single_resume(version, color_scheme, format_type, output_dir)
            
            if success:
                return {
                    "success": True,
                    "message": f"Resume generated successfully",
                    "version": version,
                    "color_scheme": color_scheme,
                    "format": format_type,
                    "output_path": f"{output_dir}/{version}/{color_scheme}/{format_type}/dheeraj_chand_{version}_{color_scheme}.{format_type}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to generate resume",
                    "version": version,
                    "color_scheme": color_scheme,
                    "format": format_type
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating resume: {str(e)}",
                "version": version,
                "color_scheme": color_scheme,
                "format": format_type
            }
    
    def generate_all_resumes(self, output_dir: str = "outputs") -> Dict[str, Any]:
        """Generate all resume combinations"""
        try:
            results = self.manager.generate_all_combinations(output_dir)
            
            return {
                "success": True,
                "message": "All resumes generated successfully",
                "results": results,
                "total_generated": results["success"],
                "total_failed": results["failed"]
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating all resumes: {str(e)}",
                "results": {"success": 0, "failed": 0}
            }
    
    def get_available_versions(self) -> List[str]:
        """Get list of available resume versions"""
        return list(self.manager.versions.keys())
    
    def get_available_color_schemes(self) -> List[str]:
        """Get list of available color schemes"""
        return self.manager.color_schemes.copy()
    
    def get_available_formats(self) -> List[str]:
        """Get list of available output formats"""
        return self.manager.formats.copy()


class ContentManagementService:
    """Service for managing resume content"""
    
    def __init__(self):
        self.inputs_dir = Path("inputs")
    
    def get_resume_data(self, version: str) -> Optional[Dict[str, Any]]:
        """Get resume data for a specific version"""
        try:
            version_mapping = {
                "research": "dheeraj_chand_research_focused",
                "technical": "dheeraj_chand_technical_detailed", 
                "comprehensive": "dheeraj_chand_comprehensive_full",
                "consulting": "dheeraj_chand_consulting_minimal",
                "software": "dheeraj_chand_software_engineer",
                "marketing": "dheeraj_chand_product_marketing"
            }
            
            if version not in version_mapping:
                return None
            
            input_basename = version_mapping[version]
            data_file = self.inputs_dir / input_basename / "resume_data.json"
            
            if not data_file.exists():
                return None
            
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error loading resume data for {version}: {e}")
            return None
    
    def get_config_data(self, version: str) -> Optional[Dict[str, Any]]:
        """Get config data for a specific version"""
        try:
            version_mapping = {
                "research": "dheeraj_chand_research_focused",
                "technical": "dheeraj_chand_technical_detailed", 
                "comprehensive": "dheeraj_chand_comprehensive_full",
                "consulting": "dheeraj_chand_consulting_minimal",
                "software": "dheeraj_chand_software_engineer",
                "marketing": "dheeraj_chand_product_marketing"
            }
            
            if version not in version_mapping:
                return None
            
            input_basename = version_mapping[version]
            config_file = self.inputs_dir / input_basename / "config.json"
            
            if not config_file.exists():
                return None
            
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error loading config data for {version}: {e}")
            return None
    
    def list_available_versions(self) -> List[str]:
        """List all available resume versions"""
        versions = []
        for item in self.inputs_dir.iterdir():
            if item.is_dir() and item.name.startswith("dheeraj_chand_"):
                # Extract version name from directory name
                version_name = item.name.replace("dheeraj_chand_", "").replace("_", " ")
                versions.append(version_name)
        return versions