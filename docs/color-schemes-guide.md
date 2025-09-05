# Color Schemes Guide

## Overview

The Resume Generator includes 7 professional color schemes designed for different industries and use cases. This guide explains each scheme, how to create custom schemes, and best practices for color selection.

## Available Color Schemes

### 1. Default Professional
**File:** `color_schemes/default_professional.json`

**Color Palette:**
- **Primary Green:** #228B22 (Forest Green)
- **Secondary Gold:** #B8860B (Dark Goldenrod)  
- **Accent Red:** #722F37 (Dark Red)
- **Text Gray:** #333333 (Dark Gray)

**Best For:**
- Traditional corporate environments
- Finance and banking
- Consulting firms
- Government positions

**Visual Characteristics:**
- Conservative and trustworthy
- High contrast for readability
- Professional appearance
- Works well in print and digital

### 2. Corporate Blue
**File:** `color_schemes/corporate_blue.json`

**Color Palette:**
- **Primary Blue:** #1E3A8A (Navy Blue)
- **Secondary Blue:** #4A90E2 (Steel Blue)
- **Accent Blue:** #1E40AF (Dark Blue)
- **Text Gray:** #2C3E50 (Dark Gray)

**Best For:**
- Financial services
- Healthcare
- Legal firms
- Large corporations

**Visual Characteristics:**
- Authoritative and stable
- Clean, modern look
- High professional credibility
- Excellent for executive positions

### 3. Modern Tech
**File:** `color_schemes/modern_tech.json`

**Color Palette:**
- **Primary Blue:** #0066CC (Electric Blue)
- **Secondary Orange:** #FF6B35 (Orange)
- **Accent Gray:** #2C3E50 (Dark Gray)
- **Text Gray:** #34495E (Medium Gray)

**Best For:**
- Technology companies
- Startups
- Software development
- Digital marketing

**Visual Characteristics:**
- Dynamic and innovative
- Contemporary design
- Tech-forward appearance
- Appeals to younger audiences

### 4. Satellite Imagery
**File:** `color_schemes/satellite_imagery.json`

**Color Palette:**
- **Primary Green:** #2D5016 (Earth Green)
- **Secondary Blue:** #87CEEB (Sky Blue)
- **Accent Brown:** #CD853F (Terracotta)
- **Text Gray:** #2F4F4F (Dark Slate Gray)

**Best For:**
- Environmental science
- GIS and mapping
- Remote sensing
- Earth observation

**Visual Characteristics:**
- Natural and earthy
- Scientific appearance
- Reflects environmental focus
- Professional yet approachable

### 5. Terrain Mapping
**File:** `color_schemes/terrain_mapping.json`

**Color Palette:**
- **Primary Green:** #228B22 (Forest Green)
- **Secondary Brown:** #8B4513 (Saddle Brown)
- **Accent Tan:** #D2B48C (Tan)
- **Text Gray:** #2F4F4F (Dark Slate Gray)

**Best For:**
- Cartography
- Geography
- Surveying
- Geology

**Visual Characteristics:**
- Topographic map inspired
- Earth-tone palette
- Technical and precise
- Field-oriented appearance

### 6. Cartographic Professional
**File:** `color_schemes/cartographic_professional.json`

**Color Palette:**
- **Primary Blue:** #003366 (Deep Blue)
- **Secondary Gold:** #DAA520 (Goldenrod)
- **Accent Green:** #006400 (Dark Green)
- **Text Gray:** #2F4F4F (Dark Slate Gray)

**Best For:**
- GIS professionals
- Mapping specialists
- Surveying engineers
- Geographic analysis

**Visual Characteristics:**
- Classic map colors
- Professional and technical
- High contrast for clarity
- Traditional cartographic feel

### 7. Topographic Classic
**File:** `color_schemes/topographic_classic.json`

**Color Palette:**
- **Primary Brown:** #8B4513 (Saddle Brown)
- **Secondary Tan:** #D2B48C (Tan)
- **Accent Green:** #006400 (Dark Green)
- **Text Gray:** #2F4F4F (Dark Slate Gray)

**Best For:**
- Traditional mapping
- Geology
- Civil engineering
- Land surveying

**Visual Characteristics:**
- Classic topographic colors
- Earth-tone based
- Traditional and reliable
- Field-work oriented

## Color Role System

Each color scheme defines specific roles for different elements:

### Primary Colors
- **NAME_COLOR:** Main resume name/title
- **TITLE_COLOR:** Professional title/subtitle
- **SECTION_HEADER_COLOR:** Section titles (Experience, Education, etc.)

### Secondary Colors
- **JOB_TITLE_COLOR:** Individual job titles and project names
- **ACCENT_COLOR:** Highlights and important elements
- **COMPETENCY_HEADER_COLOR:** Competency category headers
- **SUBTITLE_COLOR:** Job subtitles and descriptions

### Link Colors
- **LINK_COLOR:** Email, website, and LinkedIn links
- **LIGHT_ACCENT_COLOR:** Lighter version of accent color
- **LIGHT_SECONDARY_COLOR:** Lighter version of secondary color

### Text Colors
- **DARK_TEXT_COLOR:** Main body text
- **MEDIUM_TEXT_COLOR:** Secondary text
- **LIGHT_TEXT_COLOR:** Tertiary text

