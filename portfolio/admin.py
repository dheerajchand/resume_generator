"""
Portfolio admin — full Grappelli configuration with sortable inlines,
fieldsets, and filter widgets for all portfolio models.
"""

from django.contrib import admin

from .models import (
    Achievement,
    EmailTemplate,
    GenerationRecord,
    PersonalInfo,
    Position,
    ProfessionalSummary,
    Project,
    ProjectTechnology,
    Recipient,
    Responsibility,
    ResumeArchetype,
    ResumeArchetypeAchievement,
    ResumeArchetypePosition,
    ResumeArchetypeProject,
    ResumeArchetypeSkillCategory,
    ResumeInstance,
    Skill,
    SkillCategory,
    SocialLink,
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
        ("Identity", {"fields": ["name", "title", "slogan", "logo_url"]}),
        ("Contact", {"fields": ["email", "phone", "website"]}),
        ("Location", {"fields": ["location", "location_display"]}),
        ("Footer", {"fields": ["footer_text"], "description": "HTML allowed. If blank, defaults to 'Built with Django and ReportLab' with links."}),
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


def send_resume_to_recipient(modeladmin, request, queryset):
    """Admin action: generate and email resume to each selected instance's recipient."""
    import io
    import sys
    from pathlib import Path

    from .email import send_resume_email
    from .models import GenerationRecord
    from .services import build_resume_data_from_db

    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from master_resume_generator import create_brief_resume
    from resumes.core_services import ResumeGenerator

    sent = 0
    errors = []

    for instance in queryset:
        if not instance.recipient or not instance.recipient.email:
            errors.append(f"{instance.name}: no recipient email")
            continue

        # Build resume data from archetype
        resume_data = build_resume_data_from_db(instance.archetype.slug, "ats")
        if instance.summary_override:
            resume_data["summary"] = instance.summary_override

        # Use brief for email attachments
        resume_data = create_brief_resume(resume_data, instance.archetype.slug)

        # Load color scheme
        color_config_path = project_root / "color_schemes" / "default_professional.json"
        config = {}
        if color_config_path.exists():
            import json
            with open(color_config_path, "r") as f:
                config = json.load(f)

        generator = ResumeGenerator.from_data(
            resume_data=resume_data, config=config,
            color_scheme="default_professional", length_variant="brief", output_type="ats",
        )

        buffer = io.BytesIO()
        generator.generate_pdf(buffer)
        buffer.seek(0)

        filename = f"dheeraj_chand_{instance.archetype.slug}_brief_default_professional.pdf"
        result = send_resume_email(instance, buffer, filename)

        if result.get("success"):
            GenerationRecord.objects.create(
                instance=instance, archetype_slug=instance.archetype.slug,
                format_type="pdf", output_type="ats",
                color_scheme="default_professional", length_variant="brief",
                was_emailed=True,
            )
            # Auto-set follow-up to 5 business days from now
            import datetime
            today = datetime.date.today()
            days_added = 0
            follow_up = today
            while days_added < 5:
                follow_up += datetime.timedelta(days=1)
                if follow_up.weekday() < 5:  # Mon-Fri
                    days_added += 1
            instance.follow_up_date = follow_up
            instance.follow_up_status = "pending"
            instance.save(update_fields=["follow_up_date", "follow_up_status"])
            sent += 1
        else:
            errors.append(f"{instance.name}: {result.get('error', 'unknown')}")

    if sent:
        modeladmin.message_user(request, f"Sent {sent} resume(s) successfully.")
    if errors:
        modeladmin.message_user(request, f"Errors: {'; '.join(errors)}", level="error")


send_resume_to_recipient.short_description = "Send resume (brief PDF) to recipient via email"


@admin.register(ResumeInstance)
class ResumeInstanceAdmin(admin.ModelAdmin):
    list_display = ["name", "archetype", "recipient", "follow_up_status", "follow_up_date", "generation_count", "created_at"]
    list_filter = ["archetype", "follow_up_status"]
    list_editable = ["follow_up_status"]
    search_fields = ["name", "recipient__name", "recipient__company"]
    autocomplete_fields = ["archetype", "recipient"]
    actions = [send_resume_to_recipient]
    change_form_template = "portfolio/admin/resumeinstance_change_form.html"
    fieldsets = [
        (None, {"fields": ["name", "archetype", "recipient"]}),
        ("Overrides", {
            "classes": ["grp-collapse grp-closed"],
            "fields": ["summary_override", "subject_override"],
            "description": "Override the archetype summary or email subject line for this specific send.",
        }),
        ("Follow-Up", {"fields": ["follow_up_date", "follow_up_status", "follow_up_notes"]}),
        ("Notes", {"fields": ["notes"]}),
    ]

    def generation_count(self, obj):
        return obj.generations.count()
    generation_count.short_description = "Generations"

    def get_urls(self):
        from django.urls import path
        custom_urls = [
            path(
                "<int:instance_id>/generate-download/",
                self.admin_site.admin_view(self.generate_download_view),
                name="portfolio_resumeinstance_generate",
            ),
            path(
                "<int:instance_id>/send-email/",
                self.admin_site.admin_view(self.send_email_view),
                name="portfolio_resumeinstance_send",
            ),
        ]
        return custom_urls + super().get_urls()

    def generate_download_view(self, request, instance_id):
        """Generate a brief PDF for this instance and stream as download."""
        import io
        import sys
        from pathlib import Path as FilePath

        from .models import GenerationRecord
        from .services import build_resume_data_from_db

        instance = ResumeInstance.objects.get(pk=instance_id)

        project_root = FilePath(__file__).resolve().parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from master_resume_generator import create_brief_resume
        from resumes.core_services import ResumeGenerator

        resume_data = build_resume_data_from_db(instance.archetype.slug, "ats")
        if instance.summary_override:
            resume_data["summary"] = instance.summary_override

        resume_data = create_brief_resume(resume_data, instance.archetype.slug)

        import json
        color_config_path = project_root / "color_schemes" / "default_professional.json"
        config = {}
        if color_config_path.exists():
            with open(color_config_path, "r") as f:
                config = json.load(f)

        generator = ResumeGenerator.from_data(
            resume_data=resume_data, config=config,
            color_scheme="default_professional", length_variant="brief", output_type="ats",
        )

        buffer = io.BytesIO()
        generator.generate_pdf(buffer)
        buffer.seek(0)

        GenerationRecord.objects.create(
            instance=instance, archetype_slug=instance.archetype.slug,
            format_type="pdf", output_type="ats",
            color_scheme="default_professional", length_variant="brief",
        )

        from django.http import HttpResponse
        filename = f"dheeraj_chand_{instance.archetype.slug}_brief.pdf"
        response = HttpResponse(buffer.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def send_email_view(self, request, instance_id):
        """Generate a brief PDF and send it to the recipient."""
        import io
        import sys
        import datetime
        from pathlib import Path as FilePath

        from django.contrib import messages
        from django.shortcuts import redirect

        from .email import send_resume_email
        from .models import GenerationRecord
        from .services import build_resume_data_from_db

        instance = ResumeInstance.objects.get(pk=instance_id)

        if not instance.recipient or not instance.recipient.email:
            messages.error(request, f"No recipient email for {instance.name}")
            return redirect(f"../../{instance_id}/change/")

        project_root = FilePath(__file__).resolve().parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from master_resume_generator import create_brief_resume
        from resumes.core_services import ResumeGenerator

        resume_data = build_resume_data_from_db(instance.archetype.slug, "ats")
        if instance.summary_override:
            resume_data["summary"] = instance.summary_override

        resume_data = create_brief_resume(resume_data, instance.archetype.slug)

        import json
        color_config_path = project_root / "color_schemes" / "default_professional.json"
        config = {}
        if color_config_path.exists():
            with open(color_config_path, "r") as f:
                config = json.load(f)

        generator = ResumeGenerator.from_data(
            resume_data=resume_data, config=config,
            color_scheme="default_professional", length_variant="brief", output_type="ats",
        )

        buffer = io.BytesIO()
        generator.generate_pdf(buffer)
        buffer.seek(0)

        filename = f"dheeraj_chand_{instance.archetype.slug}_brief.pdf"
        result = send_resume_email(instance, buffer, filename)

        if result.get("success"):
            GenerationRecord.objects.create(
                instance=instance, archetype_slug=instance.archetype.slug,
                format_type="pdf", output_type="ats",
                color_scheme="default_professional", length_variant="brief",
                was_emailed=True,
            )
            # Auto-set follow-up
            today = datetime.date.today()
            days_added = 0
            follow_up = today
            while days_added < 5:
                follow_up += datetime.timedelta(days=1)
                if follow_up.weekday() < 5:
                    days_added += 1
            instance.follow_up_date = follow_up
            instance.follow_up_status = "pending"
            instance.save(update_fields=["follow_up_date", "follow_up_status"])
            messages.success(request, f"Resume sent to {instance.recipient.email}")
        else:
            messages.error(request, f"Send failed: {result.get('error', 'unknown')}")

        return redirect(f"../../{instance_id}/change/")


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
