#!/usr/bin/env python3
"""
Professional Color Scheme Generator for Resume System
Generates color schemes based on industry, brand colors, or color theory
"""

import json
import colorsys
from pathlib import Path
import argparse

class ColorSchemeGenerator:
    """Generate professional color schemes for resumes"""

    def __init__(self):
        self.base_template = {
            'NAME_COLOR': '#000000',
            'TITLE_COLOR': '#000000',
            'SECTION_HEADER_COLOR': '#000000',
            'JOB_TITLE_COLOR': '#000000',
            'ACCENT_COLOR': '#000000',
            'COMPETENCY_HEADER_COLOR': '#000000',
            'SUBTITLE_COLOR': '#000000',
            'LINK_COLOR': '#000000',
            'DARK_TEXT_COLOR': '#333333',
            'MEDIUM_TEXT_COLOR': '#666666',
            'LIGHT_TEXT_COLOR': '#999999',

            # Typography and layout remain constant
            'FONT_MAIN': 'Helvetica',
            'FONT_BOLD': 'Helvetica-Bold',
            'FONT_ITALIC': 'Helvetica-Oblique',
            'NAME_SIZE': 24,
            'TITLE_SIZE': 14,
            'SECTION_HEADER_SIZE': 12,
            'JOB_TITLE_SIZE': 11,
            'BODY_SIZE': 9,
            'CONTACT_SIZE': 9,
            'PAGE_MARGIN': 0.6,
            'SECTION_SPACING': 0.12,
            'PARAGRAPH_SPACING': 0.06,
            'LINE_SPACING': 1.15,
            'JOB_SPACING': 6,
            'CATEGORY_SPACING': 4,
            'MAX_PAGES': 2,
            'BULLET_CHAR': '▸'
        }

    def hex_to_hsl(self, hex_color):
        """Convert hex color to HSL"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = r/255.0, g/255.0, b/255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h*360, s*100, l*100

    def hex_to_rgb_tuple(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def color_swatch(self, hex_color, width=4):
        """Create a colored terminal swatch for the color"""
        r, g, b = self.hex_to_rgb_tuple(hex_color)
        # ANSI escape codes for 24-bit color
        color_bg = f"\033[48;2;{r};{g};{b}m"
        reset = "\033[0m"
        return f"{color_bg}{' ' * width}{reset}"

    def hsl_to_hex(self, h, s, l):
        """Convert HSL to hex color"""
        h, s, l = h/360.0, s/100.0, l/100.0
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

    def adjust_lightness(self, hex_color, factor):
        """Adjust the lightness of a color"""
        h, s, l = self.hex_to_hsl(hex_color)
        l = max(0, min(100, l * factor))
        return self.hsl_to_hex(h, s, l)

    def adjust_saturation(self, hex_color, factor):
        """Adjust the saturation of a color"""
        h, s, l = self.hex_to_hsl(hex_color)
        s = max(0, min(100, s * factor))
        return self.hsl_to_hex(h, s, l)

    def get_complementary(self, hex_color):
        """Get complementary color"""
        h, s, l = self.hex_to_hsl(hex_color)
        h = (h + 180) % 360
        return self.hsl_to_hex(h, s, l)

    def get_analogous(self, hex_color, offset=30):
        """Get analogous colors"""
        h, s, l = self.hex_to_hsl(hex_color)
        h1 = (h + offset) % 360
        h2 = (h - offset) % 360
        return self.hsl_to_hex(h1, s, l), self.hsl_to_hex(h2, s, l)

    def get_triadic(self, hex_color):
        """Get triadic colors"""
        h, s, l = self.hex_to_hsl(hex_color)
        h1 = (h + 120) % 360
        h2 = (h + 240) % 360
        return self.hsl_to_hex(h1, s, l), self.hsl_to_hex(h2, s, l)

    def generate_monochromatic_scheme(self, base_color, scheme_name):
        """Generate monochromatic color scheme from base color"""
        scheme = self.base_template.copy()

        # Use base color for primary elements
        scheme['NAME_COLOR'] = base_color
        scheme['COMPETENCY_HEADER_COLOR'] = base_color
        scheme['SUBTITLE_COLOR'] = base_color

        # Lighter version for secondary elements
        lighter = self.adjust_lightness(base_color, 1.3)
        scheme['TITLE_COLOR'] = lighter
        scheme['SECTION_HEADER_COLOR'] = lighter
        scheme['LINK_COLOR'] = lighter

        # Slightly different hue for job titles
        analogous1, _ = self.get_analogous(base_color, 15)
        scheme['JOB_TITLE_COLOR'] = analogous1
        scheme['ACCENT_COLOR'] = analogous1

        return self.create_scheme_dict(scheme_name, scheme)

    def generate_complementary_scheme(self, base_color, scheme_name):
        """Generate complementary color scheme"""
        scheme = self.base_template.copy()

        complementary = self.get_complementary(base_color)

        # Primary color for main elements
        scheme['NAME_COLOR'] = base_color
        scheme['COMPETENCY_HEADER_COLOR'] = base_color
        scheme['SUBTITLE_COLOR'] = base_color

        # Complementary for secondary elements
        scheme['TITLE_COLOR'] = complementary
        scheme['SECTION_HEADER_COLOR'] = complementary
        scheme['LINK_COLOR'] = complementary

        # Muted version for job titles
        muted_comp = self.adjust_saturation(complementary, 0.7)
        scheme['JOB_TITLE_COLOR'] = muted_comp
        scheme['ACCENT_COLOR'] = muted_comp

        return self.create_scheme_dict(scheme_name, scheme)

    def generate_triadic_scheme(self, base_color, scheme_name):
        """Generate triadic color scheme"""
        scheme = self.base_template.copy()

        triadic1, triadic2 = self.get_triadic(base_color)

        # Use all three colors strategically
        scheme['NAME_COLOR'] = base_color
        scheme['COMPETENCY_HEADER_COLOR'] = base_color

        scheme['TITLE_COLOR'] = triadic1
        scheme['SECTION_HEADER_COLOR'] = triadic1
        scheme['LINK_COLOR'] = triadic1

        scheme['JOB_TITLE_COLOR'] = triadic2
        scheme['ACCENT_COLOR'] = triadic2
        scheme['SUBTITLE_COLOR'] = triadic2

        return self.create_scheme_dict(scheme_name, scheme)

    def generate_industry_scheme(self, industry, scheme_name):
        """Generate color scheme based on industry best practices"""
        industry_colors = {
            'finance': {
                'primary': '#1F4E79',    # Navy Blue
                'secondary': '#2E5090',  # Professional Blue
                'accent': '#5A7FA6'      # Steel Blue
            },
            'legal': {
                'primary': '#2C3E50',    # Dark Slate
                'secondary': '#34495E',  # Charcoal Blue
                'accent': '#5D6D7E'      # Gray Blue
            },
            'healthcare': {
                'primary': '#2E8B57',    # Sea Green
                'secondary': '#3CB371',  # Medium Sea Green
                'accent': '#20B2AA'      # Light Sea Green
            },
            'technology': {
                'primary': '#2C3E50',    # Dark Blue Gray
                'secondary': '#E74C3C',  # Modern Red
                'accent': '#3498DB'      # Bright Blue
            },
            'consulting': {
                'primary': '#8E44AD',    # Purple
                'secondary': '#F39C12',  # Orange
                'accent': '#2ECC71'      # Green
            },
            'creative': {
                'primary': '#E91E63',    # Pink
                'secondary': '#FF9800',  # Orange
                'accent': '#9C27B0'      # Purple
            },
            'education': {
                'primary': '#3F51B5',    # Indigo
                'secondary': '#FF9800',  # Orange
                'accent': '#4CAF50'      # Green
            },
            'nonprofit': {
                'primary': '#4CAF50',    # Green
                'secondary': '#FF9800',  # Orange
                'accent': '#2196F3'      # Blue
            }
        }

        if industry.lower() not in industry_colors:
            raise ValueError(f"Industry '{industry}' not supported. Available: {list(industry_colors.keys())}")

        colors = industry_colors[industry.lower()]
        scheme = self.base_template.copy()

        scheme['NAME_COLOR'] = colors['primary']
        scheme['COMPETENCY_HEADER_COLOR'] = colors['primary']
        scheme['SUBTITLE_COLOR'] = colors['primary']

        scheme['TITLE_COLOR'] = colors['secondary']
        scheme['SECTION_HEADER_COLOR'] = colors['secondary']
        scheme['LINK_COLOR'] = colors['secondary']

        scheme['JOB_TITLE_COLOR'] = colors['accent']
        scheme['ACCENT_COLOR'] = colors['accent']

        return self.create_scheme_dict(f"{industry}_{scheme_name}", scheme)

    def generate_brand_scheme(self, brand_colors, scheme_name):
        """Generate scheme from brand colors (list of 2-3 hex colors)"""
        if len(brand_colors) < 2:
            raise ValueError("Need at least 2 brand colors")

        scheme = self.base_template.copy()

        # Primary brand color for main elements
        scheme['NAME_COLOR'] = brand_colors[0]
        scheme['COMPETENCY_HEADER_COLOR'] = brand_colors[0]
        scheme['SUBTITLE_COLOR'] = brand_colors[0]

        # Secondary brand color
        scheme['TITLE_COLOR'] = brand_colors[1]
        scheme['SECTION_HEADER_COLOR'] = brand_colors[1]
        scheme['LINK_COLOR'] = brand_colors[1]

        # Third color or muted version of first
        if len(brand_colors) >= 3:
            scheme['JOB_TITLE_COLOR'] = brand_colors[2]
            scheme['ACCENT_COLOR'] = brand_colors[2]
        else:
            muted = self.adjust_saturation(brand_colors[0], 0.7)
            scheme['JOB_TITLE_COLOR'] = muted
            scheme['ACCENT_COLOR'] = muted

        return self.create_scheme_dict(f"brand_{scheme_name}", scheme)

    def create_scheme_dict(self, scheme_name, scheme):
        """Create properly formatted scheme dictionary"""
        color_keys = [k for k in scheme.keys() if k.endswith('_COLOR')]
        typography_keys = ['FONT_MAIN', 'FONT_BOLD', 'FONT_ITALIC', 'NAME_SIZE', 'TITLE_SIZE', 'SECTION_HEADER_SIZE', 'JOB_TITLE_SIZE', 'BODY_SIZE', 'CONTACT_SIZE']

        # Create clean dictionary structure
        result = {}

        # Add all color properties directly to result (for compatibility with existing system)
        for key, value in scheme.items():
            if key.endswith('_COLOR') or key in typography_keys or key in ['PAGE_MARGIN', 'SECTION_SPACING', 'PARAGRAPH_SPACING', 'LINE_SPACING', 'JOB_SPACING', 'CATEGORY_SPACING', 'MAX_PAGES', 'BULLET_CHAR']:
                result[key] = value

        # Add metadata
        result['_metadata'] = {
            'scheme_name': scheme_name,
            'description': f'{scheme_name} color scheme for professional resume',
            'generated': True
        }

        return result

    def save_scheme(self, scheme_dict, output_dir="color_schemes"):
        """Save color scheme to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        filename = f"{scheme_dict['_metadata']['scheme_name']}.json"
        filepath = output_path / filename

        with open(filepath, 'w') as f:
            json.dump(scheme_dict, f, indent=2)

        print(f"✅ Saved color scheme: {filepath}")
        return filepath

    def preview_scheme(self, scheme_dict):
        """Print a preview of the color scheme with actual colors AND hex codes"""
        print(f"\n🎨 Color Scheme: {scheme_dict['_metadata']['scheme_name']}")
        print("=" * 60)

        # Get color properties directly from scheme_dict
        color_properties = {k: v for k, v in scheme_dict.items() if k.endswith('_COLOR')}

        print("Color Roles:")
        for role, color in color_properties.items():
            role_name = role.replace('_COLOR', '').replace('_', ' ').title()
            swatch = self.color_swatch(color)
            print(f"  {role_name:20} {swatch} {color}")

        print("\nUsage Preview:")
        name_color = color_properties.get('NAME_COLOR', '#000000')
        title_color = color_properties.get('TITLE_COLOR', '#000000')
        section_color = color_properties.get('SECTION_HEADER_COLOR', '#000000')
        job_color = color_properties.get('JOB_TITLE_COLOR', '#000000')
        link_color = color_properties.get('LINK_COLOR', '#000000')

        print(f"  NAME (Header):        {self.color_swatch(name_color)} {name_color}")
        print(f"  TITLE (Subtitle):     {self.color_swatch(title_color)} {title_color}")
        print(f"  SECTIONS (Headers):   {self.color_swatch(section_color)} {section_color}")
        print(f"  JOB TITLES:           {self.color_swatch(job_color)} {job_color}")
        print(f"  LINKS (Website):      {self.color_swatch(link_color)} {link_color}")

        # Show a mockup of how it might look on a resume
        print(f"\n📄 Resume Preview:")
        print("   " + "─" * 50)

        # Name with actual color
        name_r, name_g, name_b = self.hex_to_rgb_tuple(name_color)
        name_fg = f"\033[38;2;{name_r};{name_g};{name_b}m"
        reset = "\033[0m"
        print(f"   {name_fg}DHEERAJ CHAND{reset}")

        # Title with actual color
        title_r, title_g, title_b = self.hex_to_rgb_tuple(title_color)
        title_fg = f"\033[38;2;{title_r};{title_g};{title_b}m"
        print(f"   {title_fg}Senior Software Engineer{reset}")

        print("   (202) 550-7110 | Dheeraj.Chand@gmail.com")

        # Section header example
        section_r, section_g, section_b = self.hex_to_rgb_tuple(section_color)
        section_fg = f"\033[38;2;{section_r};{section_g};{section_b}m"
        print(f"\n   {section_fg}PROFESSIONAL EXPERIENCE{reset}")

        # Job title example
        job_r, job_g, job_b = self.hex_to_rgb_tuple(job_color)
        job_fg = f"\033[38;2;{job_r};{job_g};{job_b}m"
        print(f"   {job_fg}PARTNER & SENIOR SOFTWARE ENGINEER{reset}")
        print("   Siege Analytics, Austin, TX | 2005 – Present")

        print("   " + "─" * 50)

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Generate professional color schemes for resumes')

    # Generation methods
    method_group = parser.add_mutually_exclusive_group(required=True)
    method_group.add_argument('--monochromatic', metavar='HEX_COLOR',
                             help='Generate monochromatic scheme from base color (e.g., #228B22)')
    method_group.add_argument('--complementary', metavar='HEX_COLOR',
                             help='Generate complementary scheme from base color')
    method_group.add_argument('--triadic', metavar='HEX_COLOR',
                             help='Generate triadic scheme from base color')
    method_group.add_argument('--industry', choices=['finance', 'legal', 'healthcare', 'technology', 'consulting', 'creative', 'education', 'nonprofit'],
                             help='Generate industry-appropriate scheme')
    method_group.add_argument('--brand', nargs='+', metavar='HEX_COLOR',
                             help='Generate scheme from brand colors (2-3 hex colors)')

    # Options
    parser.add_argument('--name', required=True,
                       help='Name for the color scheme')
    parser.add_argument('--output-dir', default='color_schemes',
                       help='Output directory for color scheme files')
    parser.add_argument('--preview', action='store_true',
                       help='Show color preview before saving')

    args = parser.parse_args()

    generator = ColorSchemeGenerator()
    scheme_dict = None

    try:
        if args.monochromatic:
            scheme_dict = generator.generate_monochromatic_scheme(args.monochromatic, args.name)
        elif args.complementary:
            scheme_dict = generator.generate_complementary_scheme(args.complementary, args.name)
        elif args.triadic:
            scheme_dict = generator.generate_triadic_scheme(args.triadic, args.name)
        elif args.industry:
            scheme_dict = generator.generate_industry_scheme(args.industry, args.name)
        elif args.brand:
            scheme_dict = generator.generate_brand_scheme(args.brand, args.name)

        if scheme_dict:
            if args.preview:
                generator.preview_scheme(scheme_dict)
                response = input("\n💾 Save this color scheme? (y/N): ")
                if response.lower() != 'y':
                    print("❌ Color scheme not saved")
                    return

            filepath = generator.save_scheme(scheme_dict, args.output_dir)

            print(f"\n🚀 To use this color scheme:")
            print(f"   python resume_manager.py --generate-data --color-scheme {args.name}")
            print(f"   python resume_manager.py --version software --format pdf")

    except Exception as e:
        print(f"❌ Error generating color scheme: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
