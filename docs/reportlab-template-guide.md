# ReportLab Template Guide

## Overview

The Resume Generator uses ReportLab to create professional PDF resumes with customizable styling and color schemes. This guide explains how the template is built, how to modify it, and how the color system works.

## Template Architecture

### Core Components

The ReportLab template is built using several key components:

1. **Document Structure** - PDF document setup and page configuration
2. **Style System** - Paragraph styles for different content types
3. **Color Schemes** - Configurable color palettes
4. **Content Layout** - How different sections are arranged
5. **Typography** - Font choices and sizing

### Document Setup

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Document configuration
doc = SimpleDocTemplate(
    filename, 
    pagesize=letter,
    rightMargin=0.6*inch, 
    leftMargin=0.6*inch,
    topMargin=0.6*inch, 
    bottomMargin=0.6*inch
)
```

**Key Parameters:**
- `pagesize=letter` - Standard US letter size (8.5" x 11")
- `margins=0.6*inch` - Professional margins for readability
- `filename` - Output PDF file path

## Style System

### Paragraph Styles

The template uses a hierarchical style system with these main styles:

#### 1. Name Style
```python
"Name": ParagraphStyle(
    "CustomName",
    parent=styles["Heading1"],
    fontSize=24,
    textColor=HexColor(colors.get("NAME_COLOR", "#228B22")),
    alignment=TA_CENTER,
    spaceAfter=6,
)
```

**Purpose:** Main resume name/title
**Characteristics:**
- Large font (24pt)
- Centered alignment
- Custom color from scheme
- Green by default (#228B22)

#### 2. Title Style
```python
"Title": ParagraphStyle(
    "CustomTitle",
    parent=styles["Heading2"],
    fontSize=14,
    textColor=HexColor(colors.get("TITLE_COLOR", "#B8860B")),
    alignment=TA_CENTER,
    spaceAfter=12,
)
```

**Purpose:** Professional title/subtitle
**Characteristics:**
- Medium font (14pt)
- Centered alignment
- Gold color by default (#B8860B)

#### 3. Section Header Style
```python
"SectionHeader": ParagraphStyle(
    "CustomSectionHeader",
    parent=styles["Heading2"],
    fontSize=12,
    textColor=HexColor(colors.get("SECTION_HEADER_COLOR", "#B8860B")),
    spaceAfter=6,
    spaceBefore=12,
)
```

**Purpose:** Section titles (Experience, Education, etc.)
**Characteristics:**
- Medium font (12pt)
- Left aligned
- Spacing before and after
- Gold color by default

#### 4. Job Title Style
```python
"JobTitle": ParagraphStyle(
    "CustomJobTitle",
    parent=styles["Heading3"],
    fontSize=11,
    textColor=HexColor(colors.get("JOB_TITLE_COLOR", "#722F37")),
    spaceAfter=3,
)
```

**Purpose:** Individual job titles and project names
**Characteristics:**
- Smaller font (11pt)
- Dark red color (#722F37)
- Minimal spacing

#### 5. Body Text Style
```python
"Body": ParagraphStyle(
    "CustomBody",
    parent=styles["Normal"],
    fontSize=9,
    textColor=HexColor(colors.get("DARK_TEXT_COLOR", "#333333")),
    spaceAfter=3,
)
```

**Purpose:** Main content text
**Characteristics:**
- Small font (9pt) for space efficiency
- Dark gray color (#333333)
- Minimal spacing

#### 6. Contact Style
```python
"Contact": ParagraphStyle(
    "CustomContact",
    parent=styles["Normal"],
    fontSize=9,
    textColor=HexColor(colors.get("DARK_TEXT_COLOR", "#333333")),
    alignment=TA_CENTER,
    spaceAfter=6,
)
```

**Purpose:** Contact information
**Characteristics:**
- Centered alignment
- Same color as body text
- Slightly more spacing

## Color Scheme System

### Color Scheme Structure

Each color scheme is defined in a JSON file with these key color roles:

```json
{
  "NAME_COLOR": "#228B22",
  "TITLE_COLOR": "#B8860B", 
  "SECTION_HEADER_COLOR": "#B8860B",
  "JOB_TITLE_COLOR": "#722F37",
  "ACCENT_COLOR": "#722F37",
  "COMPETENCY_HEADER_COLOR": "#228B22",
  "SUBTITLE_COLOR": "#228B22",
  "LINK_COLOR": "#B8860B",
  "LIGHT_ACCENT_COLOR": "#8B4444",
  "LIGHT_SECONDARY_COLOR": "#DAA520",
  "DARK_TEXT_COLOR": "#333333",
  "MEDIUM_TEXT_COLOR": "#666666",
  "LIGHT_TEXT_COLOR": "#999999"
}
```

### Available Color Schemes

#### 1. Default Professional
- **Primary:** Forest Green (#228B22)
- **Secondary:** Dark Goldenrod (#B8860B)
- **Accent:** Dark Red (#722F37)
- **Best for:** Traditional corporate environments

#### 2. Corporate Blue
- **Primary:** Navy Blue (#1E3A8A)
- **Secondary:** Steel Blue (#4A90E2)
- **Accent:** Dark Blue (#1E40AF)
- **Best for:** Financial services, consulting

#### 3. Modern Tech
- **Primary:** Electric Blue (#0066CC)
- **Secondary:** Orange (#FF6B35)
- **Accent:** Dark Gray (#2C3E50)
- **Best for:** Technology companies, startups

#### 4. Satellite Imagery
- **Primary:** Earth Green (#2D5016)
- **Secondary:** Sky Blue (#87CEEB)
- **Accent:** Terracotta (#CD853F)
- **Best for:** Environmental, GIS, remote sensing

#### 5. Terrain Mapping
- **Primary:** Forest Green (#228B22)
- **Secondary:** Brown (#8B4513)
- **Accent:** Tan (#D2B48C)
- **Best for:** Cartography, geography, surveying

#### 6. Cartographic Professional
- **Primary:** Deep Blue (#003366)
- **Secondary:** Gold (#DAA520)
- **Accent:** Dark Green (#006400)
- **Best for:** GIS professionals, mapping

#### 7. Topographic Classic
- **Primary:** Dark Brown (#8B4513)
- **Secondary:** Light Brown (#D2B48C)
- **Accent:** Dark Green (#006400)
- **Best for:** Traditional mapping, geology

## Content Layout Structure

### 1. Header Section
```
[NAME] - Large, centered, primary color
[Contact Info] - Centered, separated by pipes
```

### 2. Professional Summary
```
PROFESSIONAL SUMMARY - Section header
[Summary text] - Body text
```

### 3. Core Competencies
```
CORE COMPETENCIES - Section header
Category: skill1 • skill2 • skill3 - Body text
```

### 4. Professional Experience
```
PROFESSIONAL EXPERIENCE - Section header
Job Title - Company (Location) | Dates - Job title style
Subtitle - Body text
• Responsibility 1 - Body text
• Responsibility 2 - Body text
```

### 5. Key Projects
```
KEY PROJECTS - Section header
Project Name (Dates) - Job title style
Description - Body text
Technologies: tech1, tech2 - Body text
Impact: impact statement - Body text
```

### 6. Education
```
EDUCATION - Section header
Degree - Institution (Location) | Dates - Job title style
GPA: 3.8 - Body text
Honors: Magna Cum Laude - Body text
```

### 7. Achievements
```
KEY ACHIEVEMENTS AND IMPACT - Section header
Category - Job title style
• Achievement 1 - Body text
• Achievement 2 - Body text
```

## Modifying the Template

### Adding New Styles

1. **Define the style in `_create_styles()` method:**
```python
"NewStyle": ParagraphStyle(
    "CustomNewStyle",
    parent=styles["Normal"],
    fontSize=10,
    textColor=HexColor(colors.get("NEW_COLOR", "#000000")),
    spaceAfter=6,
)
```

2. **Add the color to color schemes:**
```json
{
  "NEW_COLOR": "#FF0000"
}
```

3. **Use the style in content generation:**
```python
story.append(Paragraph("New content", self.styles["NewStyle"]))
```

### Modifying Existing Styles

1. **Change font size:**
```python
fontSize=12,  # Change from 9 to 12
```

2. **Change alignment:**
```python
alignment=TA_RIGHT,  # Change from TA_LEFT to TA_RIGHT
```

3. **Change spacing:**
```python
spaceAfter=12,  # Increase spacing
spaceBefore=6,  # Add space before
```

### Adding New Color Schemes

1. **Create new JSON file in `color_schemes/` directory:**
```json
{
  "scheme_name": "my_custom_scheme",
  "NAME_COLOR": "#FF0000",
  "TITLE_COLOR": "#00FF00",
  "SECTION_HEADER_COLOR": "#0000FF",
  "JOB_TITLE_COLOR": "#FFFF00",
  "ACCENT_COLOR": "#FF00FF",
  "COMPETENCY_HEADER_COLOR": "#00FFFF",
  "SUBTITLE_COLOR": "#FFA500",
  "LINK_COLOR": "#800080",
  "LIGHT_ACCENT_COLOR": "#FFB6C1",
  "LIGHT_SECONDARY_COLOR": "#F0E68C",
  "DARK_TEXT_COLOR": "#000000",
  "MEDIUM_TEXT_COLOR": "#404040",
  "LIGHT_TEXT_COLOR": "#808080"
}
```

2. **The system will automatically detect and use the new scheme**

### Modifying Content Structure

1. **Add new sections in the generation methods:**
```python
# Add after existing sections
if self.data.get("new_section"):
    story.append(Paragraph("NEW SECTION", self.styles["SectionHeader"]))
    for item in self.data["new_section"]:
        story.append(Paragraph(f"• {item}", self.styles["Body"]))
    story.append(Spacer(1, 6))
