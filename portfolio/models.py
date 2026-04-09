"""
Professional Portfolio Models — the master data for all resume outputs.

Content models (raw materials): PersonalInfo, SocialLink, Position,
Responsibility, Achievement, Project, ProjectTechnology, SkillCategory, Skill.

Single-user system — no user FK. Content is global, composed into
archetypes via M2M through-tables.
"""

from django.db import models


# ─── Content Models ───────────────────────────────────────────────────────────


class PersonalInfo(models.Model):
    """Singleton: name, contact, slogan, location. One record only."""

    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, help_text="e.g., Data Scientist & Software Engineer")
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, help_text="e.g., Austin, TX")
    location_display = models.CharField(
        max_length=200, blank=True,
        help_text="Display version with coordinates, e.g., Austin, TX (30.2672°N, 97.7431°W)"
    )
    slogan = models.CharField(max_length=300, blank=True, help_text="Tagline shown in header")

    class Meta:
        verbose_name = "Personal Info"
        verbose_name_plural = "Personal Info"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Enforce singleton: only one PersonalInfo record
        if not self.pk and PersonalInfo.objects.exists():
            raise ValueError("Only one PersonalInfo record is allowed.")
        super().save(*args, **kwargs)


class SocialLink(models.Model):
    """Ordered social/professional links (GitHub, LinkedIn, etc.)."""

    personal_info = models.ForeignKey(
        PersonalInfo, on_delete=models.CASCADE, related_name="social_links"
    )
    platform = models.CharField(max_length=100, help_text="e.g., LinkedIn, GitHub")
    url = models.URLField()
    display_text = models.CharField(max_length=200, blank=True, help_text="Text shown on resume if different from URL")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.platform}: {self.url}"


class Position(models.Model):
    """A job held. Title, company, location, dates."""

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    dates = models.CharField(max_length=100, help_text="e.g., 2021 - 2023 or 2005 - Present")
    subtitle = models.CharField(max_length=300, blank=True, help_text="e.g., Data Science & Political Analytics")
    is_current = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower = appears first (most recent)")

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.company} | {self.title} ({self.dates})"


class Responsibility(models.Model):
    """A bullet point under a Position. Two text variants for electoral/neutral contexts."""

    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="responsibilities"
    )
    text = models.TextField(help_text="Full version (used in electoral archetypes)")
    text_neutral = models.TextField(
        blank=True,
        help_text="Neutral version (used in non-electoral archetypes). If blank, 'text' is used everywhere."
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name_plural = "Responsibilities"

    def __str__(self):
        preview = self.text[:80] + "..." if len(self.text) > 80 else self.text
        return f"{self.position.company}: {preview}"

    def get_text(self, is_electoral=False):
        """Return the appropriate text variant."""
        if is_electoral or not self.text_neutral:
            return self.text
        return self.text_neutral


class Achievement(models.Model):
    """A standalone accomplishment bullet (key_achievements in JSON)."""

    slug = models.SlugField(unique=True, help_text="e.g., demographic_breakthrough")
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.slug


class Project(models.Model):
    """A key project with multiple description perspectives."""

    name = models.CharField(max_length=300)
    dates = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    impact = models.TextField(blank=True)
    technical_description = models.TextField(blank=True)
    business_description = models.TextField(blank=True)
    spatial_description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.name


class ProjectTechnology(models.Model):
    """A technology used in a project."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="technologies"
    )
    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name_plural = "Project Technologies"

    def __str__(self):
        return f"{self.project.name}: {self.name}"


class SkillCategory(models.Model):
    """Top-level skill grouping (e.g., Data Infrastructure, Programming)."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    """An individual skill within a category."""

    category = models.ForeignKey(
        SkillCategory, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=200, help_text="e.g., Python, Pipelines")
    detail = models.TextField(blank=True, help_text="e.g., 20+ years: NumPy, Pandas, Scikit-learn...")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.category.name}: {self.name}"
