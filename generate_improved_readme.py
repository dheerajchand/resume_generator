#!/usr/bin/env python3
"""
Generate improved README.md organized by resume type with tables
"""

import os
from pathlib import Path

def generate_improved_readme():
    output_dir = Path("outputs")
    
    # Resume types with detailed descriptions
    resume_types = {
        "comprehensive": {
            "name": "Comprehensive",
            "description": "Complete career overview showcasing the full breadth of experience across data science, software engineering, and political analytics. Includes all major achievements, technical skills, and project highlights. Best for senior-level positions and comprehensive career representation."
        },
        "data_engineering": {
            "name": "Data Engineering",
            "description": "Infrastructure-focused resume emphasizing data pipeline development, cloud architecture, and large-scale data processing. Highlights experience with ETL systems, data warehousing, and distributed computing. Ideal for data engineering and platform engineering roles."
        },
        "software_engineering": {
            "name": "Software Engineering", 
            "description": "Programming and development expertise with emphasis on full-stack capabilities, system architecture, and technical leadership. Showcases coding proficiency, software design patterns, and development methodologies. Perfect for software engineering positions."
        },
        "gis": {
            "name": "GIS & Geospatial Analysis",
            "description": "Specialized focus on geographic information systems, spatial analysis, and geospatial machine learning. Emphasizes mapping technologies, spatial databases, and location-based analytics. Tailored for GIS analyst and geospatial developer roles."
        },
        "product": {
            "name": "Product Management",
            "description": "Business-focused resume highlighting product strategy, user research, and data-driven decision making. Emphasizes stakeholder management, product metrics, and cross-functional leadership. Designed for product management and strategy roles."
        },
        "marketing": {
            "name": "Marketing Analytics",
            "description": "Marketing technology and analytics specialization with focus on campaign optimization, audience segmentation, and performance measurement. Highlights digital marketing tools and data-driven marketing strategies. Perfect for marketing analytics positions."
        },
        "data_analysis_visualization": {
            "name": "Data Analysis & Visualization",
            "description": "Statistical analysis and data storytelling expertise with emphasis on visualization, reporting, and insights generation. Showcases proficiency in analytics tools and presentation of complex data findings. Ideal for data analyst and business intelligence roles."
        },
        "polling_research_redistricting": {
            "name": "Political Research & Redistricting",
            "description": "Specialized political and electoral analytics with focus on polling methodology, redistricting technology, and political data analysis. Emphasizes expertise in electoral systems and political campaign analytics. Tailored for political consulting and research roles."
        }
    }
    
    # Color schemes with descriptions
    color_schemes = {
        "default_professional": "Default Professional",
        "corporate_blue": "Corporate Blue", 
        "modern_clean": "Modern Clean",
        "modern_tech": "Modern Tech",
        "cartographic_professional": "Cartographic Professional",
        "satellite_imagery": "Satellite Imagery",
        "terrain_mapping": "Terrain Mapping",
        "topographic_classic": "Topographic Classic"
    }
    
    # File formats with extensions and descriptions
    formats = {
        "pdf": {"ext": "pdf", "desc": "PDF", "icon": "📄", "note": "Best for submissions"},
        "docx": {"ext": "docx", "desc": "DOCX", "icon": "📝", "note": "Best for editing"},
        "rtf": {"ext": "rtf", "desc": "RTF", "icon": "📋", "note": "Universal compatibility"},
        "md": {"ext": "md", "desc": "Markdown", "icon": "🌐", "note": "Web-ready"}
    }
    
    readme_content = []
    
    # Header
    readme_content.extend([
        "# Resume Portfolio - Complete Collection",
        "",
        "**1,024 professionally formatted resumes** systematically generated for different industries and use cases.",
        "",
        "## Quick Navigation",
        "- [Overview](#overview)",
        "- [Resume Types](#resume-types)",
    ])
    
    # Add navigation links for each resume type
    for key, info in resume_types.items():
        readme_content.append(f"  - [{info['name']}](#{key.replace('_', '-')})")
    
    readme_content.extend([
        "- [Format Guide](#format-guide)",
        "- [Color Scheme Guide](#color-scheme-guide)",
        "",
        "## Overview",
        "**📊 Total Files:** 1,024 resumes organized by specialization and format",
        "**🎯 Output Types:** ATS-optimized and Human-readable versions",
        "**🎨 Color Schemes:** 8 professional color variations", 
        "**📄 Formats:** PDF, DOCX, RTF, and Markdown",
        "",
        "---",
        "",
        "## Resume Types",
        ""
    ])
    
    # Generate section for each resume type
    for resume_key, resume_info in resume_types.items():
        readme_content.extend([
            f"## {resume_info['name']}",
            "",
            resume_info['description'],
            "",
            "### Long Format",
            "",
            "| Color Scheme | PDF | DOCX | RTF | Markdown |",
            "|--------------|-----|------|-----|----------|"
        ])
        
        # Long format table
        for scheme_key, scheme_name in color_schemes.items():
            pdf_ats = f"ats/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.pdf"
            pdf_human = f"human/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.pdf"
            docx_ats = f"ats/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.docx"
            docx_human = f"human/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.docx"
            rtf_ats = f"ats/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.rtf"
            rtf_human = f"human/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.rtf"
            md_human = f"human/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.md"
            
            readme_content.append(
                f"| **{scheme_name}** | [ATS]({pdf_ats}) \\| [Human]({pdf_human}) | "
                f"[ATS]({docx_ats}) \\| [Human]({docx_human}) | "
                f"[ATS]({rtf_ats}) \\| [Human]({rtf_human}) | "
                f"[View]({md_human}) |"
            )
        
        readme_content.extend([
            "",
            "### Short Format",
            "",
            "| Color Scheme | PDF | DOCX | RTF | Markdown |",
            "|--------------|-----|------|-----|----------|"
        ])
        
        # Short format table
        for scheme_key, scheme_name in color_schemes.items():
            pdf_ats = f"ats/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.pdf"
            pdf_human = f"human/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.pdf"
            docx_ats = f"ats/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.docx"
            docx_human = f"human/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.docx"
            rtf_ats = f"ats/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.rtf"
            rtf_human = f"human/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.rtf"
            md_human = f"human/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.md"
            
            readme_content.append(
                f"| **{scheme_name}** | [ATS]({pdf_ats}) \\| [Human]({pdf_human}) | "
                f"[ATS]({docx_ats}) \\| [Human]({docx_human}) | "
                f"[ATS]({rtf_ats}) \\| [Human]({rtf_human}) | "
                f"[View]({md_human}) |"
            )
        
        readme_content.extend([
            "",
            "---",
            ""
        ])
    
    # Add guides
    readme_content.extend([
        "## Format Guide",
        "",
        "| Format | Best For | Features |",
        "|--------|----------|----------|",
        "| **PDF** 📄 | Job applications, ATS systems | Preserves formatting, universal compatibility |",
        "| **DOCX** 📝 | Customization, editing | Easy to modify, widely supported |",
        "| **RTF** 📋 | Maximum compatibility | Works with any word processor |",
        "| **Markdown** 🌐 | Web portfolios, GitHub | Version control friendly, web-ready |",
        "",
        "## Color Scheme Guide",
        "",
        "| Scheme | Style | Best For |",
        "|--------|-------|----------|",
        "| **Default Professional** | Clean, traditional | General business, conservative industries |",
        "| **Corporate Blue** | Professional corporate | Finance, consulting, enterprise |",
        "| **Modern Clean** | Minimalist, contemporary | Startups, design-focused roles |",
        "| **Modern Tech** | Tech-forward styling | Software, data science, engineering |",
        "| **Cartographic Professional** | GIS-themed | Mapping, geospatial, urban planning |",
        "| **Satellite Imagery** | Earth observation theme | Remote sensing, environmental |",
        "| **Terrain Mapping** | Topographic styling | Surveying, geology, outdoor industries |",
        "| **Topographic Classic** | Traditional mapping | Government, military, classic GIS |",
        "",
        "---",
        "",
        "## Quick Recommendations",
        "",
        "### 🎯 Most Popular Choices",
        "- **General Applications:** [Comprehensive - Default Professional (PDF, Human)](human/comprehensive/long/default_professional/dheeraj_chand_comprehensive_long_default_professional.pdf)",
        "- **Tech Companies:** [Software Engineering - Modern Tech (PDF, Human)](human/software_engineering/long/modern_tech/dheeraj_chand_software_engineering_long_modern_tech.pdf)",
        "- **Data Roles:** [Data Engineering - Modern Tech (PDF, Human)](human/data_engineering/long/modern_tech/dheeraj_chand_data_engineering_long_modern_tech.pdf)",
        "- **Customization:** [Comprehensive - Default Professional (DOCX, Human)](human/comprehensive/long/default_professional/dheeraj_chand_comprehensive_long_default_professional.docx)",
        "",
        "### 📋 ATS vs Human Versions",
        "- **ATS Version:** Optimized for Applicant Tracking Systems, simpler formatting",
        "- **Human Version:** Enhanced visual design for human readers, richer formatting",
        "",
        "---",
        "",
        f"*Generated {len([f for f in Path('outputs').rglob('*') if f.is_file() and not f.name.startswith('.') and f.name != 'README.md'])} resume files systematically organized by specialization and format.*"
    ])
    
    # Write the README
    readme_path = output_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write('\n'.join(readme_content))
    
    print(f"✅ Generated improved README.md organized by resume type with tables")
    print(f"📄 Total lines: {len(readme_content)}")

if __name__ == "__main__":
    generate_improved_readme()
