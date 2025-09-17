#!/usr/bin/env python3
"""
Generate human-friendly resume versions
"""

import sys
import os
sys.path.append('.')

from resumes.core_services import ResumeManager

def main():
    manager = ResumeManager()
    
    # Generate human-friendly versions for comprehensive resume
    print("Generating human-friendly comprehensive resumes...")
    
    # Generate all formats for comprehensive resume
    for color_scheme in manager.color_schemes:
        for format_type in manager.formats:
            for length_variant in manager.length_variants:
                success = manager.generate_single_resume(
                    version="comprehensive",
                    color_scheme=color_scheme,
                    format_type=format_type,
                    output_dir="outputs",
                    length_variant=length_variant,
                    output_type="human"
                )
                if success:
                    print(f"✓ Generated comprehensive {length_variant} {color_scheme} {format_type}")
                else:
                    print(f"✗ Failed to generate comprehensive {length_variant} {color_scheme} {format_type}")

if __name__ == "__main__":
    main()
