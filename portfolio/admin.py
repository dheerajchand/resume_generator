"""
Portfolio admin — full Grappelli configuration with sortable inlines,
fieldsets, and filter widgets for all portfolio models.
"""

from django.contrib import admin
from .models import (
    PersonalInfo, SocialLink, Position, Responsibility,
    Achievement, Project, ProjectTechnology,
    SkillCategory, Skill,
    ResumeArchetype, ProfessionalSummary,
    ResumeArchetypePosition, ResumeArchetypeAchievement,
    ResumeArchetypeProject, ResumeArchetypeSkillCategory,
    Recipient, ResumeInstance, GenerationRecord, EmailTemplate,
)


# ─── Content Inlines ─────────────────────────────────────────────────────────


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"


class ResponsibilityInline(admin.StackedInline):
    model = Responsibility
    extra = 0
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"
    fields = ["text", "text_neutral", "sort_order"]


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"


# ─── Composition Inlines ─────────────────────────────────────────────────────


class ProfessionalSummaryInline(admin.StackedInline):
    model = ProfessionalSummary
    extra = 0
    max_num = 1
    classes = ["grp-collapse grp-open"]


class ArchetypePositionInline(admin.TabularInline):
    model = ResumeArchetypePosition
    extra = 1
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"
    autocomplete_fields = ["position"]


class ArchetypeAchievementInline(admin.TabularInline):
    model = ResumeArchetypeAchievement
    extra = 1
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"
    autocomplete_fields = ["achievement"]


class ArchetypeProjectInline(admin.TabularInline):
    model = ResumeArchetypeProject
    extra = 1
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"
    autocomplete_fields = ["project"]


class ArchetypeSkillCategoryInline(admin.TabularInline):
    model = ResumeArchetypeSkillCategory
    extra = 1
    classes = ["grp-collapse grp-open"]
    sortable_field_name = "sort_order"
    autocomplete_fields = ["skill_category"]


# ─── Content Admins ──────────────────────────────────────────────────────────


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline]
    fieldsets = [
        ("Identity", {"fields": ["name", "title", "slogan"]}),
        ("Contact", {"fields": ["email", "phone", "website"]}),
        ("Location", {"fields": ["location", "location_display"]}),
    ]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["company", "title", "dates", "is_current", "sort_order"]
    list_editable = ["sort_order"]
    list_filter = ["is_current"]
    search_fields = ["company", "title"]
    inlines = [ResponsibilityInline]
    fieldsets = [
        (None, {"fields": ["company", "title", "location", "dates", "subtitle"]}),
        ("Options", {"fields": ["is_current", "sort_order"]}),
    ]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["slug", "text_preview", "sort_order"]
    list_editable = ["sort_order"]
    search_fields = ["slug", "text"]

    def text_preview(self, obj):
        return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text
    text_preview.short_description = "Text"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "dates", "sort_order"]
    list_editable = ["sort_order"]
    search_fields = ["name"]
    inlines = [ProjectTechnologyInline]
    fieldsets = [
        (None, {"fields": ["name", "dates", "sort_order"]}),
        ("Description", {"fields": ["description", "impact"]}),
        ("Alternate Descriptions", {
            "classes": ["grp-collapse grp-closed"],
            "fields": ["technical_description", "business_description", "spatial_description"],
        }),
    ]


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "skill_count", "sort_order"]
    list_editable = ["sort_order"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [SkillInline]

    def skill_count(self, obj):
        return obj.skills.count()
    skill_count.short_description = "Skills"


# ─── Archetype Admin ─────────────────────────────────────────────────────────


@admin.register(ResumeArchetype)
class ResumeArchetypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_electoral", "max_achievements", "position_count", "project_count"]
    list_filter = ["is_electoral", "competency_detail_level"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [
        ProfessionalSummaryInline,
        ArchetypePositionInline,
        ArchetypeAchievementInline,
        ArchetypeProjectInline,
        ArchetypeSkillCategoryInline,
    ]
    fieldsets = [
        (None, {"fields": ["name", "slug", "description"]}),
        ("Configuration", {
            "fields": [
                "is_electoral",
                "max_achievements",
                "max_responsibilities_per_job",
                "siege_analytics_max",
                "show_project_technical_details",
                "competency_detail_level",
            ],
        }),
    ]

    def position_count(self, obj):
        return obj.positions.count()
    position_count.short_description = "Positions"

    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = "Projects"


# ─── Instance & Recipient Admins ─────────────────────────────────────────────


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "job_title", "relationship_type", "created_at"]
    list_filter = ["relationship_type", "company"]
    search_fields = ["name", "company", "job_title", "email"]
    fieldsets = [
        ("Contact", {"fields": ["name", "company", "role", "email", "linkedin_url"]}),
        ("Job", {"fields": ["job_title", "job_url", "relationship_type"]}),
        ("Notes", {"fields": ["notes"]}),
    ]


@admin.register(ResumeInstance)
class ResumeInstanceAdmin(admin.ModelAdmin):
    list_display = ["name", "archetype", "recipient", "created_at"]
    list_filter = ["archetype"]
    search_fields = ["name", "recipient__name", "recipient__company"]
    autocomplete_fields = ["archetype", "recipient"]
    fieldsets = [
        (None, {"fields": ["name", "archetype", "recipient"]}),
        ("Overrides", {
            "classes": ["grp-collapse grp-closed"],
            "fields": ["summary_override"],
        }),
        ("Notes", {"fields": ["notes"]}),
    ]


@admin.register(GenerationRecord)
class GenerationRecordAdmin(admin.ModelAdmin):
    list_display = ["__str__", "format_type", "length_variant", "color_scheme", "was_emailed", "generated_at"]
    list_filter = ["format_type", "output_type", "length_variant", "was_emailed"]
    readonly_fields = ["instance", "archetype_slug", "format_type", "output_type", "color_scheme", "length_variant", "generated_at", "was_emailed"]
    date_hierarchy = "generated_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_default"]
    list_filter = ["is_default"]
    prepopulated_fields = {"slug": ["name"]}
    fieldsets = [
        (None, {"fields": ["name", "slug", "is_default"]}),
        ("Template", {
            "fields": ["subject_template", "body_template"],
            "description": "Placeholders: {recipient_name}, {job_title}, {company}, {archetype_name}, {your_name}",
        }),
    ]
