"""
Resume Generator Design Constants

This module contains all design constants, spacing rules, and color mappings
used throughout the resume generation system.
"""

from reportlab.lib.units import inch

# =============================================================================
# SPACING SYSTEM
# =============================================================================

# Base spacing unit - all other spacing is derived from this
SPACE_BASE = 0.2 * inch

# Spacing hierarchy
SPACE_BETWEEN_SECTIONS = SPACE_BASE * 0.5             # Between major sections (reduced)
SPACE_BETWEEN_JOB_UNITS = SPACE_BASE * 0.25           # Between different jobs (reduced)
SPACE_BETWEEN_JOB_COMPONENTS = SPACE_BASE / 4         # Within job units
SPACE_HEADER_TO_CONTENT = SPACE_BASE * 0.1            # Between headers and their content (minimal)
SPACE_HEADER_TOP = 0.4 * inch                         # Space for header on first page

# =============================================================================
# TYPOGRAPHY SYSTEM
# =============================================================================

# Font size hierarchy
FONT_SIZE_SECTION_HEADER = 12
FONT_SIZE_COMPANY = 12
FONT_SIZE_MAIN_COMPETENCY = 12
FONT_SIZE_JOB_TITLE = 11
FONT_SIZE_BODY = 11
FONT_SIZE_SUB_COMPETENCY = 11
FONT_SIZE_BULLET_POINT = 10
FONT_SIZE_COMPETENCY_DETAIL = 10
FONT_SIZE_FOOTER = 9

# =============================================================================
# COLOR MAPPING SYSTEM
# =============================================================================

# Color role definitions - maps JSON color keys to design elements
COLOR_MAPPINGS = {
    # Primary colors
    'SECTION_HEADER_COLOR': 'primary',      # Section titles
    'COMPANY_COLOR': 'primary',             # Company names
    'COMPETENCY_HEADER_COLOR': 'primary',   # Main competency categories
    
    # Secondary colors  
    'DARK_TEXT_COLOR': 'secondary',         # Body text, competency details
    'NAME_COLOR': 'secondary',              # Person's name
    
    # Accent colors
    'ACCENT_COLOR': 'accent',               # Sub-competencies, contact info
    'JOB_TITLE_COLOR': 'muted',             # Job titles (muted)
    'MEDIUM_TEXT_COLOR': 'muted',           # Bullet points (muted)
    'SUBTITLE_COLOR': 'muted',              # Subtitles (muted)
    'TITLE_COLOR': 'muted',                 # Page titles (muted)
}

# =============================================================================
# LAYOUT CONSTANTS
# =============================================================================

# Page dimensions
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11 * inch
MARGIN_LEFT = 0.6 * inch
MARGIN_RIGHT = 0.6 * inch
MARGIN_TOP = 0.6 * inch
MARGIN_BOTTOM = 0.8 * inch

# Header positioning
HEADER_BAR_POSITION_FIRST_PAGE = 10.2 * inch
HEADER_BAR_POSITION_RECURRING_PAGES = 10.4 * inch

# Footer positioning
FOOTER_BAR_POSITION = 0.6 * inch

# =============================================================================
# JOB SPLITTING RULES
# =============================================================================

# Job unit splitting logic
MAX_BULLETS_FOR_KEEP_TOGETHER = 3
BULLETS_WITH_HEADER = 2

# =============================================================================
# STYLE CONFIGURATION
# =============================================================================

# Paragraph style spacing (in points)
PARAGRAPH_SPACING = {
    'section_header': {
        'spaceAfter': 0.5,
        'spaceBefore': 0.5,
    },
    'company': {
        'spaceAfter': 0.25,
        'spaceBefore': 0.25,
    },
    'job_title': {
        'spaceAfter': 0.25,
        'spaceBefore': 0.25,
    },
    'body': {
        'spaceAfter': 0.5,
    },
    'bullet_point': {
        'spaceAfter': 0.25,
    },
    'main_competency': {
        'spaceAfter': 0.25,
        'spaceBefore': 0.25,
    },
    'sub_competency': {
        'spaceAfter': 0.25,
    },
    'competency_detail': {
        'spaceAfter': 0.25,
    },
}

# =============================================================================
# SECTION ORDER
# =============================================================================

# Define the order of sections in the resume
SECTION_ORDER = [
    'PROFESSIONAL SUMMARY',
    'KEY ACHIEVEMENTS AND IMPACT', 
    'CORE COMPETENCIES',
    'PROFESSIONAL EXPERIENCE',
    'KEY PROJECTS',
    'EDUCATION',
]

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_spacing_constant(name: str) -> float:
    """Get spacing constant by name"""
    spacing_map = {
        'base': SPACE_BASE,
        'sections': SPACE_BETWEEN_SECTIONS,
        'job_units': SPACE_BETWEEN_JOB_UNITS,
        'job_components': SPACE_BETWEEN_JOB_COMPONENTS,
        'header_to_content': SPACE_HEADER_TO_CONTENT,
        'header_top': SPACE_HEADER_TOP,
    }
    return spacing_map.get(name, SPACE_BASE)

def get_font_size(element: str) -> int:
    """Get font size for design element"""
    font_map = {
        'section_header': FONT_SIZE_SECTION_HEADER,
        'company': FONT_SIZE_COMPANY,
        'main_competency': FONT_SIZE_MAIN_COMPETENCY,
        'job_title': FONT_SIZE_JOB_TITLE,
        'body': FONT_SIZE_BODY,
        'sub_competency': FONT_SIZE_SUB_COMPETENCY,
        'bullet_point': FONT_SIZE_BULLET_POINT,
        'competency_detail': FONT_SIZE_COMPETENCY_DETAIL,
        'footer': FONT_SIZE_FOOTER,
    }
    return font_map.get(element, FONT_SIZE_BODY)

def get_color_role(json_color_key: str) -> str:
    """Get color role for JSON color key"""
    return COLOR_MAPPINGS.get(json_color_key, 'secondary')
