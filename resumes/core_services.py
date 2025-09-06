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




class ResumeGenerator:
    """Core resume generator supporting all formats"""
    
    def __init__(self, data_file: str, config_file: Optional[str] = None):
        self.data = self._load_json(data_file)
        self.config = self._load_json(config_file) if config_file else {}
        self.styles = self._create_styles()
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading {file_path}: {e}")
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create paragraph styles based on config"""
        styles = getSampleStyleSheet()
        
        # Get colors from config (color schemes have colors directly, not wrapped in "colors")
        colors = self.config if self.config else {}
        
        custom_styles = {
            "Name": ParagraphStyle(
                "CustomName",
                parent=styles["Heading1"],
                fontSize=28,  # Bigger name
                textColor=HexColor(colors.get("NAME_COLOR", "#2C3E50")),
                alignment=TA_RIGHT,
                spaceAfter=8,
                fontName="Helvetica-Bold",
            ),
            "Title": ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading2"],
                fontSize=12,
                textColor=HexColor(colors.get("TITLE_COLOR", "#34495E")),
                alignment=TA_CENTER,
                spaceAfter=6,
                fontName="Helvetica-Bold",
            ),
            "Subtitle": ParagraphStyle(
                "CustomSubtitle",
                parent=styles["Normal"],
                fontSize=10,
                textColor=HexColor(colors.get("TITLE_COLOR", "#7F8C8D")),
                alignment=TA_CENTER,
                spaceAfter=6,
                fontName="Helvetica",
            ),
            "SectionHeader": ParagraphStyle(
                "CustomSectionHeader",
                parent=styles["Heading2"],
                fontSize=12,
                textColor=HexColor(colors.get("SECTION_HEADER_COLOR", "#2C3E50")),
                spaceAfter=2,
                spaceBefore=6,
                fontName="Helvetica-Bold",
            ),
            "JobTitle": ParagraphStyle(
                "CustomJobTitle",
                parent=styles["Normal"],
                fontSize=10,
                textColor=HexColor(colors.get("JOB_TITLE_COLOR", "#2C3E50")),
                spaceAfter=4,
                spaceBefore=4,
                fontName="Helvetica",
            ),
            "Company": ParagraphStyle(
                "CustomCompany",
                parent=styles["Heading3"],
                fontSize=10,
                textColor=HexColor(colors.get("COMPANY_COLOR", "#2C3E50")),
                spaceAfter=2,
                fontName="Helvetica-Bold",
            ),
            "Body": ParagraphStyle(
                "CustomBody",
                parent=styles["Normal"],
                fontSize=11,
                textColor=HexColor(colors.get("DARK_TEXT_COLOR", "#2C3E50")),
                spaceAfter=3,
                leftIndent=12,
                fontName="Helvetica",
            ),
            "BulletPoint": ParagraphStyle(
                "CustomBulletPoint",
                parent=styles["Normal"],
                fontSize=10,
                textColor=HexColor(colors.get("MEDIUM_TEXT_COLOR", "#666666")),
                spaceAfter=1,
                leftIndent=12,
                fontName="Helvetica",
            ),
            "MainCompetency": ParagraphStyle(
                "CustomMainCompetency",
                parent=styles["Normal"],
                fontSize=11,
                textColor=HexColor(colors.get("COMPETENCY_HEADER_COLOR", "#2C3E50")),
                spaceAfter=1,
                spaceBefore=2,
                fontName="Helvetica-Bold",
            ),
            "SubCompetency": ParagraphStyle(
                "CustomSubCompetency",
                parent=styles["Normal"],
                fontSize=11,
                textColor=HexColor(colors.get("ACCENT_COLOR", "#4682B4")),
                spaceAfter=1,
                leftIndent=12,
                fontName="Helvetica-Bold",
            ),
            "CompetencyDetail": ParagraphStyle(
                "CustomCompetencyDetail",
                parent=styles["Normal"],
                fontSize=10,
                textColor=HexColor(colors.get("DARK_TEXT_COLOR", "#2C3E50")),
                spaceAfter=1,
                leftIndent=0,
                fontName="Helvetica",
            ),
            "Contact": ParagraphStyle(
                "CustomContact",
                parent=styles["Normal"],
                fontSize=11,
                textColor=HexColor(colors.get("ACCENT_COLOR", "#4682B4")),  # Use accent color for header contact
                alignment=TA_RIGHT,
                spaceAfter=12,
                fontName="Helvetica",
            ),
            "ContactStacked": ParagraphStyle(
                "CustomContactStacked",
                parent=styles["Normal"],
                fontSize=11,
                textColor=HexColor(colors.get("ACCENT_COLOR", "#4682B4")),
                alignment=TA_RIGHT,
                spaceAfter=2,
                fontName="Helvetica",
            ),
        }
        
        return custom_styles
    
    def _create_horizontal_bar(self, color="#2C3E50", height=2):
        """Create a horizontal bar for section separation"""
        table = Table([['']], colWidths=[6*inch], rowHeights=[height/72*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor(color)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return table
    
    def generate_pdf(self, filename: str) -> str:
        """Generate PDF resume"""
        # Get website URL for footer
        personal_info = self.data.get("personal_info", {})
        website_url = personal_info.get("website", "")
        
        doc = SimpleDocTemplate(filename, pagesize=letter, 
                              rightMargin=0.6*inch, leftMargin=0.6*inch,
                              topMargin=0.6*inch, bottomMargin=0.8*inch)  # Increased bottom margin for footer
        story = []
        
        # Personal info - Three-cell header layout using canvas
        personal_info = self.data.get("personal_info", {})
        
        # Add space for header (will be drawn by canvas)
        story.append(Spacer(1, 1.2*inch))
        
        # Add extra space for subsequent pages to prevent bar interference
        story.append(Spacer(1, 0.1*inch))
        
        # Add space before first section (reduced for smaller header)
        story.append(Spacer(1, 0.05*inch))
        
        # Summary
        summary = self.data.get("summary", "")
        if summary:
            story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles["SectionHeader"]))
            story.append(Paragraph(summary, self.styles["Body"]))
            story.append(Spacer(1, 6))
        
        # Key Achievements and Impact - moved up from bottom
        achievements = self.data.get("achievements", {})
        if achievements:
            story.append(Paragraph("KEY ACHIEVEMENTS AND IMPACT", self.styles["SectionHeader"]))
            for category, achievement_list in achievements.items():
                if isinstance(achievement_list, list):
                    story.append(Paragraph(category, self.styles["MainCompetency"]))
                    for achievement in achievement_list:
                        story.append(Paragraph(f"• {achievement}", self.styles["BulletPoint"]))
                    story.append(Spacer(1, 0.5))  # Minimal spacing
        
        # Competencies in compact inline format for maximum space efficiency
        competencies = self.data.get("competencies", {})
        if competencies:
            story.append(Paragraph("CORE COMPETENCIES", self.styles["SectionHeader"]))
            
            for main_category, sub_skills in competencies.items():
                if isinstance(sub_skills, list):
                    # Build compact inline content
                    sub_content = []
                    for skill_line in sub_skills:
                        if ": " in skill_line:
                            sub_category, details = skill_line.split(": ", 1)
                            sub_content.append(f"<i>{sub_category}</i> ({details})")
                        else:
                            sub_content.append(skill_line)
                    
                    # Create single paragraph with main category and all sub-skills
                    full_text = f"<b>{main_category}:</b> {'; '.join(sub_content)}"
                    story.append(Paragraph(full_text, self.styles["CompetencyDetail"]))
            
            story.append(Spacer(1, 0.5))
        
        # Experience - Modern format like Deepak's
        experience = self.data.get("experience", [])
        if experience:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles["SectionHeader"]))
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
                
                # Keep the entire job unit together
                job_unit = []
                job_unit.append(Paragraph(company_line, self.styles["Company"]))
                
                if job.get("subtitle"):
                    job_unit.append(Paragraph(job["subtitle"], self.styles["SubCompetency"]))
                
                responsibilities = job.get("responsibilities", [])
                for resp in responsibilities:
                    job_unit.append(Paragraph(f"• {resp}", self.styles["BulletPoint"]))
                
                # Keep the entire job unit together to prevent splitting
                story.append(KeepTogether(job_unit))
                
                story.append(Spacer(1, 1))  # Minimal spacing between jobs
        
        # Projects
        projects = self.data.get("projects", [])
        if projects:
            story.append(Paragraph("KEY PROJECTS", self.styles["SectionHeader"]))
            for project in projects:
                project_name = project.get("name", "")
                dates = project.get("dates", "")
                description = project.get("description", "")
                technologies = project.get("technologies", [])
                impact = project.get("impact", "")
                
                title_line = project_name
                if dates:
                    title_line += f" ({dates})"
                
                story.append(Paragraph(title_line, self.styles["SubCompetency"]))
                
                if description:
                    story.append(Paragraph(description, self.styles["CompetencyDetail"]))
                
                if technologies:
                    tech_text = "Technologies: " + ", ".join(technologies)
                    story.append(Paragraph(tech_text, self.styles["CompetencyDetail"]))
                
                if impact:
                    impact_text = f"Impact: {impact}"
                    story.append(Paragraph(impact_text, self.styles["CompetencyDetail"]))
                
                story.append(Spacer(1, 6))
        
        # Education
        education = self.data.get("education", [])
        if education:
            story.append(Paragraph("EDUCATION", self.styles["SectionHeader"]))
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
                
                story.append(Paragraph(title_line, self.styles["JobTitle"]))
                
                if gpa:
                    story.append(Paragraph(f"GPA: {gpa}", self.styles["Body"]))
                
                if honors:
                    story.append(Paragraph(f"Honors: {honors}", self.styles["Body"]))
                
                story.append(Spacer(1, 6))
        
        
        # Build with custom header and footer
        def add_first_page_header(canvas, doc):
            """Add three-cell header for first page"""
            canvas.saveState()
            
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
            left_x = 0.6*inch
            top_y = 10.5*inch  # Lowered to prevent bleeding off page
            
            if email:
                canvas.setFont("Helvetica", 11)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                canvas.drawString(left_x, top_y, email)
            
            if phone:
                canvas.setFont("Helvetica", 11)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                canvas.drawString(left_x, top_y - 0.15*inch, phone)
            
            # Add Austin coordinates for geospatial flair
            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(HexColor(self.config.get("SUBTITLE_COLOR", "#666666")))
            canvas.drawString(left_x, top_y - 0.35*inch, "Austin, TX (30.2672°N, 97.7431°W)")
            
            # Right cell: Full name (vertically centered with left content)
            canvas.setFont("Helvetica-Bold", 28)
            canvas.setFillColor(HexColor(self.config.get("NAME_COLOR", "#2C3E50")))
            # Center name vertically with the middle of the left content
            name_y = top_y - 0.075*inch  # Center between email and phone
            canvas.drawRightString(7.5*inch, name_y, name)
            
            # Add horizontal bar separator (closer to content)
            canvas.setStrokeColor(HexColor(self.config.get("SECTION_HEADER_COLOR", "#2C3E50")))
            canvas.setLineWidth(1)
            canvas.line(0.6*inch, 10.0*inch, 7.5*inch, 10.0*inch)
            
            canvas.restoreState()
            add_footer(canvas, doc)
        
        def add_later_page_header(canvas, doc):
            """Add header for subsequent pages with three-cell layout"""
            canvas.saveState()
            
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
            canvas.setFont("Helvetica-Bold", 10)  # Smaller text
            canvas.setFillColor(HexColor(self.config.get("NAME_COLOR", "#2C3E50")))
            canvas.drawString(0.6*inch, 10.5*inch, name)
            
            # Middle cell: Email (centered)
            if email:
                canvas.setFont("Helvetica", 9)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                email_text = f"Email: {email}"
                # Center email in the middle third of the page
                email_width = canvas.stringWidth(email_text, "Helvetica", 9)
                email_x = (0.6*inch + 7.5*inch) / 2 - email_width / 2
                canvas.drawString(email_x, 10.5*inch, email_text)
            
            # Right cell: Phone (clickable link)
            if phone:
                canvas.setFont("Helvetica", 9)
                canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                phone_text = f"Phone: {phone}"
                # Create clickable link for phone
                phone_width = canvas.stringWidth(phone_text, "Helvetica", 9)
                phone_x = 7.5*inch - phone_width
                canvas.linkURL(f"tel:{phone}", (phone_x, 10.4*inch, 7.5*inch, 10.6*inch))
                canvas.drawRightString(7.5*inch, 10.5*inch, phone_text)
            
            # Add horizontal bar (higher to avoid text interference)
            canvas.setStrokeColor(HexColor(self.config.get("SECTION_HEADER_COLOR", "#2C3E50")))
            canvas.setLineWidth(1)
            canvas.line(0.6*inch, 10.4*inch, 7.5*inch, 10.4*inch)  # Higher position to avoid text
            
            canvas.restoreState()
            add_footer(canvas, doc)  # Also add footer
        
        def add_footer(canvas, doc):
            """Add footer with two-cell structure and pipe separator"""
            canvas.saveState()
            
            # Add bar above footer to separate from page text
            canvas.setStrokeColor(HexColor(self.config.get("SECTION_HEADER_COLOR", "#2C3E50")))
            canvas.setLineWidth(0.5)
            canvas.line(0.6*inch, 0.6*inch, 7.5*inch, 0.6*inch)
            
            canvas.setFont("Helvetica", 8)
            footer_y = 0.4*inch
            
            # Two-cell footer structure
            website_url = personal_info.get("website", "")
            linkedin_url = personal_info.get("linkedin", "")
            
            # Left cell: Site and LinkedIn with pipe separator
            if website_url or linkedin_url:
                current_x = 0.6*inch
                
                # Draw labels in accent color, links in regular color
                if website_url:
                    # Label in accent color
                    canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                    canvas.drawString(current_x, footer_y, "Site: ")
                    current_x += canvas.stringWidth("Site: ", "Helvetica", 8)
                    
                    # Link in regular color
                    canvas.setFillColor(HexColor("#4682B4"))
                    canvas.linkURL(website_url, (current_x, footer_y - 0.05*inch, current_x + len(website_url)*0.05*inch, footer_y + 0.1*inch))
                    canvas.drawString(current_x, footer_y, website_url)
                    current_x += canvas.stringWidth(website_url, "Helvetica", 8)
                
                if linkedin_url:
                    # Pipe separator
                    if website_url:
                        canvas.setFillColor(HexColor("#666666"))
                        canvas.drawString(current_x, footer_y, " | ")
                        current_x += canvas.stringWidth(" | ", "Helvetica", 8)
                    
                    # Label in accent color
                    canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
                    canvas.drawString(current_x, footer_y, "LinkedIn: ")
                    current_x += canvas.stringWidth("LinkedIn: ", "Helvetica", 8)
                    
                    # Link in LinkedIn blue
                    canvas.setFillColor(HexColor("#0077B5"))
                    canvas.linkURL(linkedin_url, (current_x, footer_y - 0.05*inch, current_x + len(linkedin_url)*0.05*inch, footer_y + 0.1*inch))
                    canvas.drawString(current_x, footer_y, linkedin_url)
            
            # Right cell: Page number
            canvas.setFillColor(HexColor(self.config.get("ACCENT_COLOR", "#4682B4")))
            page_num = canvas.getPageNumber()
            canvas.drawRightString(7.5*inch, footer_y, f"Page {page_num}")
            
            canvas.restoreState()
        
        doc.build(story, onFirstPage=add_first_page_header, onLaterPages=add_later_page_header)
        return filename
    
    def generate_docx(self, filename: str) -> str:
        """Generate DOCX resume"""
        doc = Document()
        
        # Personal info
        personal_info = self.data.get("personal_info", {})
        
        # Name
        name_para = doc.add_paragraph()
        name_run = name_para.add_run(personal_info.get("name", "NAME"))
        name_run.font.size = Inches(0.2)
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
        
        # Achievements
        achievements = self.data.get("achievements", {})
        if achievements:
            content.append("\\b KEY ACHIEVEMENTS AND IMPACT\\b0")
            for category, achievement_list in achievements.items():
                if isinstance(achievement_list, list):
                    content.append(f"\\b {category}\\b0")
                    for achievement in achievement_list:
                        content.append(f"• {achievement}")
                    content.append("")
        
        # Write RTF file
        rtf_content = "{\\rtf1\\ansi\\deff0 " + "\\par ".join(content) + "}"
        
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
        
        # Competencies
        competencies = self.data.get("competencies", {})
        if competencies:
            content.append("## Core Competencies")
            content.append("")
            for category, skills in competencies.items():
                content.append(f"### {category}")
                if isinstance(skills, list):
                    for skill in skills:
                        content.append(f"- {skill}")
                content.append("")
        
        # Experience
        experience = self.data.get("experience", [])
        if experience:
            content.append("## Professional Experience")
            content.append("")
            for job in experience:
                content.append(f"### {job.get('title', '')}")
                company_info = job.get('company', '')
                if job.get('location'):
                    company_info += f" | {job['location']}"
                if job.get('dates'):
                    company_info += f" | {job['dates']}"
                content.append(f"**{company_info}**")
                content.append("")
                
                if job.get('subtitle'):
                    content.append(f"*{job['subtitle']}*")
                    content.append("")
                
                responsibilities = job.get('responsibilities', [])
                if responsibilities:
                    for resp in responsibilities:
                        content.append(f"- {resp}")
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
        
        # Achievements
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
            "research": "dheeraj_chand_research_focused",
            "technical": "dheeraj_chand_technical_detailed", 
            "comprehensive": "dheeraj_chand_comprehensive_full",
            "consulting": "dheeraj_chand_consulting_minimal",
            "software": "dheeraj_chand_software_engineer",
            "marketing": "dheeraj_chand_product_marketing"
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
    
    def generate_single_resume(self, version: str, color_scheme: str, format_type: str, output_dir: str = "outputs") -> bool:
        """Generate a single resume with specified parameters"""
        if version not in self.versions:
            return False
        
        input_basename = self.versions[version]
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
                generator = ResumeGenerator(str(data_file), str(color_scheme_file))
            else:
                generator = ResumeGenerator(str(data_file), str(config_file) if config_file.exists() else None)
            
            # Create output directory
            output_path = Path(output_dir) / version / color_scheme / format_type
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate file
            filename = output_path / f"dheeraj_chand_{version}_{color_scheme}.{format_type}"
            
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
        """Generate all combinations of versions, color schemes, and formats"""
        results = {"success": 0, "failed": 0}
        
        for version in self.versions:
            for color_scheme in self.color_schemes:
                for format_type in self.formats:
                    if self.generate_single_resume(version, color_scheme, format_type, output_dir):
                        results["success"] += 1
                    else:
                        results["failed"] += 1
        
        return results
