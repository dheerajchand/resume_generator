#!/usr/bin/env python3
"""
Professional Resume Generator using ReportLab
Generates a 2-page PDF resume with precise formatting control
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import json
from pathlib import Path
from datetime import datetime

class ResumeConfig:
    """Configuration class for easy customization"""

    # Colors (matching your website theme)
    PRIMARY_GREEN = HexColor('#228B22')      # Forest Green for name and accents
    SECONDARY_GOLD = HexColor('#B8860B')     # Dark Goldenrod for headers
    LIGHT_GOLD = HexColor('#DAA520')         # Goldenrod for highlights
    DARK_GRAY = HexColor('#333333')          # Main text
    MEDIUM_GRAY = HexColor('#666666')        # Secondary text
    LIGHT_GRAY = HexColor('#999999')         # Tertiary text

    # Fonts
    FONT_MAIN = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_ITALIC = 'Helvetica-Oblique'

    # Font Sizes
    NAME_SIZE = 24
    TITLE_SIZE = 14
    SECTION_HEADER_SIZE = 12
    JOB_TITLE_SIZE = 11
    BODY_SIZE = 9
    CONTACT_SIZE = 9

    # Spacing (tightened for better page usage)
    PAGE_MARGIN = 0.6 * inch
    SECTION_SPACING = 0.12 * inch
    PARAGRAPH_SPACING = 0.06 * inch
    LINE_SPACING = 1.15
    JOB_SPACING = 6  # Space between jobs
    CATEGORY_SPACING = 4  # Space between competency categories

    # Layout
    MAX_PAGES = 2
    BULLET_CHAR = '▸'

class ResumeData:
    """Resume content data structure - now loads from JSON"""

    def __init__(self, data_file=None):
        if data_file and Path(data_file).exists():
            self.load_from_json(data_file)
        else:
            self._create_default_data()

    def load_from_json(self, data_file):
        """Load resume data from JSON file"""
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.personal_info = data.get('personal_info', {})
        self.summary = data.get('summary', '')
        self.competencies = data.get('competencies', {})
        self.experience = data.get('experience', [])
        self.achievements = data.get('achievements', {})

    def save_to_json(self, data_file):
        """Save resume data to JSON file"""
        data = {
            'personal_info': self.personal_info,
            'summary': self.summary,
            'competencies': self.competencies,
            'experience': self.experience,
            'achievements': self.achievements,
            '_metadata': {
                'created': datetime.now().isoformat(),
                'version': '1.0',
                'description': 'Resume data for Professional Resume Generator'
            }
        }

        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _create_default_data(self):
        """Create default resume data"""
        self.personal_info = {
            'name': 'DHEERAJ CHAND',
            'title': 'Director of Research and Analysis',
            'phone': '(202) 550-7110',
            'email': 'Dheeraj.Chand@gmail.com',
            'website': 'https://www.dheerajchand.com',
            'linkedin': 'https://www.linkedin.com/in/dheerajchand/'
        }

        self.summary = """Research and Data Analytics Leader with 20+ years of experience directing applied research projects from conception to completion focused on economic mobility, community development, and social impact. Proven track record of leading cross-functional teams, translating complex research insights for diverse stakeholders including elected officials and community organizations, and implementing evidence-based solutions that drive meaningful outcomes. Expert in research methodology design, statistical analysis, and community partnership development with extensive experience serving vulnerable populations and addressing systemic poverty challenges."""

        self.competencies = {
            'Applied Research Leadership': [
                'Applied Research Project Management (Conception to Completion)',
                'Research Methodology Design and Implementation',
                'Economic Mobility and Community Development Research',
                'Statistical Analysis and Data Validation',
                'Cross-functional Team Leadership and Mentoring',
                'Stakeholder Communication and Translation of Complex Findings',
                'Evidence-Based Framework Development'
            ],
            'Technical Proficiency': [
                'Programming: Python (Pandas, SciKit, TensorFlow, Django), R, SQL, Scala, JavaScript',
                'Data Platforms: PostgreSQL, MySQL, Snowflake, Spark, MongoDB, Oracle',
                'Analysis Tools: Excel (Advanced), Tableau, PowerBI, SPSS, SAS',
                'Research Tools: Survey Design, Sampling Methodology, Statistical Modeling',
                'Visualization: d3.js, Seaborn, MatplotLib, Tableau, PowerBI'
            ],
            'Community Impact and Strategic Operations': [
                'Community Partnership Development',
                'Government Relations and Policy Analysis',
                'Public Systems Integration',
                'Multi-million Dollar Project Management',
                'Performance Measurement and Evaluation',
                'Poverty Alleviation Program Assessment',
                'Data-Driven Decision Making for Social Impact'
            ]
        }

        self.experience = [
            {
                'title': 'PARTNER',
                'company': 'Siege Analytics, Austin, TX',
                'dates': '2005 – Present',
                'subtitle': 'Leading Applied Research Projects with Community Development and Social Impact Focus',
                'responsibilities': [
                    'Direct and execute comprehensive applied research projects from conception to completion for organizations focused on economic mobility, community development, and social outcomes',
                    'Lead multi-million dollar research initiatives involving sensitive demographic and economic data addressing poverty, housing, and community health challenges',
                    'Translate complex research findings for diverse stakeholder groups including elected officials, NGO leadership, community organizations, and frontline service providers',
                    'Collaborate with government agencies, community partners, and research institutions to develop evidence-based solutions addressing systemic poverty and economic mobility barriers',
                    'Manage client relationships across public sector, nonprofit, and community organizations, consistently delivering research that drives strategic decision-making for vulnerable populations',
                    'Develop and deploy custom analytical tools processing billions of records to identify patterns in economic mobility, demographic trends, and service delivery outcomes'
                ]
            },
            {
                'title': 'DATA PRODUCTS MANAGER',
                'company': 'Helm/Murmuration, Austin, TX',
                'dates': '2021 – 2023',
                'subtitle': 'Research Team Leadership and Community-Focused Methodology Innovation',
                'responsibilities': [
                    'Led cross-functional team of eleven data engineers and analysts focused on community organizing and social justice research, establishing best practices for applied research methodology',
                    'Managed national research team of five analysts specializing in community engagement and demographic analysis for social impact organizations',
                    'Overhauled organization research methodology and data collection operations for community-focused studies, significantly improving accuracy and response rates',
                    'Designed and implemented comprehensive data warehouse integrating demographic, economic, and behavioral data to support evidence-based decision making for community organizations',
                    'Developed advanced analytical pipelines for research applications that enhanced community segmentation and outcome prediction capabilities for social impact programs',
                    'Trained staff in data visualization and communication techniques to improve research deliverable quality for diverse audiences including community leaders and government officials'
                ]
            },
            {
                'title': 'ANALYTICS SUPERVISOR',
                'company': 'GSD&M, Austin, TX',
                'dates': '2018 – 2019',
                'subtitle': 'Research Operations and Team Development',
                'responsibilities': [
                    'Restructured research department to scale capabilities from small-scale analysis to comprehensive applied research operations',
                    'Managed three analysts, mentoring them in advanced research techniques, methodology design, and stakeholder communication',
                    'Implemented spatial analysis and segmentation methodologies that revealed new insights about community needs and service delivery',
                    'Introduced version control and Agile project management methodologies, improving research project delivery timelines by 40%',
                    'Developed standardized research reporting frameworks to ensure consistent, high-quality deliverables for diverse stakeholder groups'
                ]
            },
            {
                'title': 'SOFTWARE ENGINEER',
                'company': 'Mautinoa Technologies, Austin, TX',
                'dates': '2016 – 2018',
                'subtitle': 'Applied Research in Humanitarian and Crisis Context',
                'responsibilities': [
                    'Conceived, architected, and engineered econometric simulation software for measuring humanitarian crisis intervention effectiveness and resource allocation optimization',
                    'Collaborated with data and engineering directors at multinational NGOs (UNICEF, IFRC) to develop evidence-based intervention frameworks for vulnerable populations',
                    'Conducted geospatial analysis on vulnerable populations to assess intervention impact and optimize resource allocation for maximum community benefit',
                    'Designed research methodologies for measuring complex social outcomes in crisis environments, focusing on economic mobility and community resilience'
                ]
            },
            {
                'title': 'RESEARCH DIRECTOR',
                'company': 'PCCC, Austin, TX',
                'dates': '2011 – 2012',
                'subtitle': 'Large-Scale Applied Research Initiative Leadership',
                'responsibilities': [
                    'Led all aspects of applied research design, implementation, analysis, and reporting for major national studies focused on social and economic outcomes',
                    'Engineered innovative data collection system facilitating thousands of simultaneous surveys, significantly increasing research scale and efficiency',
                    'Developed new statistical methods for geographic boundary estimation, enhancing community-level analysis capabilities',
                    'Created comprehensive data visualization solutions that improved stakeholder understanding of complex research findings related to economic mobility',
                    'Managed research projects addressing policy questions related to economic mobility and community development'
                ]
            }
        ]

        self.achievements = {
            'Research Leadership and Community Impact': [
                'Regular expert testimony and consultation on research methodology for journalists, elected officials, and community leaders on economic mobility and poverty alleviation',
                'Research analysis used in court cases addressing housing, redistricting, and community development, demonstrating rigorous methodology and credible findings',
                'Conceived and deployed cloud-based analytical software used by thousands of researchers and analysts nationwide for community-focused research'
            ],
            'Systems and Infrastructure Development': [
                'Designed and implemented multi-tenant data warehouse tracking decades of demographic, economic, and policy changes affecting vulnerable populations',
                'Developed comprehensive research frameworks for measuring complex social outcomes and community intervention effectiveness',
                'Created scalable research methodologies supporting evidence-based decision making for multi-billion dollar public systems focused on poverty alleviation'
            ],
            'Community and Stakeholder Engagement': [
                'Extensive experience briefing elected officials, NGO leadership, and senior staff on research findings and policy implications for economic mobility',
                'Proven track record translating complex research for diverse audiences including community organizations, government agencies, and frontline service providers',
                'Successfully managed research partnerships across public sector, nonprofit, and community-based organizations focused on addressing systemic poverty'
            ]
        }

class ResumeGenerator:
    """Main resume generator class"""

    def __init__(self, config=None, data=None, input_dir=None, output_dir=None, basename="resume"):
        self.config = config or ResumeConfig()
        self.data = data or ResumeData()
        self.basename = basename
        self.input_dir = Path(input_dir) if input_dir else Path('inputs') / basename
        self.output_dir = Path(output_dir) if output_dir else Path('outputs') / basename
        self.styles = self._create_styles()
        self.story = []

        # Create directories if they don't exist
        self._setup_directories()

    def _setup_directories(self):
        """Create input and output directory structure"""
        print(f"🔧 DEBUG: Setting up directories...")
        print(f"   DEBUG: Input dir path: {self.input_dir}")
        print(f"   DEBUG: Output dir path: {self.output_dir}")

        # Create main directories with basename subdirectories
        print(f"   DEBUG: Creating input directory...")
        self.input_dir.mkdir(parents=True, exist_ok=True)
        print(f"   DEBUG: ✅ Input directory created/exists: {self.input_dir.exists()}")

        print(f"   DEBUG: Creating output directory...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"   DEBUG: ✅ Output directory created/exists: {self.output_dir.exists()}")

        # Create output subdirectories for each format
        pdf_dir = self.output_dir / 'pdf'
        docx_dir = self.output_dir / 'docx'
        rtf_dir = self.output_dir / 'rtf'

        print(f"   DEBUG: Creating format subdirectories...")
        pdf_dir.mkdir(exist_ok=True)
        print(f"   DEBUG: ✅ PDF dir: {pdf_dir} (exists: {pdf_dir.exists()})")

        docx_dir.mkdir(exist_ok=True)
        print(f"   DEBUG: ✅ DOCX dir: {docx_dir} (exists: {docx_dir.exists()})")

        rtf_dir.mkdir(exist_ok=True)
        print(f"   DEBUG: ✅ RTF dir: {rtf_dir} (exists: {rtf_dir.exists()})")

        print(f"📁 Directory structure:")
        print(f"   Input:  {self.input_dir.absolute()}")
        print(f"   Output: {self.output_dir.absolute()}")
        print(f"   Subdirs: pdf/, docx/, rtf/")

    def _get_output_path(self, format_type, basename):
        """Get the appropriate output path for a given format"""
        format_dir = self.output_dir / format_type
        output_path = format_dir / f"{basename}.{format_type}"
        print(f"🔧 DEBUG: Output path for {format_type}: {output_path}")
        return output_path

    def _create_styles(self):
        """Create custom paragraph styles"""
        styles = getSampleStyleSheet()

        # Name style
        styles.add(ParagraphStyle(
            name='NameStyle',
            parent=styles['Heading1'],
            fontSize=self.config.NAME_SIZE,
            textColor=self.config.PRIMARY_GREEN,
            fontName=self.config.FONT_BOLD,
            alignment=TA_CENTER,
            spaceAfter=4,
            spaceBefore=0
        ))

        # Title style
        styles.add(ParagraphStyle(
            name='TitleStyle',
            parent=styles['Normal'],
            fontSize=self.config.TITLE_SIZE,
            textColor=self.config.SECONDARY_GOLD,
            fontName=self.config.FONT_BOLD,
            alignment=TA_CENTER,
            spaceAfter=8,
            spaceBefore=0
        ))

        # Contact style
        styles.add(ParagraphStyle(
            name='ContactStyle',
            parent=styles['Normal'],
            fontSize=self.config.CONTACT_SIZE,
            textColor=self.config.MEDIUM_GRAY,
            fontName=self.config.FONT_MAIN,
            alignment=TA_CENTER,
            spaceAfter=12,
            spaceBefore=0
        ))

        # Section header style
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=self.config.SECTION_HEADER_SIZE,
            textColor=self.config.SECONDARY_GOLD,
            fontName=self.config.FONT_BOLD,
            alignment=TA_LEFT,
            spaceAfter=6,
            spaceBefore=8
        ))

        # Job title style
        styles.add(ParagraphStyle(
            name='JobTitle',
            parent=styles['Normal'],
            fontSize=self.config.JOB_TITLE_SIZE,
            textColor=self.config.SECONDARY_GOLD,
            fontName=self.config.FONT_BOLD,
            spaceAfter=2,
            spaceBefore=4
        ))

        # Company info style
        styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=styles['Normal'],
            fontSize=self.config.BODY_SIZE,
            textColor=self.config.MEDIUM_GRAY,
            fontName=self.config.FONT_MAIN,
            spaceAfter=2
        ))

        # Subtitle style
        styles.add(ParagraphStyle(
            name='SubtitleStyle',
            parent=styles['Normal'],
            fontSize=self.config.BODY_SIZE,
            textColor=self.config.PRIMARY_GREEN,
            fontName=self.config.FONT_ITALIC,
            spaceAfter=4
        ))

        # Body text style
        styles.add(ParagraphStyle(
            name='ResumeBodyText',
            parent=styles['Normal'],
            fontSize=self.config.BODY_SIZE,
            textColor=self.config.DARK_GRAY,
            fontName=self.config.FONT_MAIN,
            alignment=TA_JUSTIFY,
            spaceAfter=2,
            leading=self.config.BODY_SIZE * self.config.LINE_SPACING
        ))

        # Bullet style
        styles.add(ParagraphStyle(
            name='ResumeBulletStyle',
            parent=styles['Normal'],
            fontSize=self.config.BODY_SIZE,
            textColor=self.config.DARK_GRAY,
            fontName=self.config.FONT_MAIN,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=1.5,
            leading=self.config.BODY_SIZE * self.config.LINE_SPACING
        ))

        # Competency header style
        styles.add(ParagraphStyle(
            name='CompetencyHeader',
            parent=styles['Normal'],
            fontSize=self.config.BODY_SIZE + 1,
            textColor=self.config.PRIMARY_GREEN,
            fontName=self.config.FONT_BOLD,
            spaceAfter=3,
            spaceBefore=4
        ))

        return styles

    def _add_header(self):
        """Add the header section with name, title, and contact info"""
        # Name
        name_para = Paragraph(self.data.personal_info['name'], self.styles['NameStyle'])
        self.story.append(name_para)

        # Title
        title_para = Paragraph(self.data.personal_info['title'], self.styles['TitleStyle'])
        self.story.append(title_para)

        # Contact info
        contact_text = f"""
        <b>{self.data.personal_info['phone']} | {self.data.personal_info['email']}</b><br/>
        <a href="{self.data.personal_info['website']}" color="{self.config.SECONDARY_GOLD}">{self.data.personal_info['website']}</a> |
        <a href="{self.data.personal_info['linkedin']}" color="{self.config.SECONDARY_GOLD}">{self.data.personal_info['linkedin']}</a>
        """
        contact_para = Paragraph(contact_text, self.styles['ContactStyle'])
        self.story.append(contact_para)

        # Header separator line
        self.story.append(Spacer(1, 4))

    def _add_section_header(self, title):
        """Add a section header with underline"""
        header_text = f'<u>{title.upper()}</u>'
        header_para = Paragraph(header_text, self.styles['SectionHeader'])
        self.story.append(header_para)

    def _add_summary(self):
        """Add professional summary section"""
        self._add_section_header('Professional Summary')
        summary_para = Paragraph(self.data.summary, self.styles['ResumeBodyText'])
        self.story.append(summary_para)
        self.story.append(Spacer(1, self.config.SECTION_SPACING))

    def _add_competencies(self):
        """Add core competencies section"""
        self._add_section_header('Core Competencies')

        for category, skills in self.data.competencies.items():
            # Category header
            cat_para = Paragraph(category, self.styles['CompetencyHeader'])
            self.story.append(cat_para)

            # Skills list
            if category == 'Technical Proficiency':
                # Technical skills with better formatting
                for skill in skills:
                    skill_para = Paragraph(skill, self.styles['ResumeBodyText'])
                    self.story.append(skill_para)
            else:
                # Other competencies as a flowing paragraph
                skills_text = ' • '.join(skills)
                skills_para = Paragraph(skills_text, self.styles['ResumeBodyText'])
                self.story.append(skills_para)

            self.story.append(Spacer(1, self.config.CATEGORY_SPACING))

        self.story.append(Spacer(1, self.config.SECTION_SPACING))

    def _add_experience(self):
        """Add professional experience section"""
        self._add_section_header('Professional Experience')

        for i, job in enumerate(self.data.experience):
            job_content = []

            # Job title
            title_para = Paragraph(job['title'], self.styles['JobTitle'])
            job_content.append(title_para)

            # Company and dates
            company_para = Paragraph(f"{job['company']} | {job['dates']}", self.styles['CompanyInfo'])
            job_content.append(company_para)

            # Subtitle
            subtitle_para = Paragraph(job['subtitle'], self.styles['SubtitleStyle'])
            job_content.append(subtitle_para)

            # Responsibilities
            for responsibility in job['responsibilities']:
                bullet_text = f"{self.config.BULLET_CHAR} {responsibility}"
                bullet_para = Paragraph(bullet_text, self.styles['ResumeBulletStyle'])
                job_content.append(bullet_para)

            # Keep job together on same page if possible
            job_group = KeepTogether(job_content)
            self.story.append(job_group)

            # Add spacing between jobs, but less after the last one
            if i < len(self.data.experience) - 1:
                self.story.append(Spacer(1, self.config.JOB_SPACING))

        # Add LinkedIn reference
        linkedin_text = f'<i>Additional experience and project details available on <a href="{self.data.personal_info["linkedin"]}" color="{self.config.SECONDARY_GOLD}">LinkedIn</a></i>'
        linkedin_para = Paragraph(linkedin_text, self.styles['ResumeBodyText'])
        self.story.append(Spacer(1, 4))
        self.story.append(linkedin_para)
        self.story.append(Spacer(1, self.config.SECTION_SPACING))

    def _add_achievements(self):
        """Add key achievements section"""
        self._add_section_header('Key Achievements and Impact')

        for category, achievements in self.data.achievements.items():
            # Category header
            cat_para = Paragraph(category, self.styles['CompetencyHeader'])
            self.story.append(cat_para)

            # Achievements list
            for achievement in achievements:
                bullet_text = f"✓ {achievement}"
                bullet_para = Paragraph(bullet_text, self.styles['ResumeBulletStyle'])
                self.story.append(bullet_para)

            self.story.append(Spacer(1, 4))

    def generate_pdf(self, basename='resume'):
        """Generate the complete PDF resume"""
        output_path = self._get_output_path('pdf', basename)

        # Create document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=self.config.PAGE_MARGIN,
            leftMargin=self.config.PAGE_MARGIN,
            topMargin=self.config.PAGE_MARGIN,
            bottomMargin=self.config.PAGE_MARGIN
        )

        # Build content
        self._add_header()
        self._add_summary()
        self._add_competencies()
        self._add_experience()
        self._add_achievements()

        # Generate PDF
        doc.build(self.story)
        print(f"📄 PDF generated: {output_path}")

        return str(output_path)

    def generate_docx(self, basename='resume'):
        """Generate Word document version"""
        try:
            from docx import Document
            from docx.shared import Inches, RGBColor
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            from docx.enum.style import WD_STYLE_TYPE
        except ImportError:
            print("⚠️  python-docx not installed. Install with: pip install python-docx")
            return None

        output_path = self._get_output_path('docx', basename)
        doc = Document()

        # Set margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.6)
            section.bottom_margin = Inches(0.6)
            section.left_margin = Inches(0.6)
            section.right_margin = Inches(0.6)

        # Header
        name_para = doc.add_paragraph()
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        name_run = name_para.add_run(self.data.personal_info['name'])
        name_run.font.size = Inches(0.3)  # Approximate 24pt
        name_run.font.bold = True
        name_run.font.color.rgb = RGBColor(34, 139, 34)  # Green

        title_para = doc.add_paragraph()
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_run = title_para.add_run(self.data.personal_info['title'])
        title_run.font.size = Inches(0.17)  # Approximate 14pt
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(184, 134, 11)  # Gold

        contact_para = doc.add_paragraph()
        contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_text = f"{self.data.personal_info['phone']} | {self.data.personal_info['email']}\n{self.data.personal_info['website']} | {self.data.personal_info['linkedin']}"
        contact_para.add_run(contact_text)

        # Summary
        self._add_docx_section(doc, 'PROFESSIONAL SUMMARY', self.data.summary)

        # Competencies
        comp_heading = doc.add_heading('CORE COMPETENCIES', level=2)
        comp_heading.runs[0].font.color.rgb = RGBColor(184, 134, 11)

        for category, skills in self.data.competencies.items():
            cat_para = doc.add_paragraph()
            cat_run = cat_para.add_run(category)
            cat_run.font.bold = True
            cat_run.font.color.rgb = RGBColor(34, 139, 34)

            if category == 'Technical Proficiency':
                for skill in skills:
                    doc.add_paragraph(skill, style='List Bullet')
            else:
                skills_text = ' • '.join(skills)
                doc.add_paragraph(skills_text)

        # Experience
        exp_heading = doc.add_heading('PROFESSIONAL EXPERIENCE', level=2)
        exp_heading.runs[0].font.color.rgb = RGBColor(184, 134, 11)

        for job in self.data.experience:
            job_para = doc.add_paragraph()
            job_run = job_para.add_run(job['title'])
            job_run.font.bold = True
            job_run.font.color.rgb = RGBColor(184, 134, 11)

            company_para = doc.add_paragraph(f"{job['company']} | {job['dates']}")
            subtitle_para = doc.add_paragraph()
            subtitle_run = subtitle_para.add_run(job['subtitle'])
            subtitle_run.font.italic = True
            subtitle_run.font.color.rgb = RGBColor(34, 139, 34)

            for responsibility in job['responsibilities']:
                doc.add_paragraph(f"▸ {responsibility}", style='List Bullet')

        # LinkedIn reference
        linkedin_para = doc.add_paragraph()
        linkedin_run = linkedin_para.add_run('Additional experience and project details available on LinkedIn')
        linkedin_run.font.italic = True

        # Achievements
        ach_heading = doc.add_heading('KEY ACHIEVEMENTS AND IMPACT', level=2)
        ach_heading.runs[0].font.color.rgb = RGBColor(184, 134, 11)

        for category, achievements in self.data.achievements.items():
            cat_para = doc.add_paragraph()
            cat_run = cat_para.add_run(category)
            cat_run.font.bold = True
            cat_run.font.color.rgb = RGBColor(34, 139, 34)

            for achievement in achievements:
                doc.add_paragraph(f"✓ {achievement}", style='List Bullet')

        doc.save(str(output_path))
        print(f"📝 DOCX generated: {output_path}")
        return str(output_path)

    def _add_docx_section(self, doc, title, content):
        """Helper to add a section to Word doc"""
        from docx.shared import RGBColor
        heading = doc.add_heading(title, level=2)
        heading.runs[0].font.color.rgb = RGBColor(184, 134, 11)  # Gold
        doc.add_paragraph(content)

    def generate_rtf(self, basename='resume'):
        """Generate RTF document (can be opened by Pages)"""
        output_path = self._get_output_path('rtf', basename)

        rtf_content = r"""{\rtf1\ansi\deff0
{\fonttbl{\f0 Times New Roman;}}
{\colortbl;\red0\green0\blue0;\red34\green139\blue34;\red184\green134\blue11;}
\f0\fs24
{\qc\cf2\b\fs36 """ + self.data.personal_info['name'] + r"""\par}
{\qc\cf3\b\fs20 """ + self.data.personal_info['title'] + r"""\par}
{\qc """ + f"{self.data.personal_info['phone']} | {self.data.personal_info['email']}" + r"""\par}
{\qc """ + f"{self.data.personal_info['website']} | {self.data.personal_info['linkedin']}" + r"""\par}
\par
{\cf3\b\ul PROFESSIONAL SUMMARY\par}
""" + self.data.summary + r"""\par
\par
{\cf3\b\ul CORE COMPETENCIES\par}
"""

        for category, skills in self.data.competencies.items():
            rtf_content += r"{\cf2\b " + category + r"\par}"
            if category == 'Technical Proficiency':
                for skill in skills:
                    rtf_content += skill + r"\par"
            else:
                rtf_content += ' • '.join(skills) + r"\par"
            rtf_content += r"\par"

        rtf_content += r"{\cf3\b\ul PROFESSIONAL EXPERIENCE\par}"

        for job in self.data.experience:
            rtf_content += r"{\cf3\b " + job['title'] + r"\par}"
            rtf_content += job['company'] + " | " + job['dates'] + r"\par"
            rtf_content += r"{\cf2\i " + job['subtitle'] + r"\par}"
            for resp in job['responsibilities']:
                rtf_content += "▸ " + resp + r"\par"
            rtf_content += r"\par"

        rtf_content += r"{\i Additional experience and project details available on LinkedIn\par}"
        rtf_content += r"\par"
        rtf_content += r"{\cf3\b\ul KEY ACHIEVEMENTS AND IMPACT\par}"

        for category, achievements in self.data.achievements.items():
            rtf_content += r"{\cf2\b " + category + r"\par}"
            for achievement in achievements:
                rtf_content += "✓ " + achievement + r"\par"
            rtf_content += r"\par"

        rtf_content += "}"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rtf_content)

        print(f"📄 RTF generated: {output_path}")
        print("💡 Open this RTF file in Pages and save as .pages format")
        return str(output_path)


def load_config_from_json(input_dir, basename):
    """Load configuration from JSON file in input directory"""
    config_file = Path(input_dir) / 'config.json'
    print(f"🔧 DEBUG: Looking for config at: {config_file}")
    print(f"   DEBUG: Config file exists: {config_file.exists()}")

    if config_file.exists():
        print(f"   DEBUG: Loading existing config file...")
        with open(config_file, 'r') as f:
            config_data = json.load(f)

        config = ResumeConfig()
        for key, value in config_data.items():
            if hasattr(config, key) and not key.startswith('_'):
                setattr(config, key, value)

        print(f"📄 Loaded config: {config_file}")
        return config
    else:
        print(f"   DEBUG: Creating new config file...")
        # Create default config file
        config = ResumeConfig()
        config_dict = {attr: getattr(config, attr) for attr in dir(config)
                      if not attr.startswith('_') and not callable(getattr(config, attr))}

        # Add metadata
        config_dict['_metadata'] = {
            'basename': basename,
            'created': datetime.now().isoformat(),
            'version': '1.0',
            'description': f'Configuration for {basename} resume'
        }

        # Ensure input directory exists
        print(f"   DEBUG: Ensuring input directory exists: {input_dir}")
        Path(input_dir).mkdir(parents=True, exist_ok=True)
        print(f"   DEBUG: Input directory created/exists: {Path(input_dir).exists()}")

        print(f"   DEBUG: Writing config to: {config_file}")
        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=2, default=str)
        print(f"   DEBUG: Config file written, exists now: {config_file.exists()}")

        print(f"📄 Created default config: {config_file}")
        return config


def load_resume_data(input_dir, basename):
    """Load resume data from JSON file in input directory"""
    data_file = Path(input_dir) / 'resume_data.json'
    print(f"🔧 DEBUG: Looking for resume data at: {data_file}")
    print(f"   DEBUG: Resume data file exists: {data_file.exists()}")

    if data_file.exists():
        print(f"   DEBUG: Loading existing resume data file...")
        print(f"📄 Loading resume data: {data_file}")
        return ResumeData(data_file)
    else:
        print(f"   DEBUG: Creating new resume data file...")
        # Create default data file
        data = ResumeData()

        # Ensure input directory exists
        print(f"   DEBUG: Ensuring input directory exists: {input_dir}")
        Path(input_dir).mkdir(parents=True, exist_ok=True)
        print(f"   DEBUG: Input directory created/exists: {Path(input_dir).exists()}")

        print(f"   DEBUG: Writing resume data to: {data_file}")
        data.save_to_json(data_file)
        print(f"   DEBUG: Resume data file written, exists now: {data_file.exists()}")

        print(f"📄 Created default resume data: {data_file}")
        return data


def main():
    """Main function to generate resume"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate professional resume in multiple formats')
    parser.add_argument('--format', choices=['pdf', 'docx', 'rtf', 'all'], default='pdf',
                       help='Output format (default: pdf)')
    parser.add_argument('--basename', default='resume',
                       help='Base filename and directory name (default: resume)')
    parser.add_argument('--input-dir', default=None,
                       help='Custom input directory (default: inputs/{basename})')
    parser.add_argument('--output-dir', default=None,
                       help='Custom output directory (default: outputs/{basename})')

    args = parser.parse_args()

    print(f"🔧 DEBUG: Command line args:")
    print(f"   DEBUG: basename = {args.basename}")
    print(f"   DEBUG: format = {args.format}")
    print(f"   DEBUG: input-dir = {args.input_dir}")
    print(f"   DEBUG: output-dir = {args.output_dir}")
    print()

    # Set up directory paths
    if args.input_dir:
        input_path = Path(args.input_dir)
        print(f"🔧 DEBUG: Using custom input directory: {input_path}")
    else:
        input_path = Path('inputs') / args.basename
        print(f"🔧 DEBUG: Using default input path: inputs/{args.basename} = {input_path}")

    if args.output_dir:
        output_path = Path(args.output_dir)
        print(f"🔧 DEBUG: Using custom output directory: {output_path}")
    else:
        output_path = Path('outputs') / args.basename
        print(f"🔧 DEBUG: Using default output path: outputs/{args.basename} = {output_path}")

    print(f"🔧 DEBUG: Final paths:")
    print(f"   DEBUG: input_path = {input_path} (absolute: {input_path.absolute()})")
    print(f"   DEBUG: output_path = {output_path} (absolute: {output_path.absolute()})")
    print()

    print(f"🚀 Professional Resume Generator")
    print(f"📋 Resume: {args.basename}")
    print(f"📁 Input:  {input_path}")
    print(f"📁 Output: {output_path}")
    print()

    # Load configuration and data
    print(f"🔧 DEBUG: Loading configuration and data...")
    config = load_config_from_json(input_path, args.basename)
    data = load_resume_data(input_path, args.basename)
    print(f"🔧 DEBUG: Configuration and data loaded successfully")
    print()

    # Generate resume
    print(f"🔧 DEBUG: Creating ResumeGenerator...")
    generator = ResumeGenerator(
        config=config,
        data=data,
        input_dir=input_path,
        output_dir=output_path,
        basename=args.basename
    )
    print(f"🔧 DEBUG: ResumeGenerator created successfully")
    print()

    generated_files = []

    if args.format == 'all':
        formats = ['pdf', 'docx', 'rtf']
    else:
        formats = [args.format]

    print(f"🎨 Generating {len(formats)} format(s): {formats}")
    print()

    for fmt in formats:
        print(f"🔧 DEBUG: Generating {fmt} format...")
        if fmt == 'pdf':
            result = generator.generate_pdf(args.basename)
        elif fmt == 'docx':
            result = generator.generate_docx(args.basename)
        elif fmt == 'rtf':
            result = generator.generate_rtf(args.basename)

        if result:
            generated_files.append(result)
            print(f"🔧 DEBUG: ✅ {fmt} generation successful: {result}")
        else:
            print(f"🔧 DEBUG: ❌ {fmt} generation failed")
        print()

    print()
    print(f"✅ Resume generation complete!")
    print(f"📄 Generated {len(generated_files)} file(s)")

    print("\n🎯 Quick tips:")
    print(f"  • Edit {input_path}/config.json to customize colors and fonts")
    print(f"  • Edit {input_path}/resume_data.json to update content")
    print("  • PDF format recommended for applications")
    print("  • DOCX format good for ATS systems")
    print("  • RTF format can be opened in Pages")

    print("\n💡 Usage examples:")
    print(f"  python {Path(__file__).name} --format pdf --basename john_doe")
    print(f"  python {Path(__file__).name} --format all --basename data_scientist")
    print(f"  python {Path(__file__).name} --basename senior_dev --input-dir custom/input")

    print(f"\n📂 Your files are organized in:")
    print(f"   {input_path}/ (config & content)")
    print(f"   {output_path}/ (generated resumes)")

    return generated_files


if __name__ == "__main__":
    main()
