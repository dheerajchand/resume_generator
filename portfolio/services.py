"""
Build resume data dicts from database models.

This replaces master_resume_generator.py's create_specialized_resume()
by reading from the portfolio database models instead of JSON files.
"""

from .models import (
    PersonalInfo, ResumeArchetype, ProfessionalSummary,
    ResumeArchetypePosition, ResumeArchetypeAchievement,
    ResumeArchetypeProject, ResumeArchetypeSkillCategory,
)


def build_resume_data_from_db(archetype_slug, output_type="ats"):
    """Build a resume_data dict from database models.

    Returns the same structure as create_specialized_resume() from
    master_resume_generator.py, so ResumeGenerator.from_data() can
    consume it without changes.
    """
    archetype = (
        ResumeArchetype.objects
        .select_related()
        .prefetch_related(
            "resumearchetypeposition_set__position__responsibilities",
            "resumearchetypeachievement_set__achievement",
            "resumearchetypeproject_set__project__technologies",
            "resumearchetypeskillcategory_set__skill_category__skills",
        )
        .get(slug=archetype_slug)
    )

    # Personal info
    try:
        info = PersonalInfo.objects.prefetch_related("social_links").get()
    except PersonalInfo.DoesNotExist:
        raise ValueError("No PersonalInfo record found. Run import_master_data first.")

    personal_info = {
        "name": info.name,
        "title": info.title,
        "slogan": info.slogan,
        "location_display": info.location_display,
        "contact": {
            "email": info.email,
            "phone": info.phone,
            "website": info.website,
            "linkedin": "",
            "github": "",
            "location": info.location,
        },
    }
    for link in info.social_links.all():
        if "linkedin" in link.platform.lower():
            personal_info["contact"]["linkedin"] = link.url
        elif "github" in link.platform.lower():
            personal_info["contact"]["github"] = link.url

    # Summary
    try:
        summary_text = archetype.summary.text
    except ProfessionalSummary.DoesNotExist:
        summary_text = ""

    # Achievements
    achievement_links = archetype.resumearchetypeachievement_set.all().order_by("sort_order")
    achievements_list = [link.achievement.text for link in achievement_links]
    achievements_list = achievements_list[:archetype.max_achievements]

    # Experience
    is_electoral = archetype.is_electoral
    position_links = archetype.resumearchetypeposition_set.all().order_by("sort_order")
    experience = []
    for link in position_links:
        pos = link.position
        max_resp = (
            archetype.siege_analytics_max
            if pos.company == "Siege Analytics"
            else archetype.max_responsibilities_per_job
        )
        responsibilities = []
        for resp in pos.responsibilities.all().order_by("sort_order")[:max_resp]:
            responsibilities.append(resp.get_text(is_electoral=is_electoral))

        experience.append({
            "title": pos.title,
            "company": pos.company,
            "location": pos.location,
            "dates": pos.dates,
            "subtitle": pos.subtitle,
            "responsibilities": responsibilities,
        })

    # Projects
    project_links = archetype.resumearchetypeproject_set.all().order_by("sort_order")
    projects = []
    for link in project_links:
        proj = link.project
        project_data = {
            "name": proj.name,
            "dates": proj.dates,
            "description": proj.description,
            "technologies": [t.name for t in proj.technologies.all().order_by("sort_order")],
            "impact": proj.impact,
        }
        if archetype.show_project_technical_details:
            # Include technical_details if they exist (stored as description variants)
            pass  # technical_details are not in the DB model as a list; kept for PDF compat
        projects.append(project_data)

    # Competencies
    skill_cat_links = archetype.resumearchetypeskillcategory_set.all().order_by("sort_order")
    competencies = {}
    for link in skill_cat_links:
        cat = link.skill_category
        skills_list = []
        for skill in cat.skills.all().order_by("sort_order"):
            if skill.detail:
                skills_list.append(f"{skill.name}: {skill.detail}")
            else:
                skills_list.append(skill.name)
        competencies[cat.name] = skills_list

    return {
        "personal_info": personal_info,
        "summary": summary_text,
        "achievements": {"Impact": achievements_list},
        "experience": experience,
        "projects": projects,
        "competencies": competencies,
        "education": [],
        "additional_info": "",
    }


def get_archetype_metadata():
    """Return metadata for all archetypes (for the form page dropdown)."""
    archetypes = ResumeArchetype.objects.all().order_by("name")
    return [
        {
            "slug": a.slug,
            "name": a.name,
            "description": a.description,
        }
        for a in archetypes
    ]
