#!/usr/bin/env python3
"""
Master Resume Generator - Single source of truth approach

This script maintains ONE master resume with all achievements and content,
then derives specialized resume types by selecting and emphasizing relevant content.
"""

import json
from pathlib import Path

# Load the comprehensive master achievements
def load_master_achievements():
    """Load the comprehensive master achievements file"""
    with open('comprehensive_master_achievements.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_resume_type_definitions():
    """Load the resume type configuration definitions"""
    with open('resume_type_definitions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_specialized_resume(master_data, resume_type, output_type="ats"):
    """Create a specialized resume from master data using configuration-driven inheritance"""
    
    master = master_data["comprehensive_master_achievements"]
    type_definitions = load_resume_type_definitions()
    config = type_definitions["resume_type_configurations"].get(resume_type, type_definitions["resume_type_configurations"]["comprehensive"])
    
    # INHERIT EVERYTHING from master (like abstract class inheritance)
    resume = {
        "personal_info": master["personal_info"],
        "summary": "",  # Will be set from master using config
        "achievements": {},  # Will be built from master using config
        "competencies": {},  # Will be built from master using config
        "experience": [],  # Will be built from master using config
        "projects": [],  # Will be built from master using config
        "education": [],  # Keep empty as requested
        "additional_info": ""
    }
    
    # OVERRIDE: Select summary from master using configuration
    summary_key = config["summary_key"]
    if summary_key in master["professional_summary"]:
        resume["summary"] = master["professional_summary"][summary_key]
    else:
        resume["summary"] = master["professional_summary"]["comprehensive"]
    
    # REFINE: Build achievements from master using configuration
    achievement_config = config["achievements"]
    # Use curated key achievements from master file
    key_achievements = master["key_achievements"]
    selected_achievements = []
    
    for achievement_key in achievement_config["include_achievements"]:
        if achievement_key in key_achievements:
            selected_achievements.append(key_achievements[achievement_key])
    
    resume["achievements"] = {"Impact": selected_achievements[:achievement_config["total_max"]]}
    
    # REFINE: Build work experience from master using configuration
    work_exp = master["work_experience"]
    experience_config = config["experience"]
    
    # Build positions from master data using configuration (everything traceable to master)
    resume["experience"] = []
    for position_key in experience_config["include_positions"]:
        if position_key in work_exp:
            # Special handling for Siege Analytics - always give it maximum responsibilities
            if position_key == "siege_analytics":
                max_resp = experience_config.get("siege_analytics_max", 10)
            else:
                max_resp = experience_config["max_responsibilities_per_job"]
                
            position = {
                "title": work_exp[position_key]["title"],
                "company": work_exp[position_key]["company"],
                "location": work_exp[position_key]["location"],
                "dates": work_exp[position_key]["dates"],
                "subtitle": work_exp[position_key]["subtitle"],
                "responsibilities": work_exp[position_key]["comprehensive_responsibilities"][:max_resp]
            }
            resume["experience"].append(position)
    
    # REFINE: Build projects from master using configuration
    key_projects = master["key_projects"]
    projects_config = config["projects"]
    
    # Build projects from master data using configuration (everything traceable to master)
    resume["projects"] = []
    for project_key in projects_config["include_projects"]:
        if project_key in key_projects:
            project_data = key_projects[project_key]
            project = {
                "name": project_data["name"],
                "dates": project_data.get("dates", ""),
                "description": project_data["description"],
                "technologies": project_data["technologies"],
                "impact": project_data["impact"]
            }
            # Add technical details if configuration specifies
            if projects_config["show_technical_details"] and "technical_details" in project_data:
                project["technical_details"] = project_data["technical_details"][:2]
            
            resume["projects"].append(project)
    
    # REFINE: Build competencies from master using configuration
    competencies_config = config["competencies"]
    tech_skills = master["technical_skills_comprehensive"]
    
    # Build competencies by selecting categories from master (everything traceable to master)
    resume["competencies"] = {}
    for category_key in competencies_config["include_categories"]:
        if category_key in tech_skills:
            category_data = tech_skills[category_key]
            # Map technical category names to display names
            display_name = {
                "programming_expertise": "Programming and Development",
                "geospatial_stack": "Geospatial Technologies", 
                "machine_learning_ai": "Machine Learning & AI",
                "data_engineering": "Data Infrastructure",
                "cloud_devops": "Cloud & DevOps"
            }.get(category_key, category_key.title())
            
            # Build skills list from master data with proper formatting
            skills_list = []
            for skill_key, skill_detail in category_data.items():
                # Format skill names properly
                formatted_skill_name = {
                    "python": "Python",
                    "r": "R", 
                    "sql": "SQL/PostGIS",
                    "javascript": "JavaScript",
                    "java": "Java",
                    "other": "Other Technologies",
                    "databases": "Databases",
                    "analysis": "Analysis Tools",
                    "web_mapping": "Web Mapping",
                    "processing": "Processing",
                    "frameworks": "ML Frameworks",
                    "geospatial_ml": "Geospatial ML",
                    "techniques": "Techniques",
                    "validation": "Validation",
                    "pipelines": "Pipelines",
                    "storage": "Storage",
                    "streaming": "Streaming",
                    "aws": "AWS",
                    "containerization": "Containerization", 
                    "monitoring": "Monitoring",
                    "cicd": "CI/CD"
                }.get(skill_key, skill_key.title())
                
                skills_list.append(f"{formatted_skill_name}: {skill_detail}")
            
            resume["competencies"][display_name] = skills_list
    
    return resume

def generate_all_specialized_resumes():
    """Generate all specialized resume types from master data"""
    
    master_data = load_master_achievements()
    
    resume_types = [
        "comprehensive", "data_engineering", "software_engineering", 
        "gis", "product", "marketing", "data_analysis_visualization",
        "polling_research_redistricting"
    ]
    
    output_types = ["ats", "human"]
    
    # Map to actual directory names
    type_mapping = {
        "comprehensive": "dheeraj_chand_comprehensive_full",
        "data_engineering": "dheeraj_chand_data_engineering", 
        "software_engineering": "dheeraj_chand_software_engineering",
        "gis": "dheeraj_chand_gis",
        "product": "dheeraj_chand_product",
        "marketing": "dheeraj_chand_marketing",
        "data_analysis_visualization": "dheeraj_chand_data_analysis_visualization",
        "polling_research_redistricting": "dheeraj_chand_polling_research_redistricting"
    }
    
    generated = 0
    
    for resume_type in resume_types:
        for output_type in output_types:
            
            # Generate specialized resume
            specialized_resume = create_specialized_resume(master_data, resume_type, output_type)
            
            # Determine output path
            dir_name = type_mapping[resume_type]
            if output_type == "human":
                dir_name += "_human"
                
            output_dir = Path("inputs") / dir_name
            output_dir.mkdir(exist_ok=True)
            
            # Write resume file
            output_file = output_dir / "resume_data.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(specialized_resume, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Generated: {output_file}")
            generated += 1
    
    print(f"\n🎯 Generated {generated} specialized resumes from master data!")

if __name__ == "__main__":
    generate_all_specialized_resumes()
