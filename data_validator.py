#!/usr/bin/env python3
"""
Data Validation Functions for Resume Generator
Ensures no placeholder data and all required fields are present
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from data_loader import ResumeData, ConfigData


@dataclass(frozen=True)
class ValidationResult:
    """Immutable validation result"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]


def detect_placeholders(text: str) -> List[str]:
    """
    Pure function to detect placeholder text in content

    Args:
        text: Text to check for placeholders

    Returns:
        List of detected placeholder phrases
    """
    placeholders = [
        "Your Company Name",
        "Your City, ST",
        "YOUR FULL NAME",
        "Professional Title",
        "Your Website",
        "Your LinkedIn",
        "YOUR NAME",
        "Company Name",
        "Your City",
        "Your State",
        "Your Title",
        "Your Phone",
        "Your Email",
        "Your Address",
        "Your Website URL",
        "Your LinkedIn URL",
        "Your Company",
        "Your Job Title",
        "Your Employment Dates",
        "Your Location",
        "Your Responsibilities",
        "Your Achievements",
        "Your Skills",
        "Your Education",
        "Your Experience",
    ]

    found = [p for p in placeholders if p.lower() in text.lower()]
    return found


def validate_personal_info_no_placeholders(
    personal_info: Dict[str, str]
) -> ValidationResult:
    """
    Pure function to validate personal info has no placeholders

    Args:
        personal_info: Personal information dictionary

    Returns:
        ValidationResult with validation status
    """
    errors = []
    warnings = []

    # Check for placeholders in each field
    for field, value in personal_info.items():
        if not value or value.strip() == "":
            errors.append(f"Personal info field '{field}' is empty")
            continue

        placeholders = detect_placeholders(value)
        if placeholders:
            errors.append(
                f"Personal info field '{field}' contains placeholders: {placeholders}"
            )

    # Check for required fields
    required_fields = ["name", "email"]
    for field in required_fields:
        if field not in personal_info or not personal_info[field]:
            errors.append(f"Required personal info field '{field}' is missing")

    # Check email format
    if personal_info.get("email") and "@" not in personal_info["email"]:
        errors.append("Email address format is invalid")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


def validate_experience_no_placeholders(
    experience: List[Dict[str, Any]]
) -> ValidationResult:
    """
    Pure function to validate experience data has no placeholders

    Args:
        experience: List of experience entries

    Returns:
        ValidationResult with validation status
    """
    errors = []
    warnings = []

    if not experience:
        errors.append("At least one experience entry is required")
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

    required_fields = ["company", "title", "dates"]
    for i, exp in enumerate(experience):
        # Check required fields
        for field in required_fields:
            if field not in exp or not exp[field]:
                errors.append(f"Experience entry {i+1} missing required field: {field}")

        # Check for placeholders
        for field, value in exp.items():
            if isinstance(value, str):
                placeholders = detect_placeholders(value)
                if placeholders:
                    errors.append(
                        f"Experience entry {i+1} field '{field}' contains placeholders: {placeholders}"
                    )

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


def validate_competencies_no_placeholders(
    competencies: Dict[str, List[str]]
) -> ValidationResult:
    """
    Pure function to validate competencies have no placeholders

    Args:
        competencies: Competencies dictionary

    Returns:
        ValidationResult with validation status
    """
    errors = []
    warnings = []

    for category, skills in competencies.items():
        if not skills:
            warnings.append(f"Competency category '{category}' is empty")
            continue

        for skill in skills:
            placeholders = detect_placeholders(skill)
            if placeholders:
                errors.append(
                    f"Competency '{skill}' in category '{category}' contains placeholders: {placeholders}"
                )

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


def validate_achievements_no_placeholders(
    achievements: Dict[str, List[str]]
) -> ValidationResult:
    """
    Pure function to validate achievements have no placeholders

    Args:
        achievements: Achievements dictionary

    Returns:
        ValidationResult with validation status
    """
    errors = []
    warnings = []

    for category, achievement_list in achievements.items():
        if not achievement_list:
            warnings.append(f"Achievement category '{category}' is empty")
            continue

        for achievement in achievement_list:
            placeholders = detect_placeholders(achievement)
            if placeholders:
                errors.append(
                    f"Achievement '{achievement}' in category '{category}' contains placeholders: {placeholders}"
                )

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


