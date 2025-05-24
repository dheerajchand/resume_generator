#!/usr/bin/env python3
"""
Generate All Resume Versions for Dheeraj Chand
Uses the existing resume_data_generator.py to create all resume versions
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")

    required_packages = ['reportlab', 'python-docx']
    missing_packages = []

    for package in required_packages:
        success, _ = run_command(f"python -c \"import {package.replace('-', '_')}\"")
        if not success:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install reportlab python-docx")
        return False

    print("✅ All dependencies found")
    return True

def check_required_files():
    """Check if required files exist"""
    print("🔍 Checking required files...")

    required_files = [
        'resume_data_generator.py',
        'reportlab_resume.py'
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False

    print("✅ All required files found")
    return True

def generate_resume_data():
    """Generate all resume data files using your existing generator"""
    print("📝 Generating resume data files...")

    # Your existing color schemes
    color_schemes = [
        'default_professional',
        'corporate_blue',
        'modern_tech'
    ]

    # Generate data files for each color scheme
    for scheme in color_schemes:
        print(f"   Creating data files with {scheme} color scheme...")
        success, output = run_command(f"python resume_data_generator.py --color-scheme {scheme}")
        if not success:
            print(f"❌ Failed to generate data with {scheme} scheme")
            print(f"Error: {output}")
            return False

    print("✅ Resume data files generated")
    return True

def generate_all_resumes():
    """Generate all resume versions in all formats"""
    print("🚀 Generating all resume versions...")
    print()

    # Your existing resume versions
    versions = [
        "dheeraj_chand_research_focused",
        "dheeraj_chand_technical_detailed",
        "dheeraj_chand_comprehensive_full",
        "dheeraj_chand_consulting_minimal",
        "dheeraj_chand_software_engineer",
        "dheeraj_chand_product_marketing"
    ]

    formats = ['pdf', 'docx', 'rtf']

    # Generate each version in all formats
    generated_count = 0
    failed_versions = []

    for version in versions:
        print(f"📄 Generating: {version}")

        # Check if input directory exists
        input_dir = Path("inputs") / version
        if not input_dir.exists():
            print(f"⚠️  Input directory not found: {input_dir}")
            print(f"   Run: python resume_data_generator.py first")
            failed_versions.append(version)
            continue

        success_count = 0
        for fmt in formats:
            cmd = f"python reportlab_resume.py --format {fmt} --basename {version}"
            success, output = run_command(cmd)

            if success:
                success_count += 1
                print(f"   ✅ {fmt.upper()}")
            else:
                print(f"   ❌ {fmt.upper()} failed")
                print(f"      Error: {output}")

        if success_count == len(formats):
            print(f"✅ Completed: {version}")
            generated_count += 1
        else:
            print(f"⚠️  Partial success: {version}")
            failed_versions.append(version)

        print()

    return generated_count, failed_versions

def create_test_script():
    """Create a quick test script"""
    test_script = '''#!/usr/bin/env python3
"""Quick test of single resume generation"""

import subprocess
from pathlib import Path

def test_single_resume():
    """Test generating a single resume"""
    print("🧪 Testing single resume generation...")

    # Test with software engineer version (your default)
    version = "dheeraj_chand_software_engineer"

    # Check if input exists
    input_dir = Path("inputs") / version
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        print("Run: python resume_data_generator.py first")
        return False

    # Test PDF generation
    cmd = f"python reportlab_resume.py --format pdf --basename {version}"
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ PDF generation successful")

        # Check if file was created
        pdf_path = Path("outputs") / version / "pdf" / f"{version}.pdf"
        if pdf_path.exists():
            print(f"✅ PDF file created: {pdf_path}")
            return True
        else:
            print("❌ PDF file not found")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ PDF generation failed: {e.stderr}")
        return False

if __name__ == "__main__":
    success = test_single_resume()
    exit(0 if success else 1)
'''

    with open('test_single_resume.py', 'w') as f:
        f.write(test_script)

    print("✅ Created test script: test_single_resume.py")

def display_results(generated_count, failed_versions, total_versions):
    """Display final results"""
    print("=" * 60)
    print("🎉 GENERATION COMPLETE!")
    print("=" * 60)

    print(f"✅ Successfully generated: {generated_count}/{total_versions} versions")

    if failed_versions:
        print(f"❌ Failed versions: {len(failed_versions)}")
        for version in failed_versions:
            print(f"   • {version}")

    print()
    print("📁 Find your resumes in:")

    successful_versions = [
        "dheeraj_chand_research_focused",
        "dheeraj_chand_technical_detailed",
        "dheeraj_chand_comprehensive_full",
        "dheeraj_chand_consulting_minimal",
        "dheeraj_chand_software_engineer",
        "dheeraj_chand_product_marketing"
    ]

    for version in successful_versions:
        if version not in failed_versions:
            print(f"   📂 outputs/{version}/")
            print(f"      ├── pdf/{version}.pdf")
            print(f"      ├── docx/{version}.docx")
            print(f"      └── rtf/{version}.rtf")

    print()
    print("💡 Tips:")
    print("   • Use research_focused for academic/research roles")
    print("   • Use technical_detailed for engineering positions")
    print("   • Use comprehensive_full when you need complete history")
    print("   • Use consulting_minimal for strategic advisory roles")
    print("   • Use software_engineer for development positions (DEFAULT)")
    print("   • Use product_marketing for marketing/product roles")

    print()
    print("🎨 Color schemes available:")
    print("   • Default Professional (Green, Gold, Burgundy)")
    print("   • Corporate Blue (Navy, Gray, Steel Blue)")
    print("   • Modern Tech (Teal, Orange, Gray)")

def main():
    """Main function"""
    print("🚀 Dheeraj Chand Resume Generator")
    print("=" * 50)
    print("Generating all resume versions from your existing data")
    print()

    # Step 1: Check dependencies
    if not check_dependencies():
        return 1

    # Step 2: Check required files
    if not check_required_files():
        return 1

    # Step 3: Generate resume data (this runs your existing generator)
    if not generate_resume_data():
        return 1

    # Step 4: Generate all resumes
    generated_count, failed_versions = generate_all_resumes()

    # Step 5: Create test script
    create_test_script()

    # Step 6: Display results
    total_versions = 6  # Your 6 resume versions
    display_results(generated_count, failed_versions, total_versions)

    return 0 if len(failed_versions) == 0 else 1

if __name__ == "__main__":
    exit(main())
