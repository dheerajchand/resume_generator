#!/usr/bin/env python3
"""
Pure Style Generation Functions
Functional approach to creating ReportLab styles
"""

from typing import Dict, Any, Union
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from dataclasses import dataclass
from data_loader import ConfigData


@dataclass(frozen=True)
class StyleConfig:
    """Immutable style configuration"""

    name_color: str
    title_color: str
    section_header_color: str
    job_title_color: str
    competency_header_color: str
    subtitle_color: str
    link_color: str
    dark_text_color: str
    medium_text_color: str
    light_text_color: str
    font_main: str
    font_bold: str
    font_italic: str
    name_size: int
    title_size: int
    section_header_size: int
    job_title_size: int
    body_size: int
    contact_size: int
    line_spacing: float


def hex_to_color(hex_color: str) -> HexColor:
    """
    Pure function to convert hex color string to ReportLab HexColor

    Args:
        hex_color: Hex color string (e.g., '#FF0000')

    Returns:
        ReportLab HexColor object

    Raises:
        ValueError: If hex color is invalid
    """
    try:
        return HexColor(hex_color)
    except Exception as e:
        raise ValueError(f"Invalid hex color '{hex_color}': {e}")


def create_style_config(config_data: ConfigData) -> StyleConfig:
    """
    Pure function to create StyleConfig from ConfigData

    Args:
        config_data: Configuration data

    Returns:
        StyleConfig object
    """
    return StyleConfig(
        name_color=config_data.colors.get("NAME_COLOR", "#228B22"),
        title_color=config_data.colors.get("TITLE_COLOR", "#B8860B"),
        section_header_color=config_data.colors.get("SECTION_HEADER_COLOR", "#B8860B"),
        job_title_color=config_data.colors.get("JOB_TITLE_COLOR", "#722F37"),
        competency_header_color=config_data.colors.get(
            "COMPETENCY_HEADER_COLOR", "#228B22"
        ),
        subtitle_color=config_data.colors.get("SUBTITLE_COLOR", "#228B22"),
        link_color=config_data.colors.get("LINK_COLOR", "#B8860B"),
        dark_text_color=config_data.colors.get("DARK_TEXT_COLOR", "#333333"),
        medium_text_color=config_data.colors.get("MEDIUM_TEXT_COLOR", "#666666"),
        light_text_color=config_data.colors.get("LIGHT_TEXT_COLOR", "#999999"),
        font_main=config_data.typography.get("FONT_MAIN", "Helvetica"),
        font_bold=config_data.typography.get("FONT_BOLD", "Helvetica-Bold"),
        font_italic=config_data.typography.get("FONT_ITALIC", "Helvetica-Oblique"),
        name_size=config_data.typography.get("NAME_SIZE", 24),
        title_size=config_data.typography.get("TITLE_SIZE", 14),
        section_header_size=config_data.typography.get("SECTION_HEADER_SIZE", 12),
        job_title_size=config_data.typography.get("JOB_TITLE_SIZE", 11),
        body_size=config_data.typography.get("BODY_SIZE", 9),
        contact_size=config_data.typography.get("CONTACT_SIZE", 9),
        line_spacing=config_data.layout.get("LINE_SPACING", 1.15),
    )


def create_name_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create name style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for name
    """
    styles = getSampleStyleSheet()
    name_color = hex_to_color(style_config.name_color)

    return ParagraphStyle(
        name="NameStyle",
        parent=styles["Heading1"],
        fontSize=style_config.name_size,
        textColor=name_color,
        fontName=style_config.font_bold,
        alignment=TA_CENTER,
        spaceAfter=4,
        spaceBefore=0,
    )


def create_title_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create title style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for title
    """
    styles = getSampleStyleSheet()
    title_color = hex_to_color(style_config.title_color)

    return ParagraphStyle(
        name="TitleStyle",
        parent=styles["Normal"],
        fontSize=style_config.title_size,
        textColor=title_color,
        fontName=style_config.font_bold,
        alignment=TA_CENTER,
        spaceAfter=8,
        spaceBefore=0,
    )


def create_contact_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create contact style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for contact info
    """
    styles = getSampleStyleSheet()
    medium_text_color = hex_to_color(style_config.medium_text_color)

    return ParagraphStyle(
        name="ContactStyle",
        parent=styles["Normal"],
        fontSize=style_config.contact_size,
        textColor=medium_text_color,
        fontName=style_config.font_main,
        alignment=TA_CENTER,
        spaceAfter=12,
        spaceBefore=0,
    )


def create_section_header_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create section header style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for section headers
    """
    styles = getSampleStyleSheet()
    section_header_color = hex_to_color(style_config.section_header_color)

    return ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontSize=style_config.section_header_size,
        textColor=section_header_color,
        fontName=style_config.font_bold,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=8,
    )


def create_job_title_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create job title style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for job titles
    """
    styles = getSampleStyleSheet()
    job_title_color = hex_to_color(style_config.job_title_color)

    return ParagraphStyle(
        name="JobTitle",
        parent=styles["Normal"],
        fontSize=style_config.job_title_size,
        textColor=job_title_color,
        fontName=style_config.font_bold,
        spaceAfter=2,
        spaceBefore=4,
    )


def create_company_info_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create company info style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for company info
    """
    styles = getSampleStyleSheet()
    medium_text_color = hex_to_color(style_config.medium_text_color)

    return ParagraphStyle(
        name="CompanyInfo",
        parent=styles["Normal"],
        fontSize=style_config.body_size,
        textColor=medium_text_color,
        fontName=style_config.font_main,
        spaceAfter=2,
    )