def validate_resume_data_complete(resume_data: ResumeData) -> ValidationResult:
    """
    Pure function to validate complete resume data with no placeholders

    Args:
        resume_data: ResumeData object to validate

    Returns:
        ValidationResult with comprehensive validation status
    """
    all_errors = []
    all_warnings = []

    # Validate personal info
    personal_result = validate_personal_info_no_placeholders(resume_data.personal_info)
    all_errors.extend(personal_result.errors)
    all_warnings.extend(personal_result.warnings)

    # Validate experience
    experience_result = validate_experience_no_placeholders(resume_data.experience)
    all_errors.extend(experience_result.errors)
    all_warnings.extend(experience_result.warnings)

    # Validate competencies
    competencies_result = validate_competencies_no_placeholders(
        resume_data.competencies
    )
    all_errors.extend(competencies_result.errors)
    all_warnings.extend(competencies_result.warnings)

    # Validate achievements
    achievements_result = validate_achievements_no_placeholders(
        resume_data.achievements
    )
    all_errors.extend(achievements_result.errors)
    all_warnings.extend(achievements_result.warnings)

    # Check summary
    if not resume_data.summary or resume_data.summary.strip() == "":
        all_errors.append("Professional summary is required")
    else:
        summary_placeholders = detect_placeholders(resume_data.summary)
        if summary_placeholders:
            all_errors.append(
                f"Professional summary contains placeholders: {summary_placeholders}"
            )

    return ValidationResult(
        is_valid=len(all_errors) == 0, errors=all_errors, warnings=all_warnings
    )


def enforce_no_placeholders(resume_data: ResumeData) -> ResumeData:
    """
    Pure function to enforce no placeholders in resume data

    Args:
        resume_data: ResumeData object to validate

    Returns:
        Same ResumeData object if valid

    Raises:
        ValueError: If placeholders are detected
    """
    validation_result = validate_resume_data_complete(resume_data)

    if not validation_result.is_valid:
        error_message = (
            "Resume data contains placeholders or missing required information:\n"
        )
        error_message += "\n".join(f"  • {error}" for error in validation_result.errors)
        raise ValueError(error_message)

    if validation_result.warnings:
        print("⚠️  Warnings in resume data:")
        for warning in validation_result.warnings:
            print(f"  • {warning}")

    return resume_data


def create_validation_report(resume_data: ResumeData) -> str:
    """
    Pure function to create a detailed validation report

    Args:
        resume_data: ResumeData object to validate

    Returns:
        Detailed validation report string
    """
    validation_result = validate_resume_data_complete(resume_data)

    report = "Resume Data Validation Report\n"
    report += "=" * 40 + "\n\n"

    if validation_result.is_valid:
        report += "✅ VALIDATION PASSED\n"
        report += "No placeholders detected. Resume data is ready for generation.\n\n"
    else:
        report += "❌ VALIDATION FAILED\n"
        report += "The following issues must be fixed:\n\n"

        for i, error in enumerate(validation_result.errors, 1):
            report += f"{i}. {error}\n"

    if validation_result.warnings:
        report += "\n⚠️  WARNINGS:\n"
        for i, warning in enumerate(validation_result.warnings, 1):
            report += f"{i}. {warning}\n"

    return report


def validate_user_config_has_real_data(user_config: Dict[str, Any]) -> ValidationResult:
    """
    Pure function to validate user configuration has real data, not templates

    Args:
        user_config: User configuration dictionary

    Returns:
        ValidationResult with validation status
    """
    errors = []
    warnings = []

    # Check personal info
    personal_info = user_config.get("personal_info", {})
    personal_result = validate_personal_info_no_placeholders(personal_info)
    errors.extend(personal_result.errors)
    warnings.extend(personal_result.warnings)

    # Check if experience data is provided
    experience = user_config.get("experience", [])
    if not experience:
        errors.append("User must provide experience data - no templates allowed")
    else:
        experience_result = validate_experience_no_placeholders(experience)
        errors.extend(experience_result.errors)
        warnings.extend(experience_result.warnings)

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)
