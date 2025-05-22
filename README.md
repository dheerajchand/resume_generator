# Professional Resume Generator

A Python-based resume generator using ReportLab that creates professional, multi-format resumes with precise control over layout, styling, and content. Generates PDF, DOCX, and RTF formats from a single source.

## Features

- 🎨 **Professional Styling**: Clean, modern design with customizable colors and fonts
- 📄 **Multiple Formats**: PDF (ReportLab), DOCX (Word), RTF (Pages-compatible)
- ⚙️ **Highly Configurable**: JSON-based configuration for easy customization
- 📏 **Optimized Layout**: Designed for 2-page target with efficient spacing
- 🔧 **Modular Content**: Easy to update content without touching formatting code
- 🎯 **ATS-Friendly**: Clean structure that works well with applicant tracking systems

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-generator.git
cd resume-generator

# Install required dependencies
pip install reportlab

# Optional: Install for additional formats
pip install python-docx
```

### Basic Usage

```bash
# Generate PDF (default)
python reportlab_resume.py

# Generate Word document
python reportlab_resume.py --format docx

# Generate all formats
python reportlab_resume.py --format all

# Custom filename
python reportlab_resume.py --format pdf --basename john_doe_resume
```

## Configuration

The script automatically creates a `resume_config.json` file on first run with customizable settings:

```json
{
  "PRIMARY_GREEN": "#228B22",
  "SECONDARY_GOLD": "#B8860B",
  "FONT_MAIN": "Helvetica",
  "NAME_SIZE": 24,
  "BODY_SIZE": 9,
  "PAGE_MARGIN": 54.0,
  "MAX_PAGES": 2
}
```

### Color Scheme

- **Primary Green** (#228B22): Name and accent elements
- **Secondary Gold** (#B8860B): Section headers and job titles
- Clean, professional appearance suitable for any industry

## Customization

### Updating Content

Edit the `ResumeData` class in the script to update:

- **Personal Information**: Name, contact details, links
- **Professional Summary**: Career overview and key strengths
- **Core Competencies**: Skills organized by category
- **Professional Experience**: Jobs, responsibilities, achievements
- **Key Achievements**: Notable accomplishments and impact

### Styling Options

Modify `ResumeConfig` class or edit `resume_config.json`:

- **Colors**: Hex color codes for all elements
- **Fonts**: Font families and sizes
- **Spacing**: Margins, line spacing, section spacing
- **Layout**: Page margins, bullet characters

## Output Formats

### PDF (ReportLab)
- **Best for**: Final submissions, printing, precise formatting
- **Features**: Exact layout control, consistent rendering
- **File size**: Compact, professional quality

### DOCX (Word)
- **Best for**: Editing, collaboration, ATS systems
- **Features**: Editable format, maintains styling
- **Compatibility**: Microsoft Word, Google Docs, most HR systems

### RTF (Rich Text Format)
- **Best for**: Cross-platform compatibility, Pages conversion
- **Features**: Opens in most word processors
- **Use case**: Convert to Apple Pages format

## Command Line Options

```bash
python reportlab_resume.py [OPTIONS]

Options:
  --format {pdf,docx,rtf,all}  Output format (default: pdf)
  --basename TEXT              Base filename (default: dheeraj_chand_resume)
  --help                       Show help message
```

## Examples

```bash
# Generate PDF only
python reportlab_resume.py

# Generate Word document for ATS systems
python reportlab_resume.py --format docx

# Generate all formats for maximum compatibility
python reportlab_resume.py --format all

# Create custom-named files
python reportlab_resume.py --format all --basename jane_smith_resume
```

## File Structure

```
resume-generator/
├── reportlab_resume.py      # Main script
├── resume_config.json       # Configuration (auto-generated)
├── README.md               # This file
└── output/                 # Generated resumes (optional)
    ├── resume.pdf
    ├── resume.docx
    └── resume.rtf
```

## Dependencies

### Required
- **Python 3.7+**
- **ReportLab**: PDF generation
  ```bash
  pip install reportlab
  ```

### Optional
- **python-docx**: Word document generation
  ```bash
  pip install python-docx
  ```

## Use Cases

### Job Applications
- Generate PDF for online applications
- Use DOCX for ATS-friendly submissions
- Customize content for specific roles

### Different Industries
- Adjust color scheme for industry norms
- Modify content emphasis and keywords
- Maintain professional consistency

### Collaboration
- Share DOCX version for feedback
- Version control with Git
- Easy content updates

## Customization Examples

### Industry-Specific Color Schemes

**Tech/Creative**
```json
{
  "PRIMARY_GREEN": "#00A86B",
  "SECONDARY_GOLD": "#FF6B35"
}
```

**Finance/Legal**
```json
{
  "PRIMARY_GREEN": "#2F4F4F",
  "SECONDARY_GOLD": "#4169E1"
}
```

**Healthcare/Education**
```json
{
  "PRIMARY_GREEN": "#228B22",
  "SECONDARY_GOLD": "#8B4513"
}
```

### Font Customization

```json
{
  "FONT_MAIN": "Times-Roman",
  "FONT_BOLD": "Times-Bold",
  "FONT_ITALIC": "Times-Italic"
}
```

## Best Practices

### Content
- Keep bullet points concise and action-oriented
- Use quantifiable achievements where possible
- Tailor content for specific job applications
- Maintain consistent tense and style

### Formatting
- Test PDF output before final submission
- Use DOCX for collaborative editing
- Keep within 2-page target for most roles
- Ensure consistent spacing and alignment

### Version Control
- Commit configuration changes separately
- Use descriptive commit messages
- Tag versions for specific applications
- Keep master branch as your "base" resume

## Troubleshooting

### Common Issues

**Font not found**
- Stick to standard fonts (Helvetica, Times, Arial)
- Check font name spelling in config

**PDF too long**
- Reduce font sizes in config
- Tighten spacing settings
- Condense content

**DOCX formatting issues**
- Ensure python-docx is installed
- Colors may appear differently in Word
- Use RTF as fallback format

### Error Messages

**"Style already defined"**
- ReportLab style name conflict
- Restart Python session

**"Module not found"**
- Install missing dependencies
- Check Python environment

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-format`)
3. Make your changes
4. Test with different configurations
5. Submit a pull request

## License

MIT License - feel free to use and modify for personal and commercial use.

## Acknowledgments

- Built with [ReportLab](https://www.reportlab.com/) for PDF generation
- Uses [python-docx](https://python-docx.readthedocs.io/) for Word documents
- Inspired by modern resume design principles

---

**Note**: This generator was created for a research professional role but is easily adaptable for any industry or role type. Customize the content and styling to match your specific needs.
