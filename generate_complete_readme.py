#!/usr/bin/env python3
"""
Generate complete README.md with links to all 1,024 resume files
"""

import os
from pathlib import Path

def generate_complete_readme():
    output_dir = Path("outputs")
    
    # Resume types and their display names
    resume_types = {
        "comprehensive": "Comprehensive",
        "data_engineering": "Data Engineering", 
        "software_engineering": "Software Engineering",
        "gis": "GIS/Geospatial",
        "product": "Product Management",
        "marketing": "Marketing Analytics",
        "data_analysis_visualization": "Data Analysis & Visualization",
        "polling_research_redistricting": "Polling/Research/Redistricting"
    }
    
    # Color schemes and their display names
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
    
    # Lengths
    lengths = ["long", "short"]
    
    # Output types
    output_types = ["ats", "human"]
    
    # File formats
    formats = ["pdf", "docx", "rtf", "md"]
    
    readme_content = []
    
    # Header
    readme_content.extend([
        "# Resume Portfolio - Complete Collection",
        "",
        "**1,024 professionally formatted resumes** systematically generated for different industries and use cases.",
        "",
        "## Table of Contents",
        "- [Overview](#overview)",
        "- [Resume Types](#resume-types)",
        "- [PDF Resumes](#pdf-resumes) ⭐ *Recommended for submissions*",
        "- [DOCX Resumes](#docx-resumes) ⭐ *Recommended for editing*", 
        "- [RTF Resumes](#rtf-resumes) 📄 *Universal compatibility*",
        "- [Markdown Resumes](#markdown-resumes) 🌐 *Web-ready format*",
        "- [Quick Selection Guide](#quick-selection-guide)",
        "",
        "## Overview",
        "**📊 Total Files:** 1,024 resumes organized by format and resume type",
        "**🎯 Output Types:** ATS-optimized and Human-readable versions",
        "**🎨 Color Schemes:** 8 professional color variations",
        "**📄 Formats:** PDF, DOCX, RTF, and Markdown",
        "",
        "## Resume Types"
    ])
    
    for key, name in resume_types.items():
        readme_content.append(f"- **{name}** - Specialized for {key.replace('_', ' ').title()} roles")
    
    readme_content.extend([
        "",
        "---",
        ""
    ])
    
    # Generate sections for each format
    for format_ext in formats:
        format_name = format_ext.upper()
        if format_ext == "md":
            format_name = "Markdown"
        
        readme_content.extend([
            f"## {format_name} Resumes",
            ""
        ])
        
        if format_ext == "pdf":
            readme_content.append("⭐ *Recommended for job applications and ATS systems*")
        elif format_ext == "docx":
            readme_content.append("⭐ *Recommended for customization and editing*")
        elif format_ext == "rtf":
            readme_content.append("📄 *Universal compatibility across all systems*")
        elif format_ext == "md":
            readme_content.append("🌐 *Web-ready format for online portfolios*")
        
        readme_content.append("")
        
        # For each resume type
        for resume_key, resume_name in resume_types.items():
            readme_content.extend([
                f"### {resume_name} {format_name}s",
                ""
            ])
            
            # Long versions
            readme_content.append("#### Long Format")
            for scheme_key, scheme_name in color_schemes.items():
                if format_ext == "md":
                    # Markdown only has human versions
                    link = f"human/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.{format_ext}"
                    readme_content.append(f"- [{scheme_name}]({link})")
                else:
                    # Other formats have both ATS and human versions
                    ats_link = f"ats/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.{format_ext}"
                    human_link = f"human/{resume_key}/long/{scheme_key}/dheeraj_chand_{resume_key}_long_{scheme_key}.{format_ext}"
                    readme_content.append(f"- [{scheme_name} (ATS)]({ats_link}) | [Human]({human_link})")
            
            readme_content.append("")
            
            # Short versions
            readme_content.append("#### Short Format")
            for scheme_key, scheme_name in color_schemes.items():
                if format_ext == "md":
                    # Markdown only has human versions
                    link = f"human/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.{format_ext}"
                    readme_content.append(f"- [{scheme_name}]({link})")
                else:
                    # Other formats have both ATS and human versions
                    ats_link = f"ats/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.{format_ext}"
                    human_link = f"human/{resume_key}/short/{scheme_key}/dheeraj_chand_{resume_key}_short_{scheme_key}.{format_ext}"
                    readme_content.append(f"- [{scheme_name} (ATS)]({ats_link}) | [Human]({human_link})")
            
            readme_content.append("")
        
        readme_content.extend([
            "---",
            ""
        ])
    
    # Quick selection guide
    readme_content.extend([
        "## Quick Selection Guide",
        "",
        "### 🎯 Most Popular Combinations",
        "- **Job Applications:** [Comprehensive PDF - Default Professional (ATS)](ats/comprehensive/long/default_professional/dheeraj_chand_comprehensive_long_default_professional.pdf)",
        "- **Tech Roles:** [Software Engineering PDF - Modern Tech (Human)](human/software_engineering/long/modern_tech/dheeraj_chand_software_engineering_long_modern_tech.pdf)",
        "- **Data Roles:** [Data Engineering PDF - Modern Tech (Human)](human/data_engineering/long/modern_tech/dheeraj_chand_data_engineering_long_modern_tech.pdf)",
        "- **Customization:** [Comprehensive DOCX - Default Professional (Human)](human/comprehensive/long/default_professional/dheeraj_chand_comprehensive_long_default_professional.docx)",
        "",
        "### 📋 Format Recommendations",
        "- **PDF:** Best for submissions, maintains formatting",
        "- **DOCX:** Best for editing and customization", 
        "- **RTF:** Best for maximum compatibility",
        "- **Markdown:** Best for web portfolios and GitHub",
        "",
        "### 🎨 Color Scheme Guide",
        "- **Default Professional:** Clean, traditional styling",
        "- **Modern Tech:** Contemporary design for tech roles",
        "- **Corporate Blue:** Professional corporate styling",
        "- **Cartographic Professional:** GIS/mapping industry focus",
        "",
        "---",
        "",
        f"*Generated {len([f for f in Path('outputs').rglob('*') if f.is_file() and not f.name.startswith('.')])} files systematically organized by format and specialization.*"
    ])
    
    # Write the README
    readme_path = output_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write('\n'.join(readme_content))
    
    print(f"✅ Generated complete README.md with links to all files")
    print(f"📄 Total lines: {len(readme_content)}")

if __name__ == "__main__":
    generate_complete_readme()
