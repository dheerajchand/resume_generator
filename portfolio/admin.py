"""
Portfolio admin — basic registration for ticket #22.
Full Grappelli configuration (drag-to-reorder, fieldsets) is ticket #26.
"""

from django.contrib import admin
from .models import (
    PersonalInfo, SocialLink, Position, Responsibility,
    Achievement, Project, ProjectTechnology,
    SkillCategory, Skill,
)


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


class ResponsibilityInline(admin.TabularInline):
    model = Responsibility
    extra = 1


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["company", "title", "dates", "sort_order"]
    list_editable = ["sort_order"]
    inlines = [ResponsibilityInline]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["slug", "sort_order"]
    list_editable = ["sort_order"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "dates", "sort_order"]
    list_editable = ["sort_order"]
    inlines = [ProjectTechnologyInline]


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "sort_order"]
    list_editable = ["sort_order"]
    inlines = [SkillInline]
