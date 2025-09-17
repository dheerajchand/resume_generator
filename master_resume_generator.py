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

def create_specialized_resume(master_data, resume_type, output_type="ats"):
    """Create a specialized resume from master data"""
    
    master = master_data["comprehensive_master_achievements"]
    
    # Base structure
    resume = {
        "personal_info": master["personal_info"],
        "summary": "",
        "achievements": {"Impact": []},
        "competencies": {},
        "experience": [],
        "projects": [],
        "education": [
            {
                "degree": "Bachelor of Arts in Plan II Honors",
                "institution": "University of Texas at Austin",
                "location": "Austin, TX",
                "dates": "2008",
                "gpa": "",
                "honors": "Interdisciplinary liberal arts program"
            }
        ],
        "additional_info": ""
    }
    
    # Select summary based on resume type and output type
    if output_type == "human":
        if resume_type == "comprehensive":
            resume["summary"] = master["professional_summary"]["comprehensive"]
        elif resume_type == "data_engineering":
            resume["summary"] = "Data engineering professional with 15+ years building systems that matter. Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%. Built Civic Graph data warehouse processing billions of records and platforms serving thousands of analysts nationwide."
        elif resume_type == "software_engineering":
            resume["summary"] = "Software engineer with 15+ years building systems that matter. Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%. Expert in translating complex analytical requirements into scalable technical solutions."
        elif resume_type == "gis":
            resume["summary"] = "GIS and geospatial data scientist with 15+ years building systems that matter. Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%. Expert in geospatial analysis, redistricting, and demographic modeling."
        elif resume_type == "product":
            resume["summary"] = "Product-focused data scientist with 15+ years building systems that matter. Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%. Expert in translating technical solutions into business value."
        elif resume_type == "marketing":
            resume["summary"] = "Marketing analytics professional with 15+ years building systems that matter. Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%. Expert in campaign optimization and audience segmentation."
        elif resume_type == "data_analysis_visualization":
            resume["summary"] = "Data analysis and visualization expert with 15+ years building systems that matter. Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%. Expert in statistical modeling and data storytelling."
        elif resume_type == "polling_research_redistricting":
            resume["summary"] = "Polling and research professional with 15+ years building systems that matter. Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%. Expert in survey methodology and electoral forecasting."
        else:
            resume["summary"] = master["professional_summary"]["comprehensive"]
    else:  # ATS version
        resume["summary"] = master["professional_summary"]["technical_focused"]
    
    # Select achievements based on resume type (always include core achievements)
    core_achievements = [
        master["core_achievements"]["demographic_discovery"]["headline"],
        "Algorithm reduced mapping costs by 73.5%, saving campaigns and organizations $4.7M",
        "Built redistricting platform used by thousands of analysts nationwide",
        "Achieved 87% prediction accuracy for voter turnout vs. industry standard of 71%"
    ]
    
    # Add role-specific achievements
    if resume_type == "data_engineering":
        core_achievements.extend([
            "Built Civic Graph data warehouse processing billions of records for electoral analytics",
            "Designed ETL pipelines using PySpark, dbt, and PostgreSQL/PostGIS for geospatial datasets",
            "Maintained sub-200ms query response across billion-record datasets"
        ])
    elif resume_type == "software_engineering":
        core_achievements.extend([
            "Developed custom tile server enabling interactive visualization improving contact rates by 53%",
            "Built scalable web applications supporting thousands of concurrent users",
            "Engineered distributed systems architecture for population-scale analysis"
        ])
    elif resume_type == "gis":
        core_achievements.extend([
            "Processed geospatial data covering 3.8 million square miles of US electoral territory",
            "Developed boundary analysis algorithms for redistricting optimization",
            "Built custom tile server for Web Map Service (WMS) integration"
        ])
    
    resume["achievements"]["Impact"] = core_achievements[:8]  # Limit for readability
    
    # Build experience from master data (always include all major roles)
    resume["experience"] = [
        {
            "title": "Founder & Principal Data Scientist",
            "company": "Siege Analytics",
            "location": "Austin, TX", 
            "dates": "2012 - Present",
            "subtitle": "Data Science & Political Analytics",
            "responsibilities": master["core_achievements"]["demographic_discovery"]["details"][:6]
        },
        {
            "title": "Senior Software Engineer",
            "company": "NGP VAN",
            "location": "Washington, DC",
            "dates": "2012 - 2015", 
            "subtitle": "Political Technology & CRM Systems",
            "responsibilities": [
                "Maintained geospatial analysis tools for Java-based CRM system used by tens of thousands simultaneously",
                "Developed custom tile server enabling interactive visualization improving contact rates by 53% and segmentation accuracy by 88%",
                "Built advanced geospatial analysis capabilities using Java, JavaScript, MySQL, and TileMill",
                "Integrated mapping and visualization tools for political campaign data analysis"
            ]
        },
        {
            "title": "Research Director", 
            "company": "PCCC",
            "location": "Washington, DC",
            "dates": "2010 - 2012",
            "subtitle": "Political Research & Data Analysis (FLEEM System)",
            "responsibilities": master["core_achievements"]["platform_development"]["fleem_system"][:5]
        }
    ]
    
    # Build projects from master data
    resume["projects"] = [
        {
            "name": "National Redistricting Platform",
            "dates": "2020 - 2021",
            "description": "Cloud-based GeoDjango platform for redistricting analysis with real-time collaborative editing and Census integration, used by thousands of analysts nationwide",
            "technologies": ["GeoDjango", "PostGIS", "AWS", "Docker", "React", "Python"],
            "impact": "Reduced mapping costs by 73.5%, saving organizations $4.7M in operational expenses"
        },
        {
            "name": "FLEEM Political Polling System", 
            "dates": "2010 - 2012",
            "description": "Completely self-built IVR system using Twilio API that contacted tens of thousands of voters daily, replicated call center functionality to performance parity",
            "technologies": ["Twilio API", "Python", "Django", "PostgreSQL", "JavaScript"],
            "impact": "Saved $840K in operational costs plus millions in avoided software licensing"
        },
        {
            "name": "Geospatial Demographic Classification System",
            "dates": "2013 - 2016", 
            "description": "Machine learning platform that discovered systematic coding errors and improved demographic classification accuracy from 23% to 64%",
            "technologies": ["Python", "Scikit-learn", "PostGIS", "GeoPandas", "TensorFlow"],
            "impact": "Corrected demographic data affecting all Black and Asian-American voters nationwide"
        },
        {
            "name": "Polling Consortium Dataset Meta-Analysis",
            "dates": "2013 - 2016",
            "description": "Comprehensive meta-analysis of polling data from tens of polling and mail firms with different methodologies and encoding systems",
            "technologies": ["Python", "R", "Statistical Analysis", "Meta-Analysis", "Data Standardization"], 
            "impact": "Created $400M dataset that became foundation for modern electoral analytics, estimated current value exceeds $1B"
        }
    ]
    
    # Build competencies based on resume type
    if resume_type == "data_engineering":
        resume["competencies"] = {
            "Data Engineering": [
                "Apache Spark, PySpark, Dask: Large-scale data processing and distributed computing",
                "dbt, Airflow: Data transformation pipelines and workflow orchestration", 
                "PostgreSQL/PostGIS, Snowflake: Database design and geospatial data management",
                "AWS (EC2, RDS, S3), Docker: Cloud infrastructure and containerization"
            ],
            "Programming": [
                "Python: NumPy, Pandas, Scikit-learn, Django, Flask (15+ years)",
                "SQL: Complex queries, optimization, spatial analysis (15+ years)",
                "R: Statistical modeling, ggplot2, spatial packages (12+ years)",
                "JavaScript: React, D3.js, Node.js, real-time applications (10+ years)"
            ]
        }
    else:
        # Default comprehensive competencies
        resume["competencies"] = master["technical_skills_comprehensive"]["programming_expertise"]
    
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
