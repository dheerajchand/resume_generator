#!/usr/bin/env python3
"""
Core Resume Generation Services
Consolidated functionality for resume generation across all formats
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle, PageTemplate, BaseDocTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import tempfile
from resume_generator_django.resume_generator.constants import (
    SPACE_BASE, SPACE_BETWEEN_SECTIONS, SPACE_BETWEEN_JOB_UNITS, 
    SPACE_BETWEEN_JOB_COMPONENTS, SPACE_HEADER_TO_CONTENT, SPACE_SUBHEADER_TO_BULLETS, SPACE_HEADER_TOP,
    SPACE_HEADER_BAR_TO_CONTENT, SPACE_HEADER_HEIGHT, SPACE_FOOTER_HEIGHT, SPACE_HEADER_TO_MAIN_BODY,
    FONT_SIZE_SECTION_HEADER, FONT_SIZE_COMPANY, FONT_SIZE_MAIN_COMPETENCY,
    FONT_SIZE_JOB_TITLE, FONT_SIZE_BODY, FONT_SIZE_SUB_COMPETENCY,
    FONT_SIZE_BULLET_POINT, FONT_SIZE_COMPETENCY_DETAIL, FONT_SIZE_FOOTER,
    COLOR_MAPPINGS, PARAGRAPH_SPACING, SECTION_ORDER,
    MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP, MARGIN_BOTTOM, PAGE_HEIGHT,
    HEADER_LEFT_X, HEADER_TOP_Y, HEADER_RIGHT_X, HEADER_FOOTER_Y,
    HEADER_PHONE_OFFSET, HEADER_GITHUB_OFFSET, HEADER_GITHUB_LINK_OFFSET,
    HEADER_NAME_OFFSET, HEADER_LOCATION_OFFSET, HEADER_LOCATION_LINK_OFFSET,
    FOOTER_LINK_OFFSET, FOOTER_BAR_POSITION, SPACE_MULTIPLIER_TINY, SPACE_MULTIPLIER_MINIMAL, SPACE_MULTIPLIER_SMALL, 
    SPACE_MULTIPLIER_MEDIUM, SPACE_MULTIPLIER_LARGE, FONT_SIZE_8, FONT_SIZE_9, 
    FONT_SIZE_10, FONT_SIZE_11, FONT_SIZE_12, FONT_SIZE_14, BAR_WIDTH, BAR_HEIGHT,
    BAR_LINE_WIDTH, BAR_LINE_WIDTH_FOOTER, PAGE_CONTENT_WIDTH, PAGE_LEFT_MARGIN,
    PAGE_RIGHT_MARGIN, HEADER_FIRST_PHONE_Y, HEADER_FIRST_GITHUB_Y, 
    HEADER_FIRST_NAME_Y, HEADER_FIRST_LOCATION_Y, HEADER_RECURRING_NAME_Y,
    HEADER_RECURRING_EMAIL_Y, HEADER_RECURRING_PHONE_Y, HEADER_RECURRING_GITHUB_Y,
    FOOTER_Y, FONT_THEMES, FONT_ROLES, FONT_SIZE_THEMES,
    get_spacing_constant, get_font_size, get_color_role, get_theme_font, get_theme_font_size
)




class ResumeGenerator:
    """Core resume generator supporting all formats"""
    
    def __init__(self, data_file: str, config_file: Optional[str] = None, color_scheme: str = 'default_professional'):
        self.data = self._load_json(data_file)
        self.config = self._load_json(config_file) if config_file else {}
        self.color_scheme = color_scheme
        self.styles = self._create_styles()
        
        # Spacing system constants (imported from settings)
        self.SPACE_BASE = SPACE_BASE
        self.SPACE_BETWEEN_SECTIONS = SPACE_BETWEEN_SECTIONS
        self.SPACE_BETWEEN_JOB_UNITS = SPACE_BETWEEN_JOB_UNITS
        self.SPACE_BETWEEN_JOB_COMPONENTS = SPACE_BETWEEN_JOB_COMPONENTS
        self.SPACE_HEADER_TO_CONTENT = SPACE_HEADER_TO_CONTENT
        self.SPACE_SUBHEADER_TO_BULLETS = SPACE_SUBHEADER_TO_BULLETS
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading {file_path}: {e}")
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create paragraph styles based on config with theme-specific fonts"""
        styles = getSampleStyleSheet()
        
        # Get colors from config (color schemes have colors directly, not wrapped in "colors")
        colors = self.config if self.config else {}
        
        # Get color scheme name for font theme selection
        color_scheme = getattr(self, 'color_scheme', 'default_professional')
        
        # Helper function to get theme-specific font with proper bold/italic handling
        def get_font(role, bold=False, italic=False):
            base_font = get_theme_font(color_scheme, role)
            
            # If the theme already specifies bold/italic, use it directly
            if '-Bold' in base_font or '-Oblique' in base_font:
                return base_font
            
            # Handle font variations for ReportLab
            if bold and italic:
                return f"{base_font}-BoldOblique"
            elif bold:
                return f"{base_font}-Bold"
            elif italic:
                return f"{base_font}-Oblique"
            else:
                return base_font
        
        custom_styles = {
            "Name": ParagraphStyle(
                "CustomName",
                parent=styles["Heading1"],
                fontSize=28,  # Bigger name - keep as special case, consistent across all themes
                textColor=HexColor(colors.get("NAME_COLOR", "#2C3E50")),
                alignment=TA_RIGHT,
                spaceAfter=get_spacing_constant('base') * 1,
                fontName=get_font('name', bold=True),
            ),
            "Title": ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading2"],
                fontSize=get_font_size('section_header'),
                textColor=HexColor(colors.get("TITLE_COLOR", "#34495E")),
                alignment=TA_CENTER,
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_LARGE,
                fontName=get_font('primary', bold=True),
            ),
            "Subtitle": ParagraphStyle(
                "CustomSubtitle",
                parent=styles["Normal"],
                fontSize=get_font_size('bullet_point'),
                textColor=HexColor(colors.get("TITLE_COLOR", "#7F8C8D")),
                alignment=TA_CENTER,
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_LARGE,
                fontName=get_font('secondary'),
            ),
            # DESIGN SYSTEM: Consistent spacing scale (0.25, 0.5, 1, 2, 4 units)
            # Typography hierarchy: 8, 9, 10, 11, 12, 14pt
            # Color hierarchy: primary, secondary, accent, muted
            
            "SectionHeader": ParagraphStyle(
                "CustomSectionHeader",
                parent=styles["Heading2"],
                fontSize=get_font_size('section_header'),
                textColor=HexColor(colors.get("SECTION_HEADER_COLOR", "#2C3E50")),
                spaceAfter=get_spacing_constant('header_to_content'),  # Minimal gap to content
                spaceBefore=get_spacing_constant('base') * SPACE_MULTIPLIER_MEDIUM,     # Medium units spacing - reduced whitespace between main sections
                fontName=get_font('primary', bold=True),
            ),
            "JobTitle": ParagraphStyle(
                "CustomJobTitle",
                parent=styles["Normal"],
                fontSize=get_font_size('job_title'),
                textColor=HexColor(colors.get("JOB_TITLE_COLOR", "#666666")),  # Muted color
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_MINIMAL,   # Minimal spacing - identical to company-to-tagline distance
                spaceBefore=get_spacing_constant('base') * SPACE_MULTIPLIER_SMALL,  # Small spacing
                fontName=get_font('accent'),
            ),
            "Company": ParagraphStyle(
                "CustomCompany",
                parent=styles["Heading3"],
                fontSize=get_font_size('company'),
                textColor=HexColor(colors.get("COMPANY_COLOR", "#2C3E50")),  # Primary color
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_MINIMAL,    # Minimal spacing after company
                spaceBefore=get_spacing_constant('base') * SPACE_MULTIPLIER_MINIMAL,   # Minimal spacing before company
                fontName=get_font('primary', bold=True),
            ),
            "Body": ParagraphStyle(
                "CustomBody",
                parent=styles["Normal"],
                fontSize=get_font_size('body'),
                textColor=HexColor(colors.get("DARK_TEXT_COLOR", "#2C3E50")),
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_MEDIUM,      # Medium unit spacing
                leftIndent=12,
                fontName=get_font('secondary'),
            ),
            "BulletPoint": ParagraphStyle(
                "CustomBulletPoint",
                parent=styles["Normal"],
                fontSize=get_font_size('bullet_point'),
                textColor=HexColor(colors.get("MEDIUM_TEXT_COLOR", "#666666")),
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_SMALL,    # Small unit spacing - tighter bullet spacing
                leftIndent=12,
                fontName=get_font('secondary'),
            ),
            "MainCompetency": ParagraphStyle(
                "CustomMainCompetency",
                parent=styles["Normal"],
                fontSize=get_font_size('main_competency'),
                textColor=HexColor(colors.get("COMPETENCY_HEADER_COLOR", "#2C3E50")),
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_MINIMAL,    # Minimal unit spacing - minimal gap to bullets
                spaceBefore=get_spacing_constant('base') * SPACE_MULTIPLIER_MINIMAL,   # Minimal unit spacing - minimal gap from previous
                fontName=get_font('primary', bold=True),
            ),
            "SubCompetency": ParagraphStyle(
                "CustomSubCompetency",
                parent=styles["Normal"],
                fontSize=get_font_size('sub_competency'),
                textColor=HexColor(colors.get("ACCENT_COLOR", "#4682B4")),
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_MEDIUM,    # Medium unit spacing
                leftIndent=12,
                fontName=get_font('accent', bold=True),
            ),
            "CompetencyDetail": ParagraphStyle(
                "CustomCompetencyDetail",
                parent=styles["Normal"],
                fontSize=get_font_size('competency_detail'),
                textColor=HexColor(colors.get("DARK_TEXT_COLOR", "#2C3E50")),
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_MEDIUM,    # Medium unit spacing
                leftIndent=0,
                fontName=get_font('secondary'),
                allowWidows=1,
                allowOrphans=1,
            ),
            "Contact": ParagraphStyle(
                "CustomContact",
                parent=styles["Normal"],
                fontSize=get_font_size('body'),
                textColor=HexColor(colors.get("ACCENT_COLOR", "#4682B4")),  # Use accent color for header contact
                alignment=TA_RIGHT,
                spaceAfter=get_spacing_constant('base') * 1,
                fontName=get_font('secondary'),
            ),
            "ContactStacked": ParagraphStyle(
                "CustomContactStacked",
                parent=styles["Normal"],
                fontSize=get_font_size('body'),
                textColor=HexColor(colors.get("ACCENT_COLOR", "#4682B4")),
                alignment=TA_RIGHT,
                spaceAfter=get_spacing_constant('base') * SPACE_MULTIPLIER_MEDIUM,
                fontName=get_font('secondary'),
            ),
        }
        
        return custom_styles
    
    def _get_sections(self):
        """Define and render all resume sections in order"""
        sections = []
        
        # Professional Summary
        summary = self.data.get("summary", "")
        if summary:
            sections.append({
                "name": "PROFESSIONAL SUMMARY",
                "content": [Paragraph(summary, self.styles["Body"])]
            })
        
        # Key Achievements and Impact
        achievements = self.data.get("achievements", {})
        if achievements:
            achievement_content = []
            for category, achievement_list in achievements.items():
                if isinstance(achievement_list, list):
                    achievement_content.append(Paragraph(category, self.styles["MainCompetency"]))
                    # Add small spacing between subheader and bullets (consistent with section headers)
                    achievement_content.append(Spacer(1, self.SPACE_HEADER_TO_CONTENT))
                    for achievement in achievement_list:
                        achievement_content.append(Paragraph(f"• {achievement}", self.styles["BulletPoint"]))
            
            sections.append({
                "name": "KEY ACHIEVEMENTS AND IMPACT",
                "content": achievement_content
            })
        
        # Core Competencies
        competencies = self.data.get("competencies", {})
        if competencies:
            competency_content = []
            for main_category, sub_skills in competencies.items():
                if isinstance(sub_skills, list):
                    # Build compact inline content with color hierarchy
                    colors = self.config if self.config else {}
                    accent_color = colors.get("ACCENT_COLOR", "#4682B4") 
                    muted_color = colors.get("MEDIUM_TEXT_COLOR", "#666666")
                    
                    sub_content = []
                    for skill_line in sub_skills:
                        if ": " in skill_line:
                            sub_category, details = skill_line.split(": ", 1)
                            sub_content.append(f'<font color="{accent_color}"><i>{sub_category}</i></font> <font color="{muted_color}">({details})</font>')
                        else:
                            sub_content.append(f'<font color="{accent_color}">{skill_line}</font>')
                    
                    # Create single paragraph with main category and all sub-skills using color hierarchy
                    # Main category in primary color, sub-categories in accent color, details in muted color
                    main_color = colors.get("COMPETENCY_HEADER_COLOR", "#2C3E50")
                    
                    full_text = f'<font color="{main_color}"><b>{main_category}:</b></font> {"; ".join(sub_content)}'
                    competency_content.append(Paragraph(full_text, self.styles["CompetencyDetail"]))
            
            sections.append({
                "name": "CORE COMPETENCIES",
                "content": competency_content
            })
        
        # Professional Experience
        experience = self.data.get("experience", [])
        if experience:
            experience_content = []
            for job in experience:
                job_title = job.get("title", "")
                company = job.get("company", "")
                location = job.get("location", "")
                dates = job.get("dates", "")
                
                # Company, job title, and dates on one line
                company_line = company
                if job_title:
                    company_line += f" | {job_title}"
                if location:
                    company_line += f" - {location}"
                if dates:
                    company_line += f" {dates}"
                
                # Intelligent job unit splitting logic
                job_unit = []
                job_unit.append(Paragraph(company_line, self.styles["Company"]))
                
                if job.get("subtitle"):
                    job_unit.append(Spacer(1, self.SPACE_BETWEEN_JOB_COMPONENTS))  # Spacing between company and subtitle
                    job_unit.append(Paragraph(job["subtitle"], self.styles["SubCompetency"]))
                
                responsibilities = job.get("responsibilities", [])
                
                # No additional spacing - JobTitle.spaceAfter already provides the correct spacing
                
                # If job has many responsibilities, allow splitting but keep header together
                if len(responsibilities) > 4:  # Increased threshold to 4
                    # Keep company + title + subtitle + first bullet together
                    header_unit = job_unit.copy()
                    # Add first bullet to header to ensure at least one stays with header
                    header_unit.append(Paragraph(f"• {responsibilities[0]}", self.styles["BulletPoint"]))
                    experience_content.append(KeepTogether(header_unit))
                    
                    # Add remaining bullets (can split across pages)
                    for resp in responsibilities[1:]:
                        experience_content.append(Paragraph(f"• {resp}", self.styles["BulletPoint"]))
                elif len(responsibilities) > 1:  # For jobs with 2-4 responsibilities
                    # Keep header + at least one bullet together
                    header_unit = job_unit.copy()
                    # Add first bullet to header to ensure at least one stays with header
                    header_unit.append(Paragraph(f"• {responsibilities[0]}", self.styles["BulletPoint"]))
                    experience_content.append(KeepTogether(header_unit))
                    
                    # Add remaining bullets (can split across pages)
                    for resp in responsibilities[1:]:
                        experience_content.append(Paragraph(f"• {resp}", self.styles["BulletPoint"]))
                else:
                    # For shorter jobs, keep everything together
                    for resp in responsibilities:
                        job_unit.append(Paragraph(f"• {resp}", self.styles["BulletPoint"]))
                    experience_content.append(KeepTogether(job_unit))
                
                # Add spacer between job units (but not after the last job)
                if job != experience[-1]:  # Only add spacer if not the last job
                    experience_content.append(Spacer(1, self.SPACE_BETWEEN_JOB_UNITS))
            
            sections.append({
                "name": "PROFESSIONAL EXPERIENCE",
                "content": experience_content
            })
        
        # Key Projects
        projects = self.data.get("projects", [])
        if projects:
            project_content = []
            for project in projects:
                project_name = project.get("name", "")
                dates = project.get("dates", "")
                description = project.get("description", "")
                technologies = project.get("technologies", [])
                impact = project.get("impact", "")
                
                title_line = project_name
                if dates:
                    title_line += f" ({dates})"
                
                project_content.append(Paragraph(title_line, self.styles["SubCompetency"]))
                
                if description:
                    project_content.append(Paragraph(description, self.styles["CompetencyDetail"]))
                
                if technologies:
                    tech_text = "Technologies: " + ", ".join(technologies)
                    project_content.append(Paragraph(tech_text, self.styles["CompetencyDetail"]))
                
                if impact:
                    project_content.append(Paragraph(f"Impact: {impact}", self.styles["CompetencyDetail"]))
            
            sections.append({
                "name": "KEY PROJECTS",
                "content": project_content
            })
        
        # Education
        education = self.data.get("education", [])
        if education:
            education_content = []
            for edu in education:
                degree = edu.get("degree", "")
                institution = edu.get("institution", "")
                location = edu.get("location", "")
                dates = edu.get("dates", "")
                gpa = edu.get("gpa", "")
                honors = edu.get("honors", "")
                
                title_line = degree
                if institution:
                    title_line += f" - {institution}"
                if location:
                    title_line += f" ({location})"
                if dates:
                    title_line += f" | {dates}"
                
                education_content.append(Paragraph(title_line, self.styles["JobTitle"]))
                
                if gpa:
                    education_content.append(Paragraph(f"GPA: {gpa}", self.styles["Body"]))
                
                if honors:
                    education_content.append(Paragraph(f"Honors: {honors}", self.styles["Body"]))
            
            sections.append({
                "name": "EDUCATION",
                "content": education_content
            })
        
        return sections
    
    def _create_horizontal_bar(self, color="#2C3E50", height=2):
        """Create a horizontal bar for section separation"""
        table = Table([['']], colWidths=[BAR_WIDTH], rowHeights=[height/72*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor(color)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return table
    
    def _calculate_header_footer_dimensions(self):
        """SYSTEMATIC APPROACH: Calculate header and footer dimensions first"""
        personal_info = self.data.get("personal_info", {})
        github_url = personal_info.get("github", "")
        
        # Calculate header bar position based on actual content
        # First page has larger header with name + location, so bar goes under the lowest content
        if github_url:
            # Header bar goes under GitHub link (lowest left content)
            header_bar_y = HEADER_FIRST_GITHUB_Y - SPACE_MULTIPLIER_MINIMAL * inch  # Just under GitHub link
        else:
            # Header bar goes under phone number (lowest left content)
            header_bar_y = HEADER_FIRST_PHONE_Y - SPACE_MULTIPLIER_MINIMAL * inch   # Just under phone number
        
        # But first page also has name + location on right side that goes lower
        # The bar should go under the lowest of either side
        # Right side: name at HEADER_FIRST_NAME_Y, location at HEADER_FIRST_LOCATION_Y
        right_side_bottom = HEADER_FIRST_LOCATION_Y - SPACE_MULTIPLIER_MINIMAL * inch  # Just under location
        
        # Use the lower of the two sides
        header_bar_y = min(header_bar_y, right_side_bottom)
        
        # Calculate footer bar position (fixed at bottom)
        footer_bar_y = FOOTER_BAR_POSITION
        
        # Calculate available space for body content
        # Use same spacing as section headers to their content for consistency
        section_to_subheader_spacing = SPACE_HEADER_TO_CONTENT
        body_start_y = header_bar_y - section_to_subheader_spacing
        body_end_y = footer_bar_y + section_to_subheader_spacing
        
        # Calculate margins based on actual header/footer positions
        top_margin = PAGE_HEIGHT - body_start_y
        bottom_margin = body_end_y
        
        return {
            'header_bar_y': header_bar_y,
            'footer_bar_y': footer_bar_y,
            'body_start_y': body_start_y,
            'body_end_y': body_end_y,
            'top_margin': top_margin,
            'bottom_margin': bottom_margin,
            'section_to_subheader_spacing': section_to_subheader_spacing
        }

    def generate_pdf(self, filename: str) -> str:
        """Generate PDF resume using systematic header/footer approach"""
        # SYSTEMATIC APPROACH: Calculate dimensions first
        dimensions = self._calculate_header_footer_dimensions()
        
        doc = SimpleDocTemplate(filename, pagesize=letter, 
                              rightMargin=MARGIN_RIGHT, leftMargin=MARGIN_LEFT,
                              topMargin=dimensions['top_margin'], 
                              bottomMargin=dimensions['bottom_margin'],
                              # Optimized quality settings for maximum quality within size limits
                              compress=1,  # Light compression for reasonable file size
                              creator="Resume Generator Pro",
                              title=f"Resume - {self.data.get('personal_info', {}).get('name', 'Professional')}",
                              author=self.data.get('personal_info', {}).get('name', 'Professional'),
                              # Additional quality settings
                              subject="Professional Resume",
                              keywords="resume, professional, career")
        story = []
        
        # Define sections in order
        sections = self._get_sections()
        
        # Render each section
        for i, section in enumerate(sections):
            if section["content"]:
                story.append(Paragraph(section["name"], self.styles["SectionHeader"]))
                story.extend(section["content"])
        
        
        
        # Build with custom header and footer using systematic approach
        def add_first_page_header(canvas, doc):
            """Add three-cell header for first page using calculated dimensions"""
            canvas.saveState()
            
            # High quality rendering settings
            canvas.setLineCap(1)  # Round line caps for smoother lines
            canvas.setLineJoin(1)  # Round line joins for smoother lines
            canvas.setLineWidth(1.0)  # Ensure consistent line width
            
            # Use calculated dimensions
            header_bar_y = dimensions['header_bar_y']
            personal_info = self.data.get("personal_info", {})
            
            # Three-cell layout: Email/Phone (left) | Empty (middle) | Name (right)
            name = personal_info.get("name", "NAME")
            email = personal_info.get("email", "")
            phone = personal_info.get("phone", "").replace(".", "").replace("-", "").replace(" ", "")
            
            # Add US country code to phone if it doesn't have one
            if phone and not phone.startswith("+1") and not phone.startswith("1"):
                phone = f"+1 {phone}"
            elif phone and phone.startswith("1") and not phone.startswith("+1"):
                phone = f"+{phone}"
            
            # Left cell: Email and phone stacked vertically
            left_x = HEADER_LEFT_X
            top_y = HEADER_TOP_Y  # Lowered to prevent bleeding off page
            
            if email:
                canvas.setFont("Helvetica", FONT_SIZE_11)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                canvas.drawString(left_x, top_y, email)
            
            if phone:
                canvas.setFont("Helvetica", FONT_SIZE_11)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                canvas.drawString(left_x, top_y - HEADER_PHONE_OFFSET, phone)
            
            # GitHub link under phone on left side with equal spacing
            github_url = personal_info.get("github", "")
            if github_url:
                canvas.setFont("Helvetica", FONT_SIZE_9)
                canvas.setFillColor(HexColor(self.config.get("LINK_COLOR", "#4682B4")))
                github_text = f"GitHub: {github_url.replace('https://', '').replace('http://', '')}"
                # Create clickable link to GitHub with equal spacing
                canvas.linkURL(github_url, 
                             (left_x, top_y - HEADER_GITHUB_LINK_OFFSET, left_x + canvas.stringWidth(github_text, "Helvetica", FONT_SIZE_9), top_y - HEADER_GITHUB_OFFSET))
                canvas.drawString(left_x, top_y - HEADER_GITHUB_OFFSET, github_text)
            
            # Right cell: Full name with Austin, TX underneath
            canvas.setFont("Helvetica-Bold", FONT_SIZE_14)
            canvas.setFillColor(HexColor(self.config.get("NAME_COLOR", "#2C3E50")))
            # Center name vertically with the middle of the left content
            name_y = top_y - HEADER_NAME_OFFSET  # Center between email and phone
            canvas.drawRightString(PAGE_RIGHT_MARGIN, name_y, name)
            
            # Austin, TX with coordinates as clickable link under name
            canvas.setFont("Helvetica", FONT_SIZE_9)
            canvas.setFillColor(HexColor(self.config.get("SUBTITLE_COLOR", "#666666")))
            austin_text = "Austin, TX (30.2672°N, 97.7431°W)"
            austin_width = canvas.stringWidth(austin_text, "Helvetica", FONT_SIZE_9)
            austin_x = PAGE_RIGHT_MARGIN - austin_width
            # Create clickable link to OpenStreetMap
            canvas.linkURL("https://www.openstreetmap.org/?mlat=30.2672&mlon=-97.7431&zoom=12", 
                         (austin_x, name_y - HEADER_LOCATION_LINK_OFFSET, PAGE_RIGHT_MARGIN, name_y - HEADER_LOCATION_OFFSET))
            canvas.drawRightString(PAGE_RIGHT_MARGIN, name_y - HEADER_LOCATION_OFFSET, austin_text)
            
            # Add horizontal bar separator using calculated position
            canvas.setStrokeColor(HexColor(self.config.get("MEDIUM_TEXT_COLOR", "#666666")))
            canvas.setLineWidth(BAR_LINE_WIDTH)
            canvas.line(PAGE_LEFT_MARGIN, header_bar_y, PAGE_RIGHT_MARGIN, header_bar_y)
            
            canvas.restoreState()
            add_footer(canvas, doc)
        
        def add_later_page_header(canvas, doc):
            """Add header for subsequent pages using systematic approach"""
            canvas.saveState()
            
            # High quality rendering settings
            canvas.setLineCap(1)  # Round line caps for smoother lines
            canvas.setLineJoin(1)  # Round line joins for smoother lines
            canvas.setLineWidth(1.0)  # Ensure consistent line width
            
            # Use calculated dimensions (same as first page)
            header_bar_y = dimensions['header_bar_y']
            personal_info = self.data.get("personal_info", {})
            
            # Three-cell layout: Name (left) | Email (middle) | Phone (right)
            name = personal_info.get("name", "NAME").upper()  # Bold and all caps
            email = personal_info.get("email", "").lower()    # Lowercase
            phone = personal_info.get("phone", "").replace(".", "").replace("-", "").replace(" ", "")  # Remove periods, dashes, spaces
            
            # Add US country code to phone if it doesn't have one
            if phone and not phone.startswith("+1") and not phone.startswith("1"):
                phone = f"+1 {phone}"
            elif phone and phone.startswith("1") and not phone.startswith("+1"):
                phone = f"+{phone}"
            
            # Left cell: Name (bold, all caps)
            canvas.setFont("Helvetica-Bold", FONT_SIZE_10)  # Smaller text
            canvas.setFillColor(HexColor(self.config.get("NAME_COLOR", "#2C3E50")))
            canvas.drawString(PAGE_LEFT_MARGIN, HEADER_RECURRING_NAME_Y, name)
            
            # Middle cell: Email (centered)
            if email:
                canvas.setFont("Helvetica", FONT_SIZE_9)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                email_text = f"Email: {email}"
                # Center email in the middle third of the page
                email_width = canvas.stringWidth(email_text, "Helvetica", FONT_SIZE_9)
                email_x = (PAGE_LEFT_MARGIN + PAGE_RIGHT_MARGIN) / 2 - email_width / 2
                canvas.drawString(email_x, HEADER_RECURRING_EMAIL_Y, email_text)
            
            # Right cell: Phone and GitHub stacked
            if phone:
                canvas.setFont("Helvetica", FONT_SIZE_9)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                phone_text = f"Phone: {phone}"
                # Create clickable link for phone
                phone_width = canvas.stringWidth(phone_text, "Helvetica", FONT_SIZE_9)
                phone_x = PAGE_RIGHT_MARGIN - phone_width
                canvas.linkURL(f"tel:{phone}", (phone_x, HEADER_RECURRING_PHONE_Y - 0.1*inch, PAGE_RIGHT_MARGIN, HEADER_RECURRING_PHONE_Y + 0.1*inch))
                canvas.drawRightString(PAGE_RIGHT_MARGIN, HEADER_RECURRING_PHONE_Y, phone_text)
            
            # GitHub link under phone on right side
            github_url = personal_info.get("github", "")
            if github_url:
                canvas.setFont("Helvetica", FONT_SIZE_8)
                canvas.setFillColor(HexColor(self.config.get("LINK_COLOR", "#4682B4")))
                github_text = f"GitHub: {github_url.replace('https://', '').replace('http://', '')}"
                # Create clickable link to GitHub
                canvas.linkURL(github_url, 
                             (PAGE_RIGHT_MARGIN - canvas.stringWidth(github_text, "Helvetica", FONT_SIZE_8), 
                              HEADER_RECURRING_GITHUB_Y - 0.05*inch, PAGE_RIGHT_MARGIN, HEADER_RECURRING_GITHUB_Y + 0.05*inch))
                canvas.drawRightString(PAGE_RIGHT_MARGIN, HEADER_RECURRING_GITHUB_Y, github_text)
            
            # Add horizontal bar using calculated position
            canvas.setStrokeColor(HexColor(self.config.get("MEDIUM_TEXT_COLOR", "#666666")))
            canvas.setLineWidth(BAR_LINE_WIDTH)
            canvas.line(PAGE_LEFT_MARGIN, header_bar_y, PAGE_RIGHT_MARGIN, header_bar_y)
            
            canvas.restoreState()
            add_footer(canvas, doc)  # Also add footer
        
        def add_footer(canvas, doc):
            """Add footer with two-cell structure using calculated dimensions"""
            canvas.saveState()
            
            # High quality rendering settings
            canvas.setLineCap(1)  # Round line caps for smoother lines
            canvas.setLineJoin(1)  # Round line joins for smoother lines
            canvas.setLineWidth(1.0)  # Ensure consistent line width
            
            # Use calculated footer bar position
            footer_bar_y = dimensions['footer_bar_y']
            personal_info = self.data.get("personal_info", {})
            
            # Add bar above footer to separate from page text
            canvas.setStrokeColor(HexColor(self.config.get("MEDIUM_TEXT_COLOR", "#666666")))
            canvas.setLineWidth(BAR_LINE_WIDTH_FOOTER)
            canvas.line(PAGE_LEFT_MARGIN, footer_bar_y, PAGE_RIGHT_MARGIN, footer_bar_y)
            
            canvas.setFont("Helvetica", FONT_SIZE_8)
            footer_y = FOOTER_Y
            
            # Two-cell footer structure
            website_url = personal_info.get("website", "")
            linkedin_url = personal_info.get("linkedin", "")
            
            # Left cell: Site and LinkedIn with pipe separator
            if website_url or linkedin_url:
                current_x = PAGE_LEFT_MARGIN
                
                # Draw labels in accent color, links in different color
                if website_url:
                    # Label in accent color
                    canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                    canvas.drawString(current_x, footer_y, "Site: ")
                    current_x += canvas.stringWidth("Site: ", "Helvetica", FONT_SIZE_8)
                    
                    # Link in different color (use medium text color for contrast)
                    canvas.setFillColor(HexColor(self.config.get("MEDIUM_TEXT_COLOR", "#666666")))
                    canvas.linkURL(website_url, (current_x, footer_y - FOOTER_LINK_OFFSET, current_x + len(website_url)*FOOTER_LINK_OFFSET, footer_y + FOOTER_LINK_OFFSET*2))
                    canvas.drawString(current_x, footer_y, website_url)
                    current_x += canvas.stringWidth(website_url, "Helvetica", FONT_SIZE_8)
                
                if linkedin_url:
                    # Pipe separator
                    if website_url:
                        canvas.setFillColor(HexColor("#666666"))
                        canvas.drawString(current_x, footer_y, " | ")
                        current_x += canvas.stringWidth(" | ", "Helvetica", FONT_SIZE_8)
                    
                    # Label in accent color
                    canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                    canvas.drawString(current_x, footer_y, "LinkedIn: ")
                    current_x += canvas.stringWidth("LinkedIn: ", "Helvetica", FONT_SIZE_8)
                    
                    # Link in different color (use medium text color for contrast)
                    canvas.setFillColor(HexColor(self.config.get("MEDIUM_TEXT_COLOR", "#666666")))
                    canvas.linkURL(linkedin_url, (current_x, footer_y - FOOTER_LINK_OFFSET, current_x + len(linkedin_url)*FOOTER_LINK_OFFSET, footer_y + FOOTER_LINK_OFFSET*2))
                    canvas.drawString(current_x, footer_y, linkedin_url)
            
            # Right cell: Page number
            canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
            page_num = canvas.getPageNumber()
            canvas.drawRightString(PAGE_RIGHT_MARGIN, footer_y, f"Page {page_num}")
            
            canvas.restoreState()
        
        doc.build(story, onFirstPage=add_first_page_header, onLaterPages=add_later_page_header)
        return filename
    
    def generate_docx(self, filename: str) -> str:
        """Generate DOCX resume with high quality settings"""
        doc = Document()
        
        # High quality DOCX settings
        doc.core_properties.title = f"Resume - {self.data.get('personal_info', {}).get('name', 'Professional')}"
        doc.core_properties.author = self.data.get('personal_info', {}).get('name', 'Professional')
        doc.core_properties.creator = "Resume Generator Pro"
        doc.core_properties.subject = "Professional Resume"
        doc.core_properties.keywords = "resume, professional, career"
        doc.core_properties.comments = "Generated by Resume Generator Pro"
        
        # Personal info
        personal_info = self.data.get("personal_info", {})
        
        # Name
        name_para = doc.add_paragraph()
        name_run = name_para.add_run(personal_info.get("name", "NAME"))
        name_run.font.size = Inches(0.2)  # Keep this as it's a reasonable size for DOCX
        name_run.font.bold = True
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Contact info
        contact_parts = []
        if personal_info.get("phone"):
            contact_parts.append(personal_info["phone"])
        if personal_info.get("email"):
            contact_parts.append(personal_info["email"])
        if personal_info.get("website"):
            contact_parts.append(personal_info["website"])
        if personal_info.get("linkedin"):
            contact_parts.append(personal_info["linkedin"])
        if personal_info.get("location"):
            contact_parts.append(personal_info["location"])
        
        if contact_parts:
            contact_para = doc.add_paragraph(" | ".join(contact_parts))
            contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Summary
        summary = self.data.get("summary", "")
        if summary:
            doc.add_heading("PROFESSIONAL SUMMARY", level=2)
            doc.add_paragraph(summary)
        
        # Competencies
        competencies = self.data.get("competencies", {})
        if competencies:
            doc.add_heading("CORE COMPETENCIES", level=2)
            for category, skills in competencies.items():
                if isinstance(skills, list):
                    skill_text = " • ".join(skills)
                    doc.add_paragraph(f"{category}: {skill_text}")
        
        # Experience
        experience = self.data.get("experience", [])
        if experience:
            doc.add_heading("PROFESSIONAL EXPERIENCE", level=2)
            for job in experience:
                job_title = job.get("title", "")
                company = job.get("company", "")
                location = job.get("location", "")
                dates = job.get("dates", "")
                
                title_line = f"{job_title}"
                if company:
                    title_line += f" - {company}"
                if location:
                    title_line += f" ({location})"
                if dates:
                    title_line += f" | {dates}"
                
                doc.add_heading(title_line, level=3)
                
                if job.get("subtitle"):
                    doc.add_paragraph(job["subtitle"])
                
                responsibilities = job.get("responsibilities", [])
                for resp in responsibilities:
                    doc.add_paragraph(f"• {resp}")
        
        # Projects
        projects = self.data.get("projects", [])
        if projects:
            doc.add_heading("KEY PROJECTS", level=2)
            for project in projects:
                project_name = project.get("name", "")
                dates = project.get("dates", "")
                description = project.get("description", "")
                technologies = project.get("technologies", [])
                impact = project.get("impact", "")
                
                title_line = project_name
                if dates:
                    title_line += f" ({dates})"
                
                doc.add_heading(title_line, level=3)
                
                if description:
                    doc.add_paragraph(description)
                
                if technologies:
                    doc.add_paragraph(f"Technologies: {', '.join(technologies)}")
                
                if impact:
                    doc.add_paragraph(f"Impact: {impact}")
        
        # Education
        education = self.data.get("education", [])
        if education:
            doc.add_heading("EDUCATION", level=2)
            for edu in education:
                degree = edu.get("degree", "")
                institution = edu.get("institution", "")
                location = edu.get("location", "")
                dates = edu.get("dates", "")
                gpa = edu.get("gpa", "")
                honors = edu.get("honors", "")
                
                title_line = degree
                if institution:
                    title_line += f" - {institution}"
                if location:
                    title_line += f" ({location})"
                if dates:
                    title_line += f" | {dates}"
                
                doc.add_heading(title_line, level=3)
                
                if gpa:
                    doc.add_paragraph(f"GPA: {gpa}")
                
                if honors:
                    doc.add_paragraph(f"Honors: {honors}")
        
        # Achievements
        achievements = self.data.get("achievements", {})
        if achievements:
            doc.add_heading("KEY ACHIEVEMENTS AND IMPACT", level=2)
            for category, achievement_list in achievements.items():
                if isinstance(achievement_list, list):
                    doc.add_heading(category, level=3)
                    for achievement in achievement_list:
                        doc.add_paragraph(f"• {achievement}")
        
        doc.save(filename)
        return filename
    
    def generate_rtf(self, filename: str) -> str:
        """Generate RTF resume"""
        # RTF is a text format, so we'll create a simple text version
        content = []
        
        # Personal info
        personal_info = self.data.get("personal_info", {})
        content.append(f"\\b {personal_info.get('name', 'NAME')}\\b0")
        content.append("")
        
        # Contact info
        contact_parts = []
        if personal_info.get("phone"):
            contact_parts.append(personal_info["phone"])
        if personal_info.get("email"):
            contact_parts.append(personal_info["email"])
        if personal_info.get("website"):
            contact_parts.append(personal_info["website"])
        if personal_info.get("linkedin"):
            contact_parts.append(personal_info["linkedin"])
        if personal_info.get("location"):
            contact_parts.append(personal_info["location"])
        
        if contact_parts:
            content.append(" | ".join(contact_parts))
        
        content.append("")
        
        # Summary
        summary = self.data.get("summary", "")
        if summary:
            content.append("\\b PROFESSIONAL SUMMARY\\b0")
            content.append(summary)
            content.append("")
        
        # Achievements (moved to top)
        achievements = self.data.get("achievements", {})
        if achievements:
            content.append("\\b KEY ACHIEVEMENTS AND IMPACT\\b0")
            for category, achievement_list in achievements.items():
                if isinstance(achievement_list, list):
                    content.append(f"\\b {category}\\b0")
                    for achievement in achievement_list:
                        content.append(f"• {achievement}")
                    content.append("")
            content.append("")
        
        # Competencies
        competencies = self.data.get("competencies", {})
        if competencies:
            content.append("\\b CORE COMPETENCIES\\b0")
            for category, skills in competencies.items():
                if isinstance(skills, list):
                    skill_text = " • ".join(skills)
                    content.append(f"{category}: {skill_text}")
            content.append("")
        
        # Experience
        experience = self.data.get("experience", [])
        if experience:
            content.append("\\b PROFESSIONAL EXPERIENCE\\b0")
            for job in experience:
                job_title = job.get("title", "")
                company = job.get("company", "")
                location = job.get("location", "")
                dates = job.get("dates", "")
                
                title_line = f"{job_title}"
                if company:
                    title_line += f" - {company}"
                if location:
                    title_line += f" ({location})"
                if dates:
                    title_line += f" | {dates}"
                
                content.append(f"\\b {title_line}\\b0")
                
                if job.get("subtitle"):
                    content.append(job["subtitle"])
                
                responsibilities = job.get("responsibilities", [])
                for resp in responsibilities:
                    content.append(f"• {resp}")
                
                content.append("")
        
        # Projects
        projects = self.data.get("projects", [])
        if projects:
            content.append("\\b KEY PROJECTS\\b0")
            for project in projects:
                project_name = project.get("name", "")
                dates = project.get("dates", "")
                description = project.get("description", "")
                technologies = project.get("technologies", [])
                impact = project.get("impact", "")
                
                title_line = project_name
                if dates:
                    title_line += f" ({dates})"
                
                content.append(f"\\b {title_line}\\b0")
                
                if description:
                    content.append(description)
                
                if technologies:
                    content.append(f"Technologies: {', '.join(technologies)}")
                
                if impact:
                    content.append(f"Impact: {impact}")
                
                content.append("")
        
        # Education
        education = self.data.get("education", [])
        if education:
            content.append("\\b EDUCATION\\b0")
            for edu in education:
                degree = edu.get("degree", "")
                institution = edu.get("institution", "")
                location = edu.get("location", "")
                dates = edu.get("dates", "")
                gpa = edu.get("gpa", "")
                honors = edu.get("honors", "")
                
                title_line = degree
                if institution:
                    title_line += f" - {institution}"
                if location:
                    title_line += f" ({location})"
                if dates:
                    title_line += f" | {dates}"
                
                content.append(f"\\b {title_line}\\b0")
                
                if gpa:
                    content.append(f"GPA: {gpa}")
                
                if honors:
                    content.append(f"Honors: {honors}")
                
                content.append("")
        
        
        # Write RTF file
        rtf_content = "{\\rtf1\\ansi\\deff0\\par " + "\\par ".join(content) + "\\par }"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(rtf_content)
        
        return filename
    
    def generate_markdown(self, filename: str) -> str:
        """Generate Markdown resume"""
        content = []
        
        # Personal info
        personal_info = self.data.get("personal_info", {})
        content.append(f"# {personal_info.get('name', 'NAME')}")
        content.append("")
        
        # Contact information
        contact_parts = []
        if personal_info.get('phone'):
            contact_parts.append(f"**Phone:** {personal_info['phone']}")
        if personal_info.get('email'):
            contact_parts.append(f"**Email:** {personal_info['email']}")
        if personal_info.get('website'):
            contact_parts.append(f"**Website:** {personal_info['website']}")
        if personal_info.get('linkedin'):
            contact_parts.append(f"**LinkedIn:** {personal_info['linkedin']}")
        if personal_info.get('location'):
            contact_parts.append(f"**Location:** {personal_info['location']}")
        
        if contact_parts:
            content.append(" | ".join(contact_parts))
            content.append("")
        
        # Summary
        summary = self.data.get("summary", "")
        if summary:
            content.append("## Professional Summary")
            content.append("")
            content.append(summary)
            content.append("")
        
        # Achievements (moved to top)
        achievements = self.data.get("achievements", {})
        if achievements:
            content.append("## Key Achievements and Impact")
            content.append("")
            for category, achievement_list in achievements.items():
                content.append(f"### {category}")
                if isinstance(achievement_list, list):
                    for achievement in achievement_list:
                        content.append(f"- {achievement}")
                content.append("")
        
        # Competencies (enhanced paragraph format with visual hierarchy)
        competencies = self.data.get("competencies", {})
        if competencies:
            content.append("## Core Competencies")
            content.append("")
            for category, skills in competencies.items():
                if isinstance(skills, list):
                    # Build paragraph format with enhanced Markdown formatting for visual hierarchy
                    skill_parts = []
                    for skill_line in skills:
                        if ": " in skill_line:
                            sub_category, details = skill_line.split(": ", 1)
                            # Enhanced formatting to represent color hierarchy
                            # Main sub-categories: **bold** (like accent color)
                            # Details: *italics* with `code` for technical terms (like muted color)
                            # Extract technical terms and format them as code
                            tech_terms = []
                            for term in details.split(", "):
                                if any(tech in term.lower() for tech in ['python', 'sql', 'aws', 'docker', 'git', 'tableau', 'powerbi', 'spark', 'hadoop', 'mongodb', 'postgresql', 'mysql', 'oracle', 'neo4j', 'arcgis', 'qgis', 'osgeo', 'grass', 'django', 'flask', 'pandas', 'numpy', 'scikit', 'tensorflow', 'r', 'spss', 'sas', 'stata', 'javascript', 'react', 'php', 'html', 'css', 'scala', 'java', 'groovy', 'jupyter', 'netlogo', 'd3.js', 'matplotlib', 'seaborn']):
                                    tech_terms.append(f"`{term.strip()}`")
                                else:
                                    tech_terms.append(term.strip())
                            formatted_details = ", ".join(tech_terms)
                            skill_parts.append(f"**{sub_category}**: *{formatted_details}*")
                        else:
                            # Use **bold** for main skills (like accent color)
                            skill_parts.append(f"**{skill_line}**")
                    
                    # Create single paragraph with main category and all sub-skills
                    # Main category: **bold** (like primary color)
                    full_text = f"**{category}**: " + " • ".join(skill_parts)
                    content.append(full_text)
            content.append("")
        
        # Experience (enhanced formatting with visual hierarchy)
        experience = self.data.get("experience", [])
        if experience:
            content.append("## Professional Experience")
            content.append("")
            for job in experience:
                # Job title: ### header (like primary color)
                content.append(f"### {job.get('title', '')}")
                
                # Company info: **bold** (like accent color)
                company_info = job.get('company', '')
                if job.get('location'):
                    company_info += f" | {job['location']}"
                if job.get('dates'):
                    company_info += f" | {job['dates']}"
                content.append(f"**{company_info}**")
                content.append("")
                
                # Subtitle: *italics* (like muted color)
                if job.get('subtitle'):
                    content.append(f"*{job['subtitle']}*")
                    content.append("")
                
                # Responsibilities with enhanced formatting
                responsibilities = job.get('responsibilities', [])
                if responsibilities:
                    for resp in responsibilities:
                        # Extract and format technical terms in responsibilities
                        enhanced_resp = resp
                        tech_terms = ['Python', 'SQL', 'AWS', 'Docker', 'Git', 'Tableau', 'PowerBI', 'Spark', 'Hadoop', 'MongoDB', 'PostgreSQL', 'MySQL', 'Oracle', 'Neo4j', 'ArcGIS', 'QGIS', 'OSGeo', 'GRASS', 'Django', 'Flask', 'Pandas', 'NumPy', 'SciKit', 'TensorFlow', 'R', 'SPSS', 'SAS', 'Stata', 'JavaScript', 'React', 'PHP', 'HTML', 'CSS', 'Scala', 'Java', 'Groovy', 'Jupyter', 'NetLogo', 'd3.js', 'Matplotlib', 'Seaborn']
                        
                        for term in tech_terms:
                            if term in enhanced_resp:
                                enhanced_resp = enhanced_resp.replace(term, f"`{term}`")
                        
                        content.append(f"- {enhanced_resp}")
                content.append("")
        
        # Projects
        projects = self.data.get("projects", [])
        if projects:
            content.append("## Key Projects")
            content.append("")
            for project in projects:
                content.append(f"### {project.get('name', '')}")
                if project.get('dates'):
                    content.append(f"*{project['dates']}*")
                    content.append("")
                if project.get('description'):
                    content.append(f"{project['description']}")
                    content.append("")
                if project.get('technologies'):
                    content.append(f"**Technologies:** {', '.join(project['technologies'])}")
                if project.get('impact'):
                    content.append(f"**Impact:** {project['impact']}")
                content.append("")
        
        # Education
        education = self.data.get("education", [])
        if education:
            content.append("## Education")
            content.append("")
            for edu in education:
                content.append(f"### {edu.get('degree', '')}")
                institution_info = edu.get('institution', '')
                if edu.get('location'):
                    institution_info += f" | {edu['location']}"
                if edu.get('dates'):
                    institution_info += f" | {edu['dates']}"
                content.append(f"**{institution_info}**")
                if edu.get('gpa'):
                    content.append(f"**GPA:** {edu['gpa']}")
                if edu.get('honors'):
                    content.append(f"**Honors:** {edu['honors']}")
                content.append("")
        
        
        # Footer
        content.append("---")
        content.append("")
        content.append("*Generated using Resume Generator System*")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        
        return filename


class ResumeManager:
    """Manages resume generation with color schemes and formats"""
    
    def __init__(self):
        self.versions = {
            "comprehensive": "dheeraj_chand_comprehensive_full",
            "polling_research_redistricting": "dheeraj_chand_polling_research_redistricting",
            "marketing": "dheeraj_chand_marketing",
            "data_analysis": "dheeraj_chand_data_analysis",
            "visualisation": "dheeraj_chand_visualisation",
            "product": "dheeraj_chand_product"
        }
        
        # Length variants for each version
        self.length_variants = {
            "long": "full",
            "short": "abbreviated"
        }
        
        self.color_schemes = [
            "default_professional",
            "corporate_blue", 
            "modern_tech",
            "modern_clean",
            "satellite_imagery",
            "terrain_mapping",
            "cartographic_professional",
            "topographic_classic"
        ]
        
        self.formats = ["pdf", "docx", "rtf", "md"]
    
    def generate_single_resume(self, version: str, color_scheme: str, format_type: str, output_dir: str = "outputs", length_variant: str = "long") -> bool:
        """Generate a single resume with specified parameters"""
        if version not in self.versions:
            return False
        
        if length_variant not in self.length_variants:
            return False
        
        # Determine input directory based on length variant
        input_basename = self.versions[version]
        if length_variant == "short":
            input_basename += "_abbreviated"
        
        input_dir = Path("inputs") / input_basename
        
        if not input_dir.exists():
            return False
        
        data_file = input_dir / "resume_data.json"
        config_file = input_dir / "config.json"
        
        if not data_file.exists():
            return False
        
        try:
            # Load color scheme
            color_scheme_file = Path("color_schemes") / f"{color_scheme}.json"
            if color_scheme_file.exists():
                generator = ResumeGenerator(str(data_file), str(color_scheme_file), color_scheme)
            else:
                generator = ResumeGenerator(str(data_file), str(config_file) if config_file.exists() else None, color_scheme)
            
            # Create output directory
            output_path = Path(output_dir) / version / length_variant / color_scheme / format_type
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate file
            filename = output_path / f"dheeraj_chand_{version}_{length_variant}_{color_scheme}.{format_type}"
            
            if format_type == "pdf":
                generator.generate_pdf(str(filename))
            elif format_type == "docx":
                generator.generate_docx(str(filename))
            elif format_type == "rtf":
                generator.generate_rtf(str(filename))
            elif format_type == "md":
                generator.generate_markdown(str(filename))
            else:
                return False
            
            return True
            
        except Exception as e:
            print(f"Error generating {version} {color_scheme} {format_type}: {e}")
            return False
    
    def generate_all_combinations(self, output_dir: str = "outputs") -> Dict[str, int]:
        """Generate all combinations of versions, lengths, color schemes, and formats"""
        results = {"success": 0, "failed": 0}
        
        for version in self.versions:
            for length_variant in self.length_variants:
                for color_scheme in self.color_schemes:
                    for format_type in self.formats:
                        if self.generate_single_resume(version, color_scheme, format_type, output_dir, length_variant):
                            results["success"] += 1
                        else:
                            results["failed"] += 1
        
        return results