def create_subtitle_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create subtitle style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for subtitles
    """
    styles = getSampleStyleSheet()
    subtitle_color = hex_to_color(style_config.subtitle_color)

    return ParagraphStyle(
        name="SubtitleStyle",
        parent=styles["Normal"],
        fontSize=style_config.body_size,
        textColor=subtitle_color,
        fontName=style_config.font_italic,
        spaceAfter=4,
    )


def create_body_text_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create body text style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for body text
    """
    styles = getSampleStyleSheet()
    dark_text_color = hex_to_color(style_config.dark_text_color)

    return ParagraphStyle(
        name="ResumeBodyText",
        parent=styles["Normal"],
        fontSize=style_config.body_size,
        textColor=dark_text_color,
        fontName=style_config.font_main,
        alignment=TA_JUSTIFY,
        spaceAfter=2,
        leading=style_config.body_size * style_config.line_spacing,
    )


def create_bullet_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create bullet style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for bullet points
    """
    styles = getSampleStyleSheet()
    dark_text_color = hex_to_color(style_config.dark_text_color)

    return ParagraphStyle(
        name="ResumeBulletStyle",
        parent=styles["Normal"],
        fontSize=style_config.body_size,
        textColor=dark_text_color,
        fontName=style_config.font_main,
        leftIndent=12,
        bulletIndent=0,
        spaceAfter=1.5,
        leading=style_config.body_size * style_config.line_spacing,
    )


def create_competency_header_style(style_config: StyleConfig) -> ParagraphStyle:
    """
    Pure function to create competency header style

    Args:
        style_config: Style configuration

    Returns:
        ParagraphStyle for competency headers
    """
    styles = getSampleStyleSheet()
    competency_header_color = hex_to_color(style_config.competency_header_color)

    return ParagraphStyle(
        name="CompetencyHeader",
        parent=styles["Normal"],
        fontSize=style_config.body_size + 1,
        textColor=competency_header_color,
        fontName=style_config.font_bold,
        spaceAfter=3,
        spaceBefore=4,
    )


def create_all_styles(config_data: ConfigData) -> Dict[str, ParagraphStyle]:
    """
    Pure function to create all paragraph styles from configuration

    Args:
        config_data: Configuration data

    Returns:
        Dictionary of style names to ParagraphStyle objects
    """
    style_config = create_style_config(config_data)

    return {
        "NameStyle": create_name_style(style_config),
        "TitleStyle": create_title_style(style_config),
        "ContactStyle": create_contact_style(style_config),
        "SectionHeader": create_section_header_style(style_config),
        "JobTitle": create_job_title_style(style_config),
        "CompanyInfo": create_company_info_style(style_config),
        "SubtitleStyle": create_subtitle_style(style_config),
        "ResumeBodyText": create_body_text_style(style_config),
        "ResumeBulletStyle": create_bullet_style(style_config),
        "CompetencyHeader": create_competency_header_style(style_config),
    }


def apply_color_scheme(
    styles: Dict[str, ParagraphStyle], color_scheme: Dict[str, str]
) -> Dict[str, ParagraphStyle]:
    """
    Pure function to apply a color scheme to existing styles

    Args:
        styles: Dictionary of existing styles
        color_scheme: Dictionary of color mappings

    Returns:
        New dictionary of styles with updated colors
    """
    # This would create new styles with updated colors
    # For now, return the original styles as this is a placeholder
    # In a full implementation, this would create new ParagraphStyle objects
    # with the updated colors from the color scheme
    return styles


def get_style_by_name(styles: Dict[str, ParagraphStyle], name: str) -> ParagraphStyle:
    """
    Pure function to get a style by name with fallback

    Args:
        styles: Dictionary of styles
        name: Name of the style to retrieve

    Returns:
        ParagraphStyle object

    Raises:
        KeyError: If style not found and no fallback available
    """
    if name in styles:
        return styles[name]

    # Fallback to default styles
    default_styles = getSampleStyleSheet()
    if name in default_styles:
        return default_styles[name]

    raise KeyError(f"Style '{name}' not found")


def validate_style_config(style_config: StyleConfig) -> bool:
    """
    Pure function to validate style configuration

    Args:
        style_config: Style configuration to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        # Test color conversion
        hex_to_color(style_config.name_color)
        hex_to_color(style_config.title_color)
        hex_to_color(style_config.section_header_color)
        hex_to_color(style_config.job_title_color)
        hex_to_color(style_config.competency_header_color)
        hex_to_color(style_config.subtitle_color)
        hex_to_color(style_config.link_color)
        hex_to_color(style_config.dark_text_color)
        hex_to_color(style_config.medium_text_color)
        hex_to_color(style_config.light_text_color)

        # Test size values
        assert style_config.name_size > 0
        assert style_config.title_size > 0
        assert style_config.section_header_size > 0
        assert style_config.job_title_size > 0
        assert style_config.body_size > 0
        assert style_config.contact_size > 0
        assert style_config.line_spacing > 0

        return True
    except Exception:
        return False