## Creating Custom Color Schemes

### Step 1: Choose Your Base Colors

**Primary Color Selection:**
- Choose a color that represents your industry
- Ensure good contrast with white background
- Consider your target audience
- Think about brand consistency

**Secondary Color Selection:**
- Should complement the primary color
- Use color theory (complementary, analogous, triadic)
- Ensure sufficient contrast
- Consider accessibility

### Step 2: Create the JSON File

Create a new file in `color_schemes/` directory:

```json
{
  "scheme_name": "my_custom_scheme",
  "NAME_COLOR": "#1A365D",
  "TITLE_COLOR": "#2D3748", 
  "SECTION_HEADER_COLOR": "#2D3748",
  "JOB_TITLE_COLOR": "#1A365D",
  "ACCENT_COLOR": "#2B6CB0",
  "COMPETENCY_HEADER_COLOR": "#1A365D",
  "SUBTITLE_COLOR": "#4A5568",
  "LINK_COLOR": "#2B6CB0",
  "LIGHT_ACCENT_COLOR": "#63B3ED",
  "LIGHT_SECONDARY_COLOR": "#718096",
  "DARK_TEXT_COLOR": "#2D3748",
  "MEDIUM_TEXT_COLOR": "#4A5568",
  "LIGHT_TEXT_COLOR": "#718096"
}
```

### Step 3: Test Your Scheme

1. **Generate a test resume:**
```bash
python manage.py generate_resume --version comprehensive --color-scheme my_custom_scheme --format pdf
```

2. **Check for issues:**
   - Sufficient contrast
   - Readability
   - Professional appearance
   - Print compatibility

### Step 4: Refine and Iterate

- Adjust colors based on test results
- Consider different lighting conditions
- Test with different content lengths
- Get feedback from others

## Color Theory Guidelines

### Complementary Colors
- Colors opposite on the color wheel
- High contrast and visual impact
- Example: Blue and Orange

### Analogous Colors
- Colors next to each other on the color wheel
- Harmonious and pleasing
- Example: Blue, Blue-Green, Green

### Triadic Colors
- Three colors evenly spaced on the color wheel
- Vibrant and balanced
- Example: Red, Yellow, Blue

### Monochromatic Colors
- Different shades of the same color
- Elegant and sophisticated
- Example: Light Blue, Blue, Dark Blue

## Accessibility Considerations

### Contrast Ratios
- **Normal text:** Minimum 4.5:1 contrast ratio
- **Large text:** Minimum 3:1 contrast ratio
- **Test tools:** Use WebAIM contrast checker

### Colorblind Considerations
- **Red-Green colorblind:** Most common type
- **Blue-Yellow colorblind:** Less common
- **Monochrome:** Rare but important
- **Test with simulators:** Use online tools

### Best Practices
- Don't rely solely on color to convey information
- Use patterns or shapes as alternatives
- Test with different user groups
- Consider high contrast mode

## Industry-Specific Recommendations

### Technology
- **Colors:** Blues, grays, accent colors
- **Style:** Modern, clean, innovative
- **Examples:** Electric blue, steel gray, orange accents

### Healthcare
- **Colors:** Blues, greens, whites
- **Style:** Clean, trustworthy, professional
- **Examples:** Navy blue, medical green, clean white

### Finance
- **Colors:** Blues, grays, dark colors
- **Style:** Conservative, authoritative, stable
- **Examples:** Navy blue, charcoal gray, gold accents

### Creative
- **Colors:** Vibrant, contrasting, unique
- **Style:** Bold, artistic, expressive
- **Examples:** Bright colors, high contrast, unique combinations

### Education
- **Colors:** Blues, greens, warm colors
- **Style:** Approachable, intellectual, inspiring
- **Examples:** Academic blue, forest green, warm accents

## Testing Your Color Schemes

### Print Testing
1. **Print a sample resume**
2. **Check color accuracy**
3. **Verify readability**
4. **Test different paper types**

### Digital Testing
1. **View on different screens**
2. **Test in different lighting**
3. **Check mobile compatibility**
4. **Verify PDF rendering**

### User Testing
1. **Get feedback from colleagues**
2. **Test with target audience**
3. **Check accessibility**
4. **Verify professional appearance**

## Troubleshooting Common Issues

### Colors Too Bright
- Reduce saturation
- Use darker shades
- Add more gray
- Test in different lighting

### Poor Contrast
- Increase color difference
- Use darker text colors
- Add more contrast between elements
- Test with accessibility tools

### Unprofessional Appearance
- Use more conservative colors
- Reduce color variety
- Stick to industry standards
- Get professional feedback

### Print Issues
- Test color profiles
- Use CMYK color space
- Check printer settings
- Verify paper quality

## Advanced Customization

### Gradient Effects
While ReportLab doesn't support gradients directly, you can:
- Use multiple colors in sequence
- Create visual hierarchy with color intensity
- Use spacing and typography for depth

### Brand Integration
- Match company brand colors
- Use brand guidelines
- Maintain consistency across materials
- Consider brand personality

### Seasonal Variations
- Create seasonal color schemes
- Adjust for different times of year
- Consider cultural associations
- Test appropriateness

This color system provides a solid foundation for creating professional, accessible, and visually appealing resumes while maintaining the flexibility to customize for specific needs and industries.
