#!/usr/bin/env python3
"""
Interactive User Setup Script
Creates personalized configuration for the resume generation system
"""

import json
import re
from pathlib import Path
from user_config import UserConfig

def get_user_input(prompt, default=None, validator=None):
    """Get user input with optional default and validation"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if validator:
            validation_result = validator(user_input)
            if validation_result is not True:
                print(f"❌ {validation_result}")
                continue
        
        return user_input

def validate_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return "Please enter a valid email address"

def validate_url(url):
    """Basic URL validation"""
    if url.startswith(('http://', 'https://')):
        return True
    return "Please enter a valid URL starting with http:// or https://"

def validate_phone(phone):
    """Basic phone validation"""
    if len(phone) >= 10:
        return True
    return "Please enter a valid phone number"

def generate_base_name(full_name):
    """Generate a base name from full name"""
    # Remove special characters and convert to lowercase
    name = re.sub(r'[^a-zA-Z\s]', '', full_name)
    # Split into words and join with underscore
    words = name.lower().split()
    return '_'.join(words)

def main():
    """Main setup function"""
    print("🚀 Professional Resume Generator - User Setup")
    print("=" * 60)
    print("This setup will create your personalized configuration.")
    print("You can always edit user_config.json later to make changes.")
    print()
    
    # Check if config already exists
    config_file = Path("user_config.json")
    if config_file.exists():
        response = input("⚠️  Configuration file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Setup cancelled")
            return
        print()
    
    # Collect personal information
    print("📝 Personal Information")
    print("-" * 25)
    
    full_name = get_user_input("Full Name (as it should appear on resumes)")
    phone = get_user_input("Phone Number", validator=validate_phone)
    email = get_user_input("Email Address", validator=validate_email)
    website = get_user_input("Website URL (optional)", default="")
    linkedin = get_user_input("LinkedIn URL (optional)", default="")
    
    print()
    
    # Generate base name for files
    suggested_base_name = generate_base_name(full_name)
    print("📁 File and Directory Naming")
    print("-" * 30)
    print("Files will be named: {base_name}_{version}_{color_scheme}.pdf")
    print("Directories will be named: {prefix}_{version_type}")
    print()
    
    base_name = get_user_input("Base name for files", default=suggested_base_name)
    directory_prefix = get_user_input("Directory prefix", default=base_name)
    
    print()
    
    # Professional titles
    print("💼 Professional Titles")
    print("-" * 22)
    print("Customize the professional titles for each resume version:")
    print()
    
    default_titles = {
        "research": "Director of Research and Analysis",
        "technical": "Senior Data Engineer & Technical Architect", 
        "software": "Senior Software Engineer",
        "consulting": "Data Analytics & Technology Consultant",
        "comprehensive": "Research, Data & Engineering Professional",
        "marketing": "Senior Product Marketing Manager"
    }
    
    custom_titles = {}
    for version, default_title in default_titles.items():
        title = get_user_input(f"{version.title()} version title", default=default_title)
        custom_titles[version] = title
    
    print()
    
    # Optional: Industry focus
    print("🏢 Additional Information (Optional)")
    print("-" * 35)
    
    industry_focus = get_user_input("Primary industry focus", default="technology")
    years_experience = get_user_input("Years of experience", default="10+")
    
    # Build configuration
    config = {
        "personal_info": {
            "name": full_name,
            "phone": phone,
            "email": email,
            "website": website,
            "linkedin": linkedin
        },
        "file_naming": {
            "base_name": base_name
        },
        "directory_naming": {
            "prefix": directory_prefix
        },
        "titles": custom_titles,
        "resume_content": {
            "industry_focus": industry_focus,
            "years_experience": years_experience,
            "specializations": [
                "Data Engineering",
                "Software Development", 
                "System Architecture"
            ]
        }
    }
    
    # Save configuration
    user_config = UserConfig.__new__(UserConfig)  # Create without __init__
    user_config.config_file = config_file
    user_config.save_config(config)
    
    print()
    print("✅ Configuration saved successfully!")
    print()
    print("📋 Your Configuration Summary:")
    print(f"   Name: {full_name}")
    print(f"   Email: {email}")
    print(f"   File base name: {base_name}")
    print(f"   Directory prefix: {directory_prefix}")
    print()
    print("🚀 Next Steps:")
    print("   1. Review/edit user_config.json if needed")
    print("   2. Create your resume content templates:")
    print(f"      python resume_data_generator.py --generate-data")
    print("   3. Generate your first resume:")
    print(f"      python resume_manager.py --version software --format pdf")
    print()
    print("💡 Pro Tip: Your resume files will be named like:")
    print(f"   {base_name}_software_default_professional.pdf")
    print(f"   {base_name}_technical_corporate_blue.docx")

if __name__ == "__main__":
    main()