#!/usr/bin/env python3
"""
Generate All Resume Versions
Runs the ReportLab resume script for all versions in all formats
"""

import subprocess
import sys


def run_command(cmd):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {cmd}")
        print(f"Error: {e.stderr}")
        return False


def main():
    print("🚀 Generating all resume versions...")
    print()

    # Array of resume versions
    versions = [
        "dheeraj_chand_research_focused",
        "dheeraj_chand_technical_detailed",
        "dheeraj_chand_comprehensive_full",
        "dheeraj_chand_consulting_minimal",
        "dheeraj_chand_software_engineer",
        "dheeraj_chand_product_marketing",
    ]

    formats = ["pdf", "docx", "rtf"]

    # Generate each version in all formats
    for version in versions:
        print(f"📄 Generating: {version}")

        success = True
        for fmt in formats:
            cmd = f"python reportlab_resume.py --format {fmt} --basename {version}"
            if not run_command(cmd):
                success = False
                break

        if success:
            print(f"✅ Completed: {version}")
        else:
            print(f"❌ Failed: {version}")
            sys.exit(1)
        print()

    print("🎉 All resume versions generated successfully!")
    print()
    print("📁 Find your resumes in:")
    print("   outputs/dheeraj_chand_research_focused/")
    print("   outputs/dheeraj_chand_technical_detailed/")
    print("   outputs/dheeraj_chand_comprehensive_full/")
    print("   outputs/dheeraj_chand_consulting_minimal/")
    print("   outputs/dheeraj_chand_software_engineer/")
    print("   outputs/dheeraj_chand_product_marketing/")
    print()
    print("💡 Each directory contains PDF, DOCX, and RTF versions")


if __name__ == "__main__":
    main()
