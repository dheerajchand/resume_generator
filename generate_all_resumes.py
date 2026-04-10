#!/usr/bin/env python3
"""
Generate all resume versions (ATS and Human) for all resume types
"""

import sys
from pathlib import Path

sys.path.append('.')

from resumes.core_services import ResumeManager

GITHUB_BASE = "https://raw.githubusercontent.com/dheerajchand/resume_generator/main/outputs"

RESUME_TYPE_DISPLAY = {
    "comprehensive": ("Comprehensive", "Complete career overview showcasing the full breadth of experience across data science, software engineering, and political analytics."),
    "data_engineering": ("Data Engineering", "Data infrastructure focus: pipelines, warehouses, ETL, Databricks, and federated architectures."),
    "software_engineering": ("Software Engineering", "Software development expertise: full-stack systems, distributed computing, and production platforms."),
    "gis": ("GIS & Geospatial Analysis", "Mapping and spatial analysis: PostGIS, GDAL, custom tile servers, and geospatial ML."),
    "product": ("Product Management", "Business strategy focus: team leadership, platform development, and revenue generation."),
    "marketing": ("Marketing Analytics", "Data-driven marketing: consumer segmentation, testing, and optimization."),
    "data_analysis_visualization": ("Data Analysis & Visualization", "Data science specialization: ML algorithms, demographic analysis, and spatial visualization."),
    "polling_research_redistricting": ("Political Research & Redistricting", "Research and redistricting: survey methodology, electoral prediction, and demographic modeling."),
}

COLOR_SCHEMES = [
    "default_professional", "corporate_blue", "modern_tech", "modern_clean",
    "satellite_imagery", "terrain_mapping", "cartographic_professional", "topographic_classic"
]

PREFERRED_COLOR = {
    "comprehensive": "modern_tech",
    "data_engineering": "corporate_blue",
    "software_engineering": "satellite_imagery",
    "gis": "terrain_mapping",
    "product": "cartographic_professional",
    "marketing": "modern_clean",
    "data_analysis_visualization": "topographic_classic",
    "polling_research_redistricting": "default_professional",
}


def _get_resume_types_from_db():
    """Try to read archetype names/descriptions from Django DB. Falls back to hardcoded dict."""
    try:
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_generator_django.settings")
        django.setup()
        from portfolio.models import ResumeArchetype
        archetypes = ResumeArchetype.objects.all().order_by("name")
        if archetypes.exists():
            return {a.slug: (a.name, a.description or "") for a in archetypes}
    except Exception:
        pass
    return RESUME_TYPE_DISPLAY


def generate_output_readme(output_dir="outputs"):
    """Generate outputs/README.md with download links for all resume files.

    Reads archetype names and descriptions from the database if available,
    falling back to the hardcoded RESUME_TYPE_DISPLAY dict.
    """
    resume_types = _get_resume_types_from_db()

    lines = []
    lines.append("# Resume Portfolio - Complete Collection")
    lines.append("")
    lines.append("## QUICKNESS, TL/DR")
    lines.append("")
    lines.append("This is a selection of resumes I've made. For quick navigation, without browsing anything else, here are human-oriented, PDF formatted, longer form resumes oriented towards different roles:")
    lines.append("")
    for idx, (type_key, (display_name, _)) in enumerate(resume_types.items(), 1):
        color = PREFERRED_COLOR.get(type_key, "default_professional")
        url = f"{GITHUB_BASE}/human/{type_key}/long/{color}/pdf/dheeraj_chand_{type_key}_long_{color}.pdf"
        lines.append(f"{idx}. **[{display_name}]({url})** - {display_name}")
    lines.append("")
    lines.append("---")
    lines.append("")

    total = len(resume_types) * len(COLOR_SCHEMES) * 3 * 2 * 4  # types * colors * lengths * output_types * formats
    lines.append(f"**{total} professionally formatted resumes** systematically generated for different industries and use cases.")
    lines.append("")

    for type_key, (display_name, description) in resume_types.items():
        lines.append(f"## {display_name}")
        lines.append("")
        lines.append(description)
        lines.append("")

        for length in ["long", "short", "brief"]:
            lines.append(f"### {length.title()} Format")
            lines.append("")
            lines.append("| Color Scheme | PDF | DOCX | RTF | Markdown |")
            lines.append("|--------------|-----|------|-----|----------|")

            for scheme in COLOR_SCHEMES:
                scheme_display = scheme.replace("_", " ").title()
                fname_base = f"dheeraj_chand_{type_key}_{length}_{scheme}"

                pdf_ats = f"{GITHUB_BASE}/ats/{type_key}/{length}/{scheme}/pdf/{fname_base}.pdf"
                pdf_human = f"{GITHUB_BASE}/human/{type_key}/{length}/{scheme}/pdf/{fname_base}.pdf"
                docx_ats = f"{GITHUB_BASE}/ats/{type_key}/{length}/{scheme}/docx/{fname_base}.docx"
                docx_human = f"{GITHUB_BASE}/human/{type_key}/{length}/{scheme}/docx/{fname_base}.docx"
                rtf_ats = f"{GITHUB_BASE}/ats/{type_key}/{length}/{scheme}/rtf/{fname_base}.rtf"
                rtf_human = f"{GITHUB_BASE}/human/{type_key}/{length}/{scheme}/rtf/{fname_base}.rtf"
                md_view = f"{GITHUB_BASE}/human/{type_key}/{length}/{scheme}/md/{fname_base}.md"

                row = f"| **{scheme_display}** "
                row += f"| [ATS]({pdf_ats}) \\| [Human]({pdf_human}) "
                row += f"| [ATS]({docx_ats}) \\| [Human]({docx_human}) "
                row += f"| [ATS]({rtf_ats}) \\| [Human]({rtf_human}) "
                row += f"| [View]({md_view}) |"
                lines.append(row)

            lines.append("")

    readme_path = Path(output_dir) / "README.md"
    readme_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Generated: {readme_path}")


def main():
    manager = ResumeManager()

    # All resume types from the configuration
    resume_types = [
        "comprehensive",
        "data_engineering",
        "software_engineering",
        "gis",
        "product",
        "marketing",
        "data_analysis_visualization",
        "polling_research_redistricting"
    ]

    # All output types
    output_types = ["ats", "human"]

    total_generated = 0
    total_failed = 0

    for output_type in output_types:
        print(f"\n{'='*60}")
        print(f"Generating {output_type.upper()} resumes...")
        print(f"{'='*60}")

        for resume_type in resume_types:
            print(f"\nGenerating {output_type} {resume_type} resumes...")

            for color_scheme in manager.color_schemes:
                for format_type in manager.formats:
                    for length_variant in manager.length_variants:
                        success = manager.generate_single_resume(
                            version=resume_type,
                            color_scheme=color_scheme,
                            format_type=format_type,
                            output_dir="outputs",
                            length_variant=length_variant,
                            output_type=output_type
                        )
                        if success:
                            print(f"✓ Generated {output_type} {resume_type} {length_variant} {color_scheme} {format_type}")
                            total_generated += 1
                        else:
                            print(f"✗ Failed to generate {output_type} {resume_type} {length_variant} {color_scheme} {format_type}")
                            total_failed += 1

    print(f"\n{'='*60}")
    print("GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total generated: {total_generated}")
    print(f"Total failed: {total_failed}")
    print(f"Success rate: {(total_generated/(total_generated+total_failed)*100):.1f}%")

    # Generate the output links page
    generate_output_readme()

if __name__ == "__main__":
    main()
