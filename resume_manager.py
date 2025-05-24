#!/usr/bin/env python3
"""
Resume Management Script for Dheeraj Chand
Provides granular control over resume generation using your existing data
"""

import subprocess
import sys
import argparse
from pathlib import Path

class ResumeManager:
    """Manages resume generation for multiple versions"""

    def __init__(self):
        self.versions = {
            'research': 'dheeraj_chand_research_focused',
            'technical': 'dheeraj_chand_technical_detailed',
            'comprehensive': 'dheeraj_chand_comprehensive_full',
            'consulting': 'dheeraj_chand_consulting_minimal',
            'software': 'dheeraj_chand_software_engineer',
            'marketing': 'dheeraj_chand_product_marketing'
        }

        self.color_schemes = [
            'default_professional',
            'corporate_blue',
            'modern_tech'
        ]

        self.formats = ['pdf', 'docx', 'rtf']

    def run_command(self, cmd):
        """Run a command and return success status"""
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def check_setup(self):
        """Check if the system is properly set up"""
        print("🔍 Checking system setup...")

        # Check required files
        required_files = ['resume_data_generator.py', 'reportlab_resume.py']
        missing_files = []

        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
            return False

        # Check dependencies
        try:
            import reportlab
            print("✅ ReportLab found")
        except ImportError:
            print("❌ ReportLab not found. Install with: pip install reportlab")
            return False

        try:
            import docx
            print("✅ python-docx found")
        except ImportError:
            print("⚠️  python-docx not found. DOCX generation will be skipped.")
            print("   Install with: pip install python-docx")

        print("✅ System setup OK")
        return True

    def generate_data(self, color_scheme='default_professional'):
        """Generate resume data using your existing generator"""
        print(f"📝 Generating resume data with {color_scheme} color scheme...")

        success, output = self.run_command(f"python resume_data_generator.py --color-scheme {color_scheme}")

        if success:
            print("✅ Resume data generated")
            return True
        else:
            print(f"❌ Failed to generate resume data")
            print(f"Error: {output}")
            return False

    def generate_single_resume(self, version_key, format_type='pdf'):
        """Generate a single resume version"""
        if version_key not in self.versions:
            print(f"❌ Unknown version: {version_key}")
            print(f"Available versions: {', '.join(self.versions.keys())}")
            return False

        version_name = self.versions[version_key]

        # Check if input directory exists
        input_dir = Path("inputs") / version_name
        if not input_dir.exists():
            print(f"❌ Input directory not found: {input_dir}")
            print("Run with --generate-data first")
            return False

        print(f"📄 Generating {version_key} resume in {format_type.upper()} format...")

        cmd = f"python reportlab_resume.py --format {format_type} --basename {version_name}"
        success, output = self.run_command(cmd)

        if success:
            output_path = Path("outputs") / version_name / format_type / f"{version_name}.{format_type}"
            print(f"✅ Generated: {output_path}")
            return True
        else:
            print(f"❌ Failed to generate {version_key} resume")
            print(f"Error: {output}")
            return False

    def generate_all_formats(self, version_key):
        """Generate all formats for a single version"""
        if version_key not in self.versions:
            print(f"❌ Unknown version: {version_key}")
            return False

        print(f"🚀 Generating all formats for {version_key}...")

        success_count = 0
        for fmt in self.formats:
            if self.generate_single_resume(version_key, fmt):
                success_count += 1

        print(f"✅ Generated {success_count}/{len(self.formats)} formats for {version_key}")
        return success_count == len(self.formats)

    def generate_all_versions(self, format_type='pdf'):
        """Generate all versions in specified format"""
        print(f"🚀 Generating all resume versions in {format_type.upper()} format...")

        success_count = 0
        failed_versions = []

        for version_key in self.versions.keys():
            if self.generate_single_resume(version_key, format_type):
                success_count += 1
            else:
                failed_versions.append(version_key)

        print(f"✅ Generated {success_count}/{len(self.versions)} versions")

        if failed_versions:
            print(f"❌ Failed versions: {', '.join(failed_versions)}")

        return len(failed_versions) == 0

    def generate_everything(self):
        """Generate all versions in all formats"""
        print("🚀 Generating ALL resume versions in ALL formats...")
        print("This may take a few minutes...")
        print()

        total_generated = 0
        total_possible = len(self.versions) * len(self.formats)

        for version_key in self.versions.keys():
            print(f"📋 Processing {version_key}...")
            for fmt in self.formats:
                if self.generate_single_resume(version_key, fmt):
                    total_generated += 1

        print()
        print(f"🎉 Generation complete: {total_generated}/{total_possible} files generated")

        return total_generated

    def list_versions(self):
        """List available resume versions"""
        print("📋 Available resume versions:")
        print()

        descriptions = {
            'research': 'Research & Data Analytics Leader - For academic/research roles',
            'technical': 'Senior Geospatial Data Engineer - Technical depth emphasis',
            'comprehensive': 'Complete work history - All details included',
            'consulting': 'Data Analytics & Technology Consultant - Strategic advisor',
            'software': 'Senior Software Engineer - Platform development (DEFAULT)',
            'marketing': 'Senior Product Marketing Manager - Go-to-market focus'
        }

        for key, description in descriptions.items():
            version_name = self.versions[key]
            input_dir = Path("inputs") / version_name
            status = "✅" if input_dir.exists() else "❌"
            print(f"  {status} {key:12} - {description}")

        print()
        print("🎨 Available color schemes:")
        for scheme in self.color_schemes:
            print(f"  • {scheme}")

    def clean_outputs(self):
        """Clean output directories"""
        print("🧹 Cleaning output directories...")

        outputs_dir = Path("outputs")
        if outputs_dir.exists():
            import shutil
            shutil.rmtree(outputs_dir)
            print("✅ Output directories cleaned")
        else:
            print("ℹ️  No output directories to clean")

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Resume Manager for Dheeraj Chand - Generate individual or batch resumes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Setup and generate data
  python resume_manager.py --generate-data

  # Generate single resume
  python resume_manager.py --version software --format pdf

  # Generate all formats for one version
  python resume_manager.py --version technical --all-formats

  # Generate all versions in PDF
  python resume_manager.py --all-versions --format pdf

  # Generate everything
  python resume_manager.py --everything

  # List available versions
  python resume_manager.py --list
        """
    )

    # Data generation
    parser.add_argument('--generate-data', action='store_true',
                       help='Generate resume data files using existing generator')
    parser.add_argument('--color-scheme', choices=['default_professional', 'corporate_blue', 'modern_tech'],
                       default='default_professional',
                       help='Color scheme to use (default: default_professional)')

    # Single resume generation
    parser.add_argument('--version', choices=['research', 'technical', 'comprehensive', 'consulting', 'software', 'marketing'],
                       help='Resume version to generate')
    parser.add_argument('--format', choices=['pdf', 'docx', 'rtf'], default='pdf',
                       help='Output format (default: pdf)')

    # Batch operations
    parser.add_argument('--all-formats', action='store_true',
                       help='Generate all formats for specified version')
    parser.add_argument('--all-versions', action='store_true',
                       help='Generate all versions in specified format')
    parser.add_argument('--everything', action='store_true',
                       help='Generate all versions in all formats')

    # Utility
    parser.add_argument('--list', action='store_true',
                       help='List available resume versions')
    parser.add_argument('--clean', action='store_true',
                       help='Clean output directories')
    parser.add_argument('--check', action='store_true',
                       help='Check system setup')

    args = parser.parse_args()

    manager = ResumeManager()

    # Check system setup
    if args.check or not any(vars(args).values()):
        if not manager.check_setup():
            return 1
        if args.check:
            return 0

    # List versions
    if args.list:
        manager.list_versions()
        return 0

    # Clean outputs
    if args.clean:
        manager.clean_outputs()
        return 0

    # Generate data
    if args.generate_data:
        if not manager.generate_data(args.color_scheme):
            return 1

    # Generate everything
    if args.everything:
        if not manager.check_setup():
            return 1
        total = manager.generate_everything()
        return 0 if total > 0 else 1

    # Generate all versions in one format
    if args.all_versions:
        if not manager.check_setup():
            return 1
        success = manager.generate_all_versions(args.format)
        return 0 if success else 1

    # Generate single version
    if args.version:
        if not manager.check_setup():
            return 1

        if args.all_formats:
            success = manager.generate_all_formats(args.version)
        else:
            success = manager.generate_single_resume(args.version, args.format)

        return 0 if success else 1

    # Default: show help
    parser.print_help()
    return 0

if __name__ == "__main__":
    exit(main())
