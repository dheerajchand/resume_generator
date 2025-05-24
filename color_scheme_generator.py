#!/usr/bin/env python3
"""
Resume Data Generator with Configurable Color Schemes
Creates structured JSON input files for multiple resume versions
"""

import json
from pathlib import Path
from datetime import datetime
import argparse

class ColorScheme:
    """Color scheme with role-based colors for resume styling"""

    def __init__(self, scheme_name="default"):
        self.scheme_name = scheme_name
        self.colors = {
            'NAME_COLOR': '#228B22',           # Header name color
            'TITLE_COLOR': '#B8860B',          # Professional title color
            'SECTION_HEADER_COLOR': '#B8860B', # Section headers (underlined)
            'JOB_TITLE_COLOR': '#722F37',      # Job position titles
            'ACCENT_COLOR': '#722F37',         # General accent/highlight color
            'COMPETENCY_HEADER_COLOR': '#228B22', # Competency category headers
            'SUBTITLE_COLOR': '#228B22',       # Job subtitle/description
            'LINK_COLOR': '#B8860B',           # Hyperlinks (website, LinkedIn)
            'DARK_TEXT_COLOR': '#333333',      # Main body text
            'MEDIUM_TEXT_COLOR': '#666666',    # Secondary text (company info)
            'LIGHT_TEXT_COLOR': '#999999',     # Tertiary text
        }

        self.typography = {
            'FONT_MAIN': 'Helvetica',
            'FONT_BOLD': 'Helvetica-Bold',
            'FONT_ITALIC': 'Helvetica-Oblique',
            'NAME_SIZE': 24,
            'TITLE_SIZE': 14,
            'SECTION_HEADER_SIZE': 12,
            'JOB_TITLE_SIZE': 11,
            'BODY_SIZE': 9,
            'CONTACT_SIZE': 9,
        }

        self.layout = {
            'PAGE_MARGIN': 0.6,
            'SECTION_SPACING': 0.12,
            'PARAGRAPH_SPACING': 0.06,
            'LINE_SPACING': 1.15,
            'JOB_SPACING': 6,
            'CATEGORY_SPACING': 4,
            'MAX_PAGES': 2,
            'BULLET_CHAR': '▸',
        }

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        config = {}
        config.update(self.colors)
        config.update(self.typography)
        config.update(self.layout)
        config['_metadata'] = {
            'scheme_name': self.scheme_name,
            'created': datetime.now().isoformat(),
            'description': f'{self.scheme_name} color scheme for professional resume'
        }
        return config

    def save_to_file(self, filepath):
        """Save ColorScheme to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"✅ Saved color scheme: {filepath}")

class PredefinedSchemes:
    """Collection of predefined color schemes"""

    @staticmethod
    def default_professional():
        """Green, Gold, Burgundy - Professional and distinctive"""
        scheme = ColorScheme("default_professional")
        scheme.colors.update({
            'NAME_COLOR': '#228B22',           # Forest Green
            'TITLE_COLOR': '#B8860B',          # Dark Goldenrod
            'SECTION_HEADER_COLOR': '#B8860B', # Dark Goldenrod
            'JOB_TITLE_COLOR': '#722F37',      # Deep Burgundy
            'ACCENT_COLOR': '#722F37',         # Deep Burgundy
            'COMPETENCY_HEADER_COLOR': '#228B22', # Forest Green
            'SUBTITLE_COLOR': '#228B22',       # Forest Green
            'LINK_COLOR': '#B8860B',           # Dark Goldenrod
        })
        return scheme

    @staticmethod
    def corporate_blue():
        """Navy, Gray, Steel Blue - Corporate conservative"""
        scheme = ColorScheme("corporate_blue")
        scheme.colors.update({
            'NAME_COLOR': '#1F4E79',           # Navy Blue
            'TITLE_COLOR': '#333333',          # Charcoal
            'SECTION_HEADER_COLOR': '#333333', # Charcoal
            'JOB_TITLE_COLOR': '#4682B4',      # Steel Blue
            'ACCENT_COLOR': '#4682B4',         # Steel Blue
            'COMPETENCY_HEADER_COLOR': '#1F4E79', # Navy Blue
            'SUBTITLE_COLOR': '#1F4E79',       # Navy Blue
            'LINK_COLOR': '#4682B4',           # Steel Blue
        })
        return scheme

    @staticmethod
    def modern_tech():
        """Teal, Orange, Gray - Modern tech company feel"""
        scheme = ColorScheme("modern_tech")
        scheme.colors.update({
            'NAME_COLOR': '#2C5F5D',           # Deep Teal
            'TITLE_COLOR': '#FF6B35',          # Vibrant Orange
            'SECTION_HEADER_COLOR': '#FF6B35', # Vibrant Orange
            'JOB_TITLE_COLOR': '#2C5F5D',      # Deep Teal
            'ACCENT_COLOR': '#FF6B35',         # Vibrant Orange
            'COMPETENCY_HEADER_COLOR': '#2C5F5D', # Deep Teal
            'SUBTITLE_COLOR': '#2C5F5D',       # Deep Teal
            'LINK_COLOR': '#FF6B35',           # Vibrant Orange
        })
        return scheme

    @staticmethod
    def elegant_purple():
        """Purple, Gold, Gray - Elegant and creative"""
        scheme = ColorScheme("elegant_purple")
        scheme.colors.update({
            'NAME_COLOR': '#663399',           # Rebecca Purple
            'TITLE_COLOR': '#DAA520',          # Goldenrod
            'SECTION_HEADER_COLOR': '#DAA520', # Goldenrod
            'JOB_TITLE_COLOR': '#663399',      # Rebecca Purple
            'ACCENT_COLOR': '#663399',         # Rebecca Purple
            'COMPETENCY_HEADER_COLOR': '#663399', # Rebecca Purple
            'SUBTITLE_COLOR': '#663399',       # Rebecca Purple
            'LINK_COLOR': '#DAA520',           # Goldenrod
        })
        return scheme

def create_sample_resume_data():
    """Create sample resume data for testing"""
    return {
        'personal_info': {
            'name': 'JANE DOE',
            'title': 'Senior Software Engineer',
            'phone': '(123) 456-7890',
            'email': 'jane.doe@email.com',
            'website': 'https://janedoe.dev',
            'linkedin': 'https://linkedin.com/in/janedoe'
        },
        'summary': 'Experienced software engineer with 8+ years developing scalable web applications and leading cross-functional teams. Expert in full-stack development with deep knowledge of cloud architectures and DevOps practices.',
        'competencies': {
            'Programming Languages': [
                'Programming: Python, JavaScript, TypeScript, Java, Go',
                'Frameworks: React, Node.js, Django, Flask, Spring Boot',
                'Databases: PostgreSQL, MongoDB, Redis, MySQL'
            ],
            'Cloud & Infrastructure': [
                'AWS Services (EC2, S3, Lambda, RDS)',
                'Docker & Kubernetes',
                'CI/CD Pipelines',
                'Infrastructure as Code (Terraform)',
                'Monitoring & Logging (Datadog, New Relic)'
            ],
            'Leadership & Process': [
                'Team Leadership & Mentoring',
                'Agile/Scrum Methodologies',
                'Code Review & Quality Assurance',
                'Technical Architecture Design',
                'Cross-functional Collaboration'
            ]
        },
        'experience': [
            {
                'title': 'SENIOR SOFTWARE ENGINEER',
                'company': 'Tech Company Inc.',
                'dates': '2020 – Present',
                'subtitle': 'Full-Stack Development and Team Leadership',
                'responsibilities': [
                    'Lead development of microservices architecture serving 100K+ daily active users',
                    'Mentor junior developers and conduct technical interviews',
                    'Design and implement CI/CD pipelines reducing deployment time by 60%',
                    'Collaborate with product and design teams to deliver user-focused features'
                ]
            },
            {
                'title': 'SOFTWARE ENGINEER',
                'company': 'Startup Solutions LLC',
                'dates': '2018 – 2020',
                'subtitle': 'Full-Stack Web Development',
                'responsibilities': [
                    'Built responsive web applications using React and Node.js',
                    'Implemented RESTful APIs and database optimization strategies',
                    'Participated in code reviews and pair programming sessions',
                    'Contributed to technical architecture and tooling decisions'
                ]
            }
        ],
        'achievements': {
            'Technical Innovation': [
                'Architected scalable microservices handling 1M+ requests daily',
                'Reduced application load time by 40% through performance optimization',
                'Open source contributor with 500+ GitHub stars across projects'
            ],
            'Leadership Impact': [
                'Mentored 5 junior developers, with 3 receiving promotions',
                'Led cross-functional team of 8 engineers on major product launch',
                'Established engineering best practices adopted company-wide'
            ]
        }
    }

def create_directory_structure():
    """Create directory structure for resume generation"""
    base_inputs = Path("inputs")
    base_outputs = Path("outputs")
    color_schemes = Path("color_schemes")

    # Create main directories
    base_inputs.mkdir(exist_ok=True)
    base_outputs.mkdir(exist_ok=True)
    color_schemes.mkdir(exist_ok=True)

    # Create sample resume directory
    sample_dir = base_inputs / "sample_resume"
    sample_dir.mkdir(exist_ok=True)

    # Create output subdirectories
    sample_output = base_outputs / "sample_resume"
    for fmt in ['pdf', 'docx', 'rtf']:
        (sample_output / fmt).mkdir(parents=True, exist_ok=True)

    print("✅ Created directory structure")

def create_color_scheme_files():
    """Create predefined color scheme files"""
    schemes_dir = Path("color_schemes")
    schemes_dir.mkdir(exist_ok=True)

    schemes = {
        'default_professional.json': PredefinedSchemes.default_professional(),
        'corporate_blue.json': PredefinedSchemes.corporate_blue(),
        'modern_tech.json': PredefinedSchemes.modern_tech(),
        'elegant_purple.json': PredefinedSchemes.elegant_purple(),
    }

    for filename, scheme in schemes.items():
        filepath = schemes_dir / filename
        scheme.save_to_file(filepath)

    return schemes_dir

def save_resume_files(name, data, config):
    """Save resume data and config files"""
    input_dir = Path("inputs") / name
    input_dir.mkdir(parents=True, exist_ok=True)

    # Save data file
    data_file = input_dir / "resume_data.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save config file
    config_file = input_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Created resume files for: {name}")
    print(f"   Data: {data_file}")
    print(f"   Config: {config_file}")

def create_test_script():
    """Create a test script to verify setup"""
    script_content = '''#!/usr/bin/env python3
"""
Test Resume Generation System
Quick test to verify everything is working
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {cmd}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🧪 Testing Resume Generation System")
    print("=" * 50)

    # Check if required files exist
    required_files = [
        "inputs/sample_resume/resume_data.json",
        "inputs/sample_resume/config.json",
        "reportlab_resume.py"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        print("\\nRun: python color_scheme_generator.py --create-sample first")
        return 1

    print("✅ All required files found")

    # Test PDF generation
    print("\\n📄 Testing PDF generation...")
    if run_command("python reportlab_resume.py --format pdf --basename sample_resume"):
        pdf_path = Path("outputs/sample_resume/pdf/sample_resume.pdf")
        if pdf_path.exists():
            print(f"✅ PDF created: {pdf_path}")
        else:
            print("❌ PDF file not found")
            return 1
    else:
        return 1

    # Test DOCX generation (optional)
    print("\\n📄 Testing DOCX generation...")
    run_command("python reportlab_resume.py --format docx --basename sample_resume")

    print("\\n🎉 Test completed successfully!")
    print("\\n📁 Check your generated files in: outputs/sample_resume/")

    return 0

if __name__ == "__main__":
    exit(main())
'''

    script_file = Path("test_resume_system.py")
    with open(script_file, 'w') as f:
        f.write(script_content)

    print(f"✅ Created test script: {script_file}")

def main():
    """Main function to set up resume generation system"""
    parser = argparse.ArgumentParser(description='Set up resume generation system with color schemes')
    parser.add_argument('--color-scheme',
                       choices=['default_professional', 'corporate_blue', 'modern_tech', 'elegant_purple'],
                       default='default_professional',
                       help='Color scheme to use for sample resume')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create sample resume files for testing')

    args = parser.parse_args()

    print("🚀 Resume Generation System Setup")
    print("=" * 50)

    # Create directory structure
    print("\\n📁 Creating directory structure...")
    create_directory_structure()

    # Create color scheme files
    print("\\n🎨 Creating color scheme files...")
    create_color_scheme_files()

    # Create sample resume if requested
    if args.create_sample:
        print(f"\\n📝 Creating sample resume with {args.color_scheme} color scheme...")

        # Get selected color scheme
        if args.color_scheme == 'default_professional':
            scheme = PredefinedSchemes.default_professional()
        elif args.color_scheme == 'corporate_blue':
            scheme = PredefinedSchemes.corporate_blue()
        elif args.color_scheme == 'modern_tech':
            scheme = PredefinedSchemes.modern_tech()
        elif args.color_scheme == 'elegant_purple':
            scheme = PredefinedSchemes.elegant_purple()

        # Create sample resume data and config
        sample_data = create_sample_resume_data()
        sample_config = scheme.to_dict()

        save_resume_files("sample_resume", sample_data, sample_config)

        # Create test script
        print("\\n🧪 Creating test script...")
        create_test_script()

        print("\\n✅ Setup complete!")
        print("\\n🚀 Next steps:")
        print("   1. Run: python test_resume_system.py")
        print("   2. Check outputs in: outputs/sample_resume/")
        print("   3. Customize resume data in: inputs/sample_resume/resume_data.json")
        print("   4. Try different color schemes in: color_schemes/")
    else:
        print("\\n✅ Basic setup complete!")
        print("\\n🚀 To create sample resume:")
        print("   python color_scheme_generator.py --create-sample")
        print("   python color_scheme_generator.py --create-sample --color-scheme corporate_blue")

    print("\\n🎨 Available color schemes:")
    print("   • default_professional - Green, Gold, Burgundy")
    print("   • corporate_blue - Navy, Gray, Steel Blue")
    print("   • modern_tech - Teal, Orange, Gray")
    print("   • elegant_purple - Purple, Gold, Gray")

    print("\\n💡 Color scheme files saved in: color_schemes/")
    print("   Copy and customize any scheme for your needs!")

if __name__ == "__main__":
    main()
