#!/usr/bin/env python3
"""
Generate all resume versions (ATS and Human) for all resume types
"""

import sys
import os
sys.path.append('.')

from resumes.core_services import ResumeManager

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
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total generated: {total_generated}")
    print(f"Total failed: {total_failed}")
    print(f"Success rate: {(total_generated/(total_generated+total_failed)*100):.1f}%")

if __name__ == "__main__":
    main()
