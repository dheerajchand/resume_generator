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
SPACE_BETWEEN_JOB_UNITS = SPACE_BASE * 0.05           # Between different jobs (extremely minimal)
SPACE_BETWEEN_JOB_COMPONENTS = SPACE_BASE / 32        # Within job units (extremely minimal)
SPACE_HEADER_TO_CONTENT = SPACE_BASE * 0.4            # Between headers and their content (balanced)
SPACE_SUBHEADER_TO_BULLETS = SPACE_BASE * 0.1         # Between subheaders and their bullet lists (consistent)
SPACE_HEADER_TOP = 0.4 * inch                         # Space for header on first page
SPACE_HEADER_BAR_TO_CONTENT = SPACE_BASE * 0.3        # Between header bar and main content
SPACE_HEADER_HEIGHT = 0.6 * inch                      # Total height needed for header section
SPACE_FOOTER_HEIGHT = 0.4 * inch                      # Total height needed for footer section
SPACE_HEADER_TO_MAIN_BODY = SPACE_BASE * 0.2          # Space between header bar and main body content

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

# Header content positioning
HEADER_LEFT_X = 0.6 * inch
HEADER_TOP_Y = 10.5 * inch
HEADER_RIGHT_X = 7.5 * inch
HEADER_FOOTER_Y = 0.4 * inch

# Header content spacing
HEADER_PHONE_OFFSET = 0.2 * inch
HEADER_GITHUB_OFFSET = 0.35 * inch
HEADER_GITHUB_LINK_OFFSET = 0.4 * inch
HEADER_NAME_OFFSET = 0.075 * inch
HEADER_LOCATION_OFFSET = 0.2 * inch
HEADER_LOCATION_LINK_OFFSET = 0.25 * inch

# Footer content spacing
FOOTER_LINK_OFFSET = 0.05 * inch

# Spacing multipliers (systematic scale: 0.1, 0.25, 0.5, 0.75, 1, 2, 4)
SPACE_MULTIPLIER_MINIMAL = 0.1    # Minimal spacing
SPACE_MULTIPLIER_SMALL = 0.25     # Small spacing
SPACE_MULTIPLIER_MEDIUM = 0.5     # Medium spacing
SPACE_MULTIPLIER_LARGE = 0.75     # Large spacing

# Font sizes (systematic hierarchy: 8, 9, 10, 11, 12, 14pt)
FONT_SIZE_8 = 8
FONT_SIZE_9 = 9
FONT_SIZE_10 = 10
FONT_SIZE_11 = 11
FONT_SIZE_12 = 12
FONT_SIZE_14 = 14

# Bar dimensions
BAR_WIDTH = 6 * inch
BAR_HEIGHT = 2
BAR_LINE_WIDTH = 1
BAR_LINE_WIDTH_FOOTER = 0.5

# Page content positioning
PAGE_CONTENT_WIDTH = 6 * inch
PAGE_LEFT_MARGIN = 0.6 * inch
PAGE_RIGHT_MARGIN = 7.5 * inch

# Header content positioning (first page)
HEADER_FIRST_PHONE_Y = 10.5 * inch
HEADER_FIRST_GITHUB_Y = 10.35 * inch
HEADER_FIRST_NAME_Y = 10.425 * inch
HEADER_FIRST_LOCATION_Y = 10.225 * inch

# Header content positioning (recurring pages)
HEADER_RECURRING_NAME_Y = 10.5 * inch
HEADER_RECURRING_EMAIL_Y = 10.5 * inch
HEADER_RECURRING_PHONE_Y = 10.5 * inch
HEADER_RECURRING_GITHUB_Y = 10.35 * inch

# Footer positioning
FOOTER_Y = 0.4 * inch

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
        'subheader_to_bullets': SPACE_SUBHEADER_TO_BULLETS,
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
