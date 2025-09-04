#!/usr/bin/env python3
"""
Resume Management Script for Professional Resume Generator
Provides granular control over resume generation using configurable user data
Now supports any user configuration!
"""

import subprocess
import sys
import argparse
import json
from pathlib import Path
from user_config import UserConfig


class ResumeManager:
    """Manages resume generation for multiple versions with color scheme organization"""

    def __init__(self):
        # Load user configuration
        try:
            self.user_config = UserConfig()
        except FileNotFoundError:
            print("❌ User configuration not found!")
            print(
                "🔧 Please run 'python setup_user.py' to create your configuration first."
            )
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading user configuration: {e}")
            sys.exit(1)

        # Validate user configuration
        try:
            self.user_config.validate_config()
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)

        self.versions = {
            "research": self.user_config.get_version_directory_name("research"),
            "technical": self.user_config.get_version_directory_name("technical"),
            "comprehensive": self.user_config.get_version_directory_name(
                "comprehensive"
            ),
            "consulting": self.user_config.get_version_directory_name("consulting"),
            "software": self.user_config.get_version_directory_name("software"),
            "marketing": self.user_config.get_version_directory_name("marketing"),
        }

        self.color_schemes = ["default_professional", "corporate_blue", "modern_tech"]

        self.formats = ["pdf", "docx", "rtf"]
        self.current_color_scheme = "default_professional"  # Track current scheme

    def run_command(self, cmd):
        """Run a command and return success status"""
        try:
            result = subprocess.run(
                cmd, shell=True, check=True, capture_output=True, text=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def get_current_color_scheme(self):
        """Detect current color scheme from existing config files"""
        # Check a sample config file to see what color scheme is active
        sample_version = "dheeraj_chand_software_engineer"
        config_path = Path("inputs") / sample_version / "config.json"

        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    metadata = config.get("_metadata", {})
                    return metadata.get("scheme_name", "default_professional")
            except:
                pass

        return "default_professional"

    def validate_color_scheme(self, color_scheme):
        """Validate that a color scheme exists (built-in or file)"""
        if not color_scheme:
            return True

        # Check built-in schemes
        built_ins = ["default_professional", "corporate_blue", "modern_tech"]
        if color_scheme in built_ins:
            return True

        # Check for JSON file in color_schemes directory
        scheme_file = Path("color_schemes") / f"{color_scheme}.json"
        if scheme_file.exists():
            return True

        return False

    def get_all_available_schemes(self):
        """Get all available color schemes from all sources"""
        schemes = ["default_professional", "corporate_blue", "modern_tech"]

        # Add schemes from color_schemes directory
        schemes_dir = Path("color_schemes")
        if schemes_dir.exists():
            for scheme_file in schemes_dir.glob("*.json"):
                scheme_name = scheme_file.stem
                if scheme_name not in schemes:
                    schemes.append(scheme_name)

        return schemes

    def check_setup(self):
        """Check if the system is properly set up"""
        print("🔍 Checking system setup...")

        # Check required files
        required_files = ["resume_data_generator.py", "reportlab_resume.py"]
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

    def generate_data(self, color_scheme="default_professional"):
        """Generate resume data using your existing generator"""
        print(f"📝 Generating resume data with {color_scheme} color scheme...")

        success, output = self.run_command(
            f"python resume_data_generator.py --color-scheme {color_scheme}"
        )

        if success:
            print("✅ Resume data generated")
            self.current_color_scheme = color_scheme
            return True
        else:
            print(f"❌ Failed to generate resume data")
            print(f"Error: {output}")
            return False

    def generate_single_resume(self, version_key, format_type="pdf", color_scheme=None):
        """Generate a single resume version with color scheme organization"""
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

        # Determine color scheme to use
        if color_scheme is None:
            color_scheme = self.get_current_color_scheme()

        print(
            f"📄 Generating {version_key} resume in {format_type.upper()} format with {color_scheme} colors..."
        )

        # Create color-scheme-organized output directory
        output_base = Path("outputs") / version_key / color_scheme / format_type
        output_base.mkdir(parents=True, exist_ok=True)

        # Generate with custom output path
        output_file = output_base / self.user_config.get_output_filename(
            version_key, color_scheme, format_type
        )
        cmd = f"python reportlab_resume.py --format {format_type} --basename {version_name} --output-dir outputs_temp"

        success, output = self.run_command(cmd)

        if success:
            # Move from temp location to organized location
            temp_file = Path(
                f"outputs_temp/{version_name}/{format_type}/{version_name}.{format_type}"
            )
            if temp_file.exists():
                import shutil

                shutil.move(str(temp_file), str(output_file))
                # Clean up temp directory
                shutil.rmtree("outputs_temp", ignore_errors=True)
                print(f"✅ Generated: {output_file}")
                return True
            else:
                print(f"❌ Expected file not found: {temp_file}")
                return False
        else:
            print(f"❌ Failed to generate {version_key} resume")
            print(f"Error: {output}")
            return False

    def generate_all_formats(self, version_key, color_scheme=None):
        """Generate all formats for a single version with color scheme organization"""
        if version_key not in self.versions:
            print(f"❌ Unknown version: {version_key}")
            return False

        if color_scheme is None:
            color_scheme = self.get_current_color_scheme()

        print(
            f"🚀 Generating all formats for {version_key} with {color_scheme} colors..."
        )

        success_count = 0
        for fmt in self.formats:
            if self.generate_single_resume(version_key, fmt, color_scheme):
                success_count += 1

        print(
            f"✅ Generated {success_count}/{len(self.formats)} formats for {version_key}"
        )
        return success_count == len(self.formats)

    def generate_color_comparison(self, version_key, color_schemes, format_type="pdf"):
        """Generate the same resume version with multiple color schemes for comparison"""
        if version_key not in self.versions:
            print(f"❌ Unknown version: {version_key}")
            return False

        print(
            f"🎨 Generating {version_key} resume with multiple color schemes for comparison..."
        )

        successful_schemes = []

        for scheme in color_schemes:
            print(f"\n📄 Generating with {scheme} colors...")

            # Generate data with this color scheme
            success, _ = self.run_command(
                f"python resume_data_generator.py --color-scheme {scheme}"
            )
            if not success:
                print(f"⚠️  Could not generate data with {scheme} scheme")
                continue

            # Generate resume with this scheme
            if self.generate_single_resume(version_key, format_type, scheme):
                successful_schemes.append(scheme)

        print(
            f"\n🎉 Generated {version_key} resume with {len(successful_schemes)} color schemes:"
        )
        for scheme in successful_schemes:
            output_path = (
                Path("outputs")
                / version_key
                / scheme
                / format_type
                / self.user_config.get_output_filename(version_key, scheme, format_type)
            )
            print(f"   📂 {output_path}")

        return len(successful_schemes) > 0

    def generate_all_versions(self, format_type="pdf"):
        """Generate all versions in specified format with current color scheme"""
        print(f"🚀 Generating all resume versions in {format_type.upper()} format...")

        current_scheme = self.get_current_color_scheme()
        success_count = 0
        failed_versions = []

        for version_key in self.versions.keys():
            if self.generate_single_resume(version_key, format_type, current_scheme):
                success_count += 1
            else:
                failed_versions.append(version_key)

        print(f"✅ Generated {success_count}/{len(self.versions)} versions")

        if failed_versions:
            print(f"❌ Failed versions: {', '.join(failed_versions)}")

        return len(failed_versions) == 0

    def generate_everything(self):
        """Generate all versions in all formats with current color scheme"""
        print("🚀 Generating ALL resume versions in ALL formats...")
        print("This may take a few minutes...")
        print()

        current_scheme = self.get_current_color_scheme()
        total_generated = 0
        total_possible = len(self.versions) * len(self.formats)

        for version_key in self.versions.keys():
            print(f"📋 Processing {version_key} with {current_scheme} colors...")
            for fmt in self.formats:
                if self.generate_single_resume(version_key, fmt, current_scheme):
                    total_generated += 1

        print()
        print(
            f"🎉 Generation complete: {total_generated}/{total_possible} files generated"
        )

        return total_generated

    def generate_nuclear_option(self):
        """Generate EVERY version in EVERY format with EVERY color scheme - The Nuclear Option"""
        available_schemes = self.get_all_available_schemes()
        total_combinations = (
            len(self.versions) * len(self.formats) * len(available_schemes)
        )

        print("☢️  NUCLEAR OPTION: Generating EVERYTHING")
        print("=" * 60)
        print(
            f"📊 Total combinations: {len(self.versions)} versions × {len(self.formats)} formats × {len(available_schemes)} color schemes"
        )
        print(f"🎯 Total files to generate: {total_combinations}")
        print()
        print("⏰ This will take several minutes...")
        print("☕ Perfect time for a coffee break!")
        print()

        # Confirm the nuclear option
        response = input(
            "🤔 Are you sure you want to generate ALL resumes with ALL color schemes? (y/N): "
        )
        if response.lower() != "y":
            print("❌ Nuclear option cancelled - probably wise!")
            return 0

        print("\n🚀 Launching nuclear generation sequence...")
        print("=" * 60)

        total_generated = 0
        total_failed = 0
        scheme_progress = 0

        for scheme in available_schemes:
            scheme_progress += 1
            print(
                f"\n🎨 Color Scheme {scheme_progress}/{len(available_schemes)}: {scheme}"
            )
            print("─" * 40)

            # Generate data for this color scheme
            success, _ = self.run_command(
                f"python resume_data_generator.py --color-scheme {scheme}"
            )
            if not success:
                print(f"⚠️  Failed to generate data for {scheme} scheme - skipping")
                total_failed += len(self.versions) * len(self.formats)
                continue

            scheme_generated = 0
            for version_key in self.versions.keys():
                print(f"  📄 {version_key}:", end=" ")
                version_success = 0

                for fmt in self.formats:
                    if self.generate_single_resume(version_key, fmt, scheme):
                        total_generated += 1
                        scheme_generated += 1
                        version_success += 1
                        print(f"{fmt.upper()}✅", end=" ")
                    else:
                        total_failed += 1
                        print(f"{fmt.upper()}❌", end=" ")

                print(f"({version_success}/{len(self.formats)})")

            print(
                f"  🎯 Scheme total: {scheme_generated}/{len(self.versions) * len(self.formats)} files"
            )

        print(f"\n☢️  NUCLEAR GENERATION COMPLETE!")
        print("=" * 60)
        print(f"✅ Successfully generated: {total_generated} files")
        print(f"❌ Failed: {total_failed} files")
        print(f"📊 Success rate: {(total_generated/total_combinations)*100:.1f}%")
        print()
        print(f"📁 Find your nuclear arsenal in the outputs/ directory!")
        print(f"   Organized by: outputs/[version]/[color_scheme]/[format]/")
        print(
            f"   Files named: {self.user_config.file_base_name}_[version]_[color_scheme].[extension]"
        )

        return total_generated

    def list_versions(self):
        """List available resume versions with color scheme status"""
        print("📋 Available resume versions:")
        print()

        descriptions = {
            "research": "Research & Data Analytics Leader - For academic/research roles",
            "technical": "Senior Geospatial Data Engineer - Technical depth emphasis",
            "comprehensive": "Complete work history - All details included",
            "consulting": "Data Analytics & Technology Consultant - Strategic advisor",
            "software": "Senior Software Engineer - Platform development (DEFAULT)",
            "marketing": "Senior Product Marketing Manager - Go-to-market focus",
        }

        current_scheme = self.get_current_color_scheme()
        print(f"🎨 Current color scheme: {current_scheme}")
        print()

        for key, description in descriptions.items():
            version_name = self.versions[key]
            input_dir = Path("inputs") / version_name
            status = "✅" if input_dir.exists() else "❌"

            # Check for existing outputs with current color scheme
            output_dir = Path("outputs") / key / current_scheme
            has_outputs = (
                "📄" if output_dir.exists() and any(output_dir.rglob("*")) else "  "
            )

            print(f"  {status} {has_outputs} {key:12} - {description}")

        print()
        print("🎨 Available color schemes:")
        schemes_dir = Path("color_schemes")
        if schemes_dir.exists():
            for scheme_file in schemes_dir.glob("*.json"):
                scheme_name = scheme_file.stem
                current_marker = " (CURRENT)" if scheme_name == current_scheme else ""
                print(f"  • {scheme_name}{current_marker}")
        else:
            for scheme in self.color_schemes:
                current_marker = " (CURRENT)" if scheme == current_scheme else ""
                print(f"  • {scheme}{current_marker}")

    def clean_outputs(self, version_key=None, color_scheme=None):
        """Clean output directories with optional filtering"""
        if version_key and color_scheme:
            # Clean specific version and color scheme
            target_dir = Path("outputs") / version_key / color_scheme
            if target_dir.exists():
                import shutil

                shutil.rmtree(target_dir)
                print(
                    f"✅ Cleaned {version_key} outputs for {color_scheme} color scheme"
                )
            else:
                print(f"ℹ️  No outputs found for {version_key} with {color_scheme}")
        elif version_key:
            # Clean all color schemes for a version
            target_dir = Path("outputs") / version_key
            if target_dir.exists():
                import shutil

                shutil.rmtree(target_dir)
                print(f"✅ Cleaned all outputs for {version_key}")
            else:
                print(f"ℹ️  No outputs found for {version_key}")
        else:
            # Clean everything
            outputs_dir = Path("outputs")
            if outputs_dir.exists():
                import shutil

                shutil.rmtree(outputs_dir)
                print("✅ Cleaned all output directories")
            else:
                print("ℹ️  No output directories to clean")


def get_available_color_schemes():
    """Get list of available color schemes from files and built-ins"""
    schemes = ["default_professional", "corporate_blue", "modern_tech"]  # Built-ins

    # Add schemes from color_schemes directory
    schemes_dir = Path("color_schemes")
    if schemes_dir.exists():
        for scheme_file in schemes_dir.glob("*.json"):
            scheme_name = scheme_file.stem
            if scheme_name not in schemes:
                schemes.append(scheme_name)

    return schemes


def main():
    """Main function with argument parsing"""

    # Get available color schemes dynamically for help text
    available_schemes = get_available_color_schemes()

    parser = argparse.ArgumentParser(
        description="Professional Resume Manager - Generate individual or batch resumes with color scheme organization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  # Setup and generate data
  python resume_manager.py --generate-data

  # Generate single resume (uses current color scheme)
  python resume_manager.py --version software --format pdf

  # Generate with specific color scheme
  python resume_manager.py --version technical --format pdf --color-scheme cartographic_professional

  # Generate all formats for one version
  python resume_manager.py --version technical --all-formats

  # Compare same resume with different color schemes
  python resume_manager.py --version software --color-comparison corporate_blue modern_tech cartographic_professional

  # Generate all versions in PDF
  python resume_manager.py --all-versions --format pdf

  # Generate all versions/formats with current color scheme
  python resume_manager.py --everything

  # ☢️  NUCLEAR OPTION: Generate EVERYTHING with EVERY color scheme
  python resume_manager.py --nuclear

  # List available versions and current color scheme
  python resume_manager.py --list

Available color schemes: {', '.join(available_schemes)}
        """,
    )

    # Data generation
    parser.add_argument(
        "--generate-data",
        action="store_true",
        help="Generate resume data files using existing generator",
    )
    parser.add_argument(
        "--color-scheme",
        help=f'Color scheme to use. Available: {", ".join(available_schemes)} (or any custom scheme in color_schemes/)',
    )

    # Single resume generation
    parser.add_argument(
        "--version",
        choices=[
            "research",
            "technical",
            "comprehensive",
            "consulting",
            "software",
            "marketing",
        ],
        help="Resume version to generate",
    )
    parser.add_argument(
        "--format",
        choices=["pdf", "docx", "rtf"],
        default="pdf",
        help="Output format (default: pdf)",
    )

    # Color comparison
    parser.add_argument(
        "--color-comparison",
        nargs="+",
        metavar="COLOR_SCHEME",
        help="Generate version with multiple color schemes for comparison",
    )

    # Batch operations
    parser.add_argument(
        "--all-formats",
        action="store_true",
        help="Generate all formats for specified version",
    )
    parser.add_argument(
        "--all-versions",
        action="store_true",
        help="Generate all versions in specified format",
    )
    parser.add_argument(
        "--everything",
        action="store_true",
        help="Generate all versions in all formats (current color scheme)",
    )
    parser.add_argument(
        "--nuclear",
        action="store_true",
        help="☢️  NUCLEAR OPTION: Generate EVERY version in EVERY format with EVERY color scheme",
    )

    # Utility
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available resume versions and color schemes",
    )
    parser.add_argument(
        "--clean",
        nargs="*",
        metavar="VERSION_OR_SCHEME",
        help="Clean output directories (optional: specify version and/or color scheme)",
    )
    parser.add_argument("--check", action="store_true", help="Check system setup")

    args = parser.parse_args()

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    manager = ResumeManager()

    # Validate color scheme if provided
    if args.color_scheme and not manager.validate_color_scheme(args.color_scheme):
        available = manager.get_all_available_schemes()
        print(f"❌ Color scheme '{args.color_scheme}' not found.")
        print(f"Available schemes: {', '.join(available)}")
        print(f"Generate custom schemes with: python color_scheme_generator_tool.py")
        return 1

    # Check system setup
    if args.check:
        success = manager.check_setup()
        return 0 if success else 1

    # List versions
    if args.list:
        manager.list_versions()
        return 0

    # Clean outputs
    if args.clean is not None:
        if len(args.clean) == 0:
            manager.clean_outputs()
        elif len(args.clean) == 1:
            manager.clean_outputs(version_key=args.clean[0])
        elif len(args.clean) == 2:
            manager.clean_outputs(version_key=args.clean[0], color_scheme=args.clean[1])
        else:
            print("❌ Clean accepts 0, 1, or 2 arguments: [version] [color_scheme]")
            return 1
        return 0

    # Generate data
    if args.generate_data:
        color_scheme = args.color_scheme or "default_professional"
        success = manager.generate_data(color_scheme)
        return 0 if success else 1

    # Color comparison
    if args.color_comparison:
        if not args.version:
            print("❌ --version required for color comparison")
            return 1
        success = manager.generate_color_comparison(
            args.version, args.color_comparison, args.format
        )
        return 0 if success else 1

    # Generate everything
    if args.everything:
        if not manager.check_setup():
            return 1
        total = manager.generate_everything()
        return 0 if total > 0 else 1

    # Nuclear option - generate everything with every color scheme
    if args.nuclear:
        if not manager.check_setup():
            return 1
        total = manager.generate_nuclear_option()
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
            success = manager.generate_all_formats(args.version, args.color_scheme)
        else:
            success = manager.generate_single_resume(
                args.version, args.format, args.color_scheme
            )

        return 0 if success else 1

    # If we reach here, no valid operation was specified
    print("❌ No operation specified. Use --help to see available options.")
    return 1


if __name__ == "__main__":
    exit(main())