```

2. **Modify existing sections:**
```python
# Change how experience is displayed
for job in experience:
    # Custom formatting
    title_line = f"{job.get('title', '')} at {job.get('company', '')}"
    story.append(Paragraph(title_line, self.styles["JobTitle"]))
```

## Best Practices

### Color Selection
- **Contrast:** Ensure sufficient contrast between text and background
- **Accessibility:** Consider colorblind users
- **Professional:** Choose colors appropriate for your industry
- **Consistency:** Use the same color for similar elements

### Typography
- **Hierarchy:** Use different font sizes to create visual hierarchy
- **Readability:** Don't go below 9pt for body text
- **Consistency:** Use the same font family throughout
- **Spacing:** Use consistent spacing between elements

### Layout
- **Margins:** Keep adequate margins for printing
- **Alignment:** Use consistent alignment patterns
- **Whitespace:** Don't overcrowd the page
- **Sections:** Clearly separate different sections

## Troubleshooting

### Common Issues

1. **Colors not applying:**
   - Check color scheme JSON syntax
   - Verify color codes are valid hex values
   - Ensure color keys match exactly

2. **Text not displaying:**
   - Check if data exists in JSON
   - Verify style names are correct
   - Check for encoding issues

3. **Layout problems:**
   - Adjust margins and spacing
   - Check page size settings
   - Verify content fits on page

4. **Font issues:**
   - Ensure fonts are available
   - Check font size limits
   - Verify font family names

### Debug Tips

1. **Add debug output:**
```python
print(f"Using color: {colors.get('NAME_COLOR', '#000000')}")
```

2. **Test with simple content:**
```python
story.append(Paragraph("Test", self.styles["Body"]))
```

3. **Check data structure:**
```python
print(f"Data keys: {list(self.data.keys())}")
```

## Advanced Customization

### Custom Fonts
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register custom font
pdfmetrics.registerFont(TTFont('CustomFont', 'path/to/font.ttf'))

# Use in style
"CustomStyle": ParagraphStyle(
    "CustomStyle",
    fontName="CustomFont",
    fontSize=12,
)
```

### Custom Page Sizes
```python
from reportlab.lib.pagesizes import A4, letter

# Use A4 instead of letter
doc = SimpleDocTemplate(filename, pagesize=A4)
```

### Dynamic Content
```python
# Conditional sections based on data
if self.data.get("has_projects"):
    # Add projects section
    pass
```

This template system provides a flexible foundation for creating professional resumes while maintaining consistency and allowing for easy customization.
