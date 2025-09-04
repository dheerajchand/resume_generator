#!/usr/bin/env python3
"""
Pure Data Loading Functions
Functional approach to loading and validating resume data
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass


@dataclass(frozen=True)
class ResumeData:
    """Immutable data structure for resume data"""
    personal_info: Dict[str, str]
    summary: str
    competencies: Dict[str, List[str]]
    experience: List[Dict[str, Any]]
    achievements: Dict[str, List[str]]
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class ConfigData:
    """Immutable data structure for configuration"""
    colors: Dict[str, str]
    typography: Dict[str, Union[str, int]]
    layout: Dict[str, Union[float, int, str]]
    metadata: Dict[str, Any]


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Pure function to load JSON data from file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary containing JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
        ValueError: If file cannot be read
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")


def validate_personal_info(personal_info: Dict[str, Any]) -> Dict[str, str]:
    """
    Pure function to validate and normalize personal info
    
    Args:
        personal_info: Raw personal info data
        
    Returns:
        Validated and normalized personal info
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    required_fields = ['name', 'email']
    optional_fields = ['phone', 'website', 'linkedin']
    
    # Check required fields
    missing_fields = [field for field in required_fields if not personal_info.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required personal info fields: {missing_fields}")
    
    # Normalize and validate
    validated = {}
    for field in required_fields + optional_fields:
        value = personal_info.get(field, '')
        if isinstance(value, str):
            validated[field] = value.strip()
        else:
            validated[field] = str(value).strip()
    
    return validated


def validate_competencies(competencies: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Pure function to validate and normalize competencies
    
    Args:
        competencies: Raw competencies data
        
    Returns:
        Validated competencies with normalized structure
        
    Raises:
        ValueError: If competencies structure is invalid
    """
    if not isinstance(competencies, dict):
        raise ValueError("Competencies must be a dictionary")
    
    validated = {}
    for category, skills in competencies.items():
        if isinstance(skills, list):
            validated[category] = [str(skill).strip() for skill in skills if skill]
        elif isinstance(skills, str):
            validated[category] = [skills.strip()] if skills.strip() else []
        else:
            validated[category] = []
    
    return validated


def validate_experience(experience: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Pure function to validate and normalize experience data
    
    Args:
        experience: Raw experience data
        
    Returns:
        Validated experience data
        
    Raises:
        ValueError: If experience structure is invalid
    """
    if not isinstance(experience, list):
        raise ValueError("Experience must be a list")
    
    validated = []
    for job in experience:
        if not isinstance(job, dict):
            continue
            
        validated_job = {
            'title': str(job.get('title', '')).strip(),
            'company': str(job.get('company', '')).strip(),
            'dates': str(job.get('dates', '')).strip(),
            'subtitle': str(job.get('subtitle', '')).strip(),
            'responsibilities': []
        }
        
        # Validate responsibilities
        responsibilities = job.get('responsibilities', [])
        if isinstance(responsibilities, list):
            validated_job['responsibilities'] = [
                str(resp).strip() for resp in responsibilities if resp
            ]
        
        validated.append(validated_job)
    
    return validated


def validate_achievements(achievements: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Pure function to validate and normalize achievements
    
    Args:
        achievements: Raw achievements data
        
    Returns:
        Validated achievements data
        
    Raises:
        ValueError: If achievements structure is invalid
    """
    if not isinstance(achievements, dict):
        return {}
    
    validated = {}
    for category, achievement_list in achievements.items():
        if isinstance(achievement_list, list):
            validated[category] = [
                str(achievement).strip() for achievement in achievement_list if achievement
            ]
        elif isinstance(achievement_list, str):
            validated[category] = [achievement_list.strip()] if achievement_list.strip() else []
        else:
            validated[category] = []
    
    return validated


def create_resume_data(raw_data: Dict[str, Any]) -> ResumeData:
    """
    Pure function to create validated ResumeData from raw data
    
    Args:
        raw_data: Raw data from JSON file
        
    Returns:
        Validated ResumeData object
        
    Raises:
        ValueError: If data validation fails
    """
    # Validate and normalize each section
    personal_info = validate_personal_info(raw_data.get('personal_info', {}))
    summary = str(raw_data.get('summary', '')).strip()
    competencies = validate_competencies(raw_data.get('competencies', {}))
    experience = validate_experience(raw_data.get('experience', []))
    achievements = validate_achievements(raw_data.get('achievements', {}))
    metadata = raw_data.get('_metadata', {})
    
    return ResumeData(
        personal_info=personal_info,
        summary=summary,
        competencies=competencies,
        experience=experience,
        achievements=achievements,
        metadata=metadata
    )


def load_resume_data(file_path: str) -> ResumeData:
    """
    Pure function to load and validate resume data from file
    
    Args:
        file_path: Path to resume data JSON file
        
    Returns:
        Validated ResumeData object
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If data validation fails
    """
    raw_data = load_json_file(file_path)
    return create_resume_data(raw_data)


def validate_config_colors(colors: Dict[str, Any]) -> Dict[str, str]:
    """
    Pure function to validate color configuration
    
    Args:
        colors: Raw color configuration
        
    Returns:
        Validated color configuration
        
    Raises:
        ValueError: If color validation fails
    """
    if not isinstance(colors, dict):
        raise ValueError("Colors must be a dictionary")
    
    validated = {}
    for key, value in colors.items():
        if key.endswith('_COLOR') and isinstance(value, str):
            # Basic hex color validation
            if value.startswith('#') and len(value) == 7:
                try:
                    int(value[1:], 16)  # Validate hex
                    validated[key] = value
                except ValueError:
                    raise ValueError(f"Invalid hex color: {value}")
            else:
                raise ValueError(f"Invalid color format: {value}")
    
    return validated


def validate_config_typography(typography: Dict[str, Any]) -> Dict[str, Union[str, int]]:
    """
    Pure function to validate typography configuration
    
    Args:
        typography: Raw typography configuration
        
    Returns:
        Validated typography configuration
    """
    if not isinstance(typography, dict):
        return {}
    
    validated = {}
    for key, value in typography.items():
        if key in ['FONT_MAIN', 'FONT_BOLD', 'FONT_ITALIC']:
            validated[key] = str(value)
        elif key in ['NAME_SIZE', 'TITLE_SIZE', 'SECTION_HEADER_SIZE', 
                     'JOB_TITLE_SIZE', 'BODY_SIZE', 'CONTACT_SIZE']:
            validated[key] = int(value) if isinstance(value, (int, str)) else 9
        else:
            validated[key] = value
    
    return validated


def validate_config_layout(layout: Dict[str, Any]) -> Dict[str, Union[float, int, str]]:
    """
    Pure function to validate layout configuration
    
    Args:
        layout: Raw layout configuration
        
    Returns:
        Validated layout configuration
    """
    if not isinstance(layout, dict):
        return {}
    
    validated = {}
    for key, value in layout.items():
        if key in ['PAGE_MARGIN', 'SECTION_SPACING', 'PARAGRAPH_SPACING', 'LINE_SPACING']:
            validated[key] = float(value) if isinstance(value, (int, float, str)) else 0.6
        elif key in ['JOB_SPACING', 'CATEGORY_SPACING', 'MAX_PAGES']:
            validated[key] = int(value) if isinstance(value, (int, str)) else 6
        elif key == 'BULLET_CHAR':
            validated[key] = str(value) if value else '▸'
        else:
            validated[key] = value
    
    return validated


def create_config_data(raw_config: Dict[str, Any]) -> ConfigData:
    """
    Pure function to create validated ConfigData from raw config
    
    Args:
        raw_config: Raw configuration data
        
    Returns:
        Validated ConfigData object
    """
    # Extract color keys
    color_keys = [k for k in raw_config.keys() if k.endswith('_COLOR')]
    colors = {k: raw_config[k] for k in color_keys if k in raw_config}
    validated_colors = validate_config_colors(colors)
    
    # Extract typography keys
    typography_keys = ['FONT_MAIN', 'FONT_BOLD', 'FONT_ITALIC', 'NAME_SIZE', 
                      'TITLE_SIZE', 'SECTION_HEADER_SIZE', 'JOB_TITLE_SIZE', 
                      'BODY_SIZE', 'CONTACT_SIZE']
    typography = {k: raw_config[k] for k in typography_keys if k in raw_config}
    validated_typography = validate_config_typography(typography)
    
    # Extract layout keys
    layout_keys = ['PAGE_MARGIN', 'SECTION_SPACING', 'PARAGRAPH_SPACING', 
                   'LINE_SPACING', 'JOB_SPACING', 'CATEGORY_SPACING', 
                   'MAX_PAGES', 'BULLET_CHAR']
    layout = {k: raw_config[k] for k in layout_keys if k in raw_config}
    validated_layout = validate_config_layout(layout)
    
    metadata = raw_config.get('_metadata', {})
    
    return ConfigData(
        colors=validated_colors,
        typography=validated_typography,
        layout=validated_layout,
        metadata=metadata
    )


def load_config_data(file_path: str) -> ConfigData:
    """
    Pure function to load and validate configuration data from file
    
    Args:
        file_path: Path to configuration JSON file
        
    Returns:
        Validated ConfigData object
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If configuration validation fails
    """
    raw_config = load_json_file(file_path)
    return create_config_data(raw_config)


def get_default_config() -> ConfigData:
    """
    Pure function to get default configuration
    
    Returns:
        Default ConfigData object
    """
    default_colors = {
        'NAME_COLOR': '#228B22',
        'TITLE_COLOR': '#B8860B',
        'SECTION_HEADER_COLOR': '#B8860B',
        'JOB_TITLE_COLOR': '#722F37',
        'ACCENT_COLOR': '#722F37',
        'COMPETENCY_HEADER_COLOR': '#228B22',
        'SUBTITLE_COLOR': '#228B22',
        'LINK_COLOR': '#B8860B',
        'DARK_TEXT_COLOR': '#333333',
        'MEDIUM_TEXT_COLOR': '#666666',
        'LIGHT_TEXT_COLOR': '#999999'
    }
    
    default_typography = {
        'FONT_MAIN': 'Helvetica',
        'FONT_BOLD': 'Helvetica-Bold',
        'FONT_ITALIC': 'Helvetica-Oblique',
        'NAME_SIZE': 24,
        'TITLE_SIZE': 14,
        'SECTION_HEADER_SIZE': 12,
        'JOB_TITLE_SIZE': 11,
        'BODY_SIZE': 9,
        'CONTACT_SIZE': 9
    }
    
    default_layout = {
        'PAGE_MARGIN': 0.6,
        'SECTION_SPACING': 0.12,
        'PARAGRAPH_SPACING': 0.06,
        'LINE_SPACING': 1.15,
        'JOB_SPACING': 6,
        'CATEGORY_SPACING': 4,
        'MAX_PAGES': 2,
        'BULLET_CHAR': '▸'
    }
    
    return ConfigData(
        colors=default_colors,
        typography=default_typography,
        layout=default_layout,
        metadata={'scheme_name': 'default_professional', 'created': 'system'}
    )


def load_config_with_fallback(config_path: Optional[str]) -> ConfigData:
    """
    Pure function to load config with fallback to default
    
    Args:
        config_path: Path to config file, or None for default
        
    Returns:
        ConfigData object (loaded or default)
    """
    if config_path and Path(config_path).exists():
        try:
            return load_config_data(config_path)
        except Exception:
            # Fall back to default if loading fails
            pass
    
    return get_default_config()
