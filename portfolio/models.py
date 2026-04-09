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


# ─── Composition Models ──────────────────────────────────────────────────────


class ResumeArchetype(models.Model):
    """Domain template defining which content is included and how.

    Archetypes are the "classes" — Data Engineering, GIS, etc.
    Instances inherit from archetypes for specific opportunities.
    """

    DETAIL_LEVEL_CHOICES = [
        ("comprehensive", "Comprehensive"),
        ("focused", "Focused"),
        ("business_focused", "Business Focused"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, help_text="Shown on the public download form when this archetype is selected")
    is_electoral = models.BooleanField(default=False, help_text="If True, uses electoral-specific responsibility text")
    max_achievements = models.PositiveIntegerField(default=4)
    max_responsibilities_per_job = models.PositiveIntegerField(default=3)
    siege_analytics_max = models.PositiveIntegerField(default=6, help_text="Max responsibilities for Siege Analytics position")
    show_project_technical_details = models.BooleanField(default=True)
    competency_detail_level = models.CharField(max_length=20, choices=DETAIL_LEVEL_CHOICES, default="focused")

    # M2M through-tables for content selection with ordering
    positions = models.ManyToManyField(Position, through="ResumeArchetypePosition", blank=True)
    achievements = models.ManyToManyField(Achievement, through="ResumeArchetypeAchievement", blank=True)
    projects = models.ManyToManyField(Project, through="ResumeArchetypeProject", blank=True)
    skill_categories = models.ManyToManyField(SkillCategory, through="ResumeArchetypeSkillCategory", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProfessionalSummary(models.Model):
    """One summary per archetype — the type-specific professional summary."""

    archetype = models.OneToOneField(
        ResumeArchetype, on_delete=models.CASCADE, related_name="summary"
    )
    text = models.TextField()

    class Meta:
        verbose_name_plural = "Professional Summaries"

    def __str__(self):
        return f"Summary for {self.archetype.name}"


# ─── Through-Tables (M2M with ordering) ──────────────────────────────────────


class ResumeArchetypePosition(models.Model):
    """Which positions an archetype includes, and in what order."""

    archetype = models.ForeignKey(ResumeArchetype, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        unique_together = ["archetype", "position"]

    def __str__(self):
        return f"{self.archetype.name} → {self.position.company}"


class ResumeArchetypeAchievement(models.Model):
    """Which achievements an archetype includes, and in what order."""

    archetype = models.ForeignKey(ResumeArchetype, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        unique_together = ["archetype", "achievement"]

    def __str__(self):
        return f"{self.archetype.name} → {self.achievement.slug}"


class ResumeArchetypeProject(models.Model):
    """Which projects an archetype includes, and in what order."""

    archetype = models.ForeignKey(ResumeArchetype, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        unique_together = ["archetype", "project"]

    def __str__(self):
        return f"{self.archetype.name} → {self.project.name}"


class ResumeArchetypeSkillCategory(models.Model):
    """Which skill categories an archetype includes, and in what order."""

    archetype = models.ForeignKey(ResumeArchetype, on_delete=models.CASCADE)
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        unique_together = ["archetype", "skill_category"]

    def __str__(self):
        return f"{self.archetype.name} → {self.skill_category.name}"
