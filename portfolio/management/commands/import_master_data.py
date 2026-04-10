"""
Import master resume data from JSON files into portfolio models.

Reads comprehensive_master_achievements.json and resume_type_definitions.json,
creates all portfolio model instances. Idempotent: safe to re-run.
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand

from portfolio.models import (
    Achievement,
    PersonalInfo,
    Position,
    ProfessionalSummary,
    Project,
    ProjectTechnology,
    Responsibility,
    ResumeArchetype,
    ResumeArchetypeAchievement,
    ResumeArchetypePosition,
    ResumeArchetypeProject,
    ResumeArchetypeSkillCategory,
    Skill,
    SkillCategory,
    SocialLink,
)


class Command(BaseCommand):
    help = "Import comprehensive_master_achievements.json and resume_type_definitions.json into portfolio models"

    def add_arguments(self, parser):
        parser.add_argument(
            "--json-dir",
            type=str,
            default=".",
            help="Directory containing the JSON files (default: project root)",
        )

    def handle(self, *args, **options):
        json_dir = Path(options["json_dir"])
        master_path = json_dir / "comprehensive_master_achievements.json"
        types_path = json_dir / "resume_type_definitions.json"

        if not master_path.exists():
            self.stderr.write(self.style.ERROR(f"Not found: {master_path}"))
            return

        with open(master_path, encoding="utf-8") as f:
            master = json.load(f)["comprehensive_master_achievements"]

        self.stdout.write("Importing master data...")

        self._import_personal_info(master["personal_info"])
        self._import_achievements(master["key_achievements"])
        self._import_positions(master["work_experience"])
        self._import_projects(master["key_projects"])
        self._import_skills(master["technical_skills_comprehensive"])

        if types_path.exists():
            with open(types_path, encoding="utf-8") as f:
                type_defs = json.load(f)["resume_type_configurations"]
            self._import_archetypes(type_defs, master["professional_summary"])
        else:
            self.stderr.write(self.style.WARNING(f"Not found: {types_path} — skipping archetypes"))

        self.stdout.write(self.style.SUCCESS("Import complete."))
        self._print_counts()

    def _import_personal_info(self, data):
        contact = data.get("contact", {})
        info, created = PersonalInfo.objects.update_or_create(
            pk=1,
            defaults={
                "name": data.get("name", ""),
                "title": data.get("title", ""),
                "email": contact.get("email", ""),
                "phone": contact.get("phone", ""),
                "website": contact.get("website", ""),
                "location": contact.get("location", ""),
                "location_display": data.get("location_display", ""),
                "slogan": data.get("slogan", ""),
                "footer_text": 'Built with <a href="https://www.djangoproject.com/">Django</a> and <a href="https://docs.reportlab.com/">ReportLab</a>.',
            },
        )
        # Social links
        links = [
            ("LinkedIn", contact.get("linkedin", "")),
            ("GitHub", contact.get("github", "")),
        ]
        for platform, url in links:
            if url:
                SocialLink.objects.update_or_create(
                    personal_info=info,
                    platform=platform,
                    defaults={"url": url, "sort_order": links.index((platform, url))},
                )
        action = "Created" if created else "Updated"
        self.stdout.write(f"  {action} PersonalInfo: {info.name}")

    def _import_achievements(self, data):
        for idx, (slug, text) in enumerate(data.items()):
            Achievement.objects.update_or_create(
                slug=slug,
                defaults={"text": text, "sort_order": idx},
            )
        self.stdout.write(f"  Imported {len(data)} achievements")

    def _import_positions(self, data):
        # Map of JSON keys to position data
        for idx, (_key, pos_data) in enumerate(data.items()):
            position, _ = Position.objects.update_or_create(
                company=pos_data["company"],
                title=pos_data["title"],
                defaults={
                    "location": pos_data.get("location", ""),
                    "dates": pos_data.get("dates", ""),
                    "subtitle": pos_data.get("subtitle", ""),
                    "is_current": "Present" in pos_data.get("dates", ""),
                    "sort_order": idx,
                },
            )

            # Import responsibilities
            comprehensive = pos_data.get("comprehensive_responsibilities", [])
            neutral = pos_data.get("comprehensive_responsibilities_neutral", [])

            # Match neutral to comprehensive by index
            for r_idx, text in enumerate(comprehensive):
                text_neutral = neutral[r_idx] if r_idx < len(neutral) else ""
                Responsibility.objects.update_or_create(
                    position=position,
                    sort_order=r_idx,
                    defaults={"text": text, "text_neutral": text_neutral},
                )

        self.stdout.write(f"  Imported {len(data)} positions with responsibilities")

    def _import_projects(self, data):
        for idx, (_key, proj_data) in enumerate(data.items()):
            project, _ = Project.objects.update_or_create(
                name=proj_data["name"],
                defaults={
                    "dates": proj_data.get("dates") or "",
                    "description": proj_data.get("description") or "",
                    "impact": proj_data.get("impact") or "",
                    "technical_description": proj_data.get("technical_description") or "",
                    "business_description": proj_data.get("business_description") or "",
                    "spatial_description": proj_data.get("spatial_description") or "",
                    "sort_order": idx,
                },
            )

            # Import technologies
            for t_idx, tech_name in enumerate(proj_data.get("technologies", [])):
                ProjectTechnology.objects.update_or_create(
                    project=project,
                    name=tech_name,
                    defaults={"sort_order": t_idx},
                )

        self.stdout.write(f"  Imported {len(data)} projects with technologies")

    def _import_skills(self, data):
        for idx, (cat_key, skills_data) in enumerate(data.items()):
            # Format display name from key
            display_name = {
                "programming_expertise": "Programming and Development",
                "geospatial_stack": "Geospatial Technologies",
                "machine_learning_ai": "Machine Learning & AI",
                "data_engineering": "Data Infrastructure",
                "cloud_devops": "Cloud & DevOps",
            }.get(cat_key, cat_key.replace("_", " ").title())

            category, _ = SkillCategory.objects.update_or_create(
                slug=cat_key,
                defaults={"name": display_name, "sort_order": idx},
            )

            for s_idx, (skill_key, skill_detail) in enumerate(skills_data.items()):
                # Format skill name
                skill_name = {
                    "python": "Python", "r": "R", "sql": "SQL/PostGIS",
                    "javascript": "JavaScript", "java": "Java",
                    "other": "Other Technologies", "databases": "Databases",
                    "analysis": "Analysis Tools", "web_mapping": "Web Mapping",
                    "processing": "Processing", "frameworks": "ML Frameworks",
                    "geospatial_ml": "Geospatial ML", "techniques": "Techniques",
                    "validation": "Validation", "pipelines": "Pipelines",
                    "storage": "Storage", "streaming": "Streaming",
                    "aws": "AWS", "containerization": "Containerization",
                    "monitoring": "Monitoring", "cicd": "CI/CD",
                }.get(skill_key, skill_key.replace("_", " ").title())

                Skill.objects.update_or_create(
                    category=category,
                    name=skill_name,
                    defaults={"detail": skill_detail, "sort_order": s_idx},
                )

        self.stdout.write(f"  Imported {len(data)} skill categories")

    def _import_archetypes(self, type_defs, summaries):
        # Map JSON position keys to Position objects by company name
        position_map = {}
        for pos in Position.objects.all():
            # Build the key from company name
            key = pos.company.lower().replace("/", "_").replace(" ", "_")
            # Handle known mappings
            key_mappings = {
                "siege_analytics": "siege_analytics",
                "helm_murmuration": "helm_murmuration",
                "gsd&m": "gsdm",
                "mautinoa_technologies": "mautinoa_technologies",
                "myers_research": "myers_research",
                "pccc": "pccc",
                "salsa_labs": "salsa_labs",
                "the_praxis_project": "praxis_project",
                "lake_research_partners": "lake_research_partners",
                "the_feldman_group": "feldman_group",
            }
            for pattern, mapped_key in key_mappings.items():
                if pattern in key:
                    position_map[mapped_key] = pos
                    break

        # Map JSON project keys to Project objects
        project_map = {}
        project_key_to_name = {
            "siege_utilities": "Siege Utilities",
            "redistricting_platform": "National Redistricting Platform",
            "fleem_polling_system": "FLEEM",
            "demographic_ml_system": "Geospatial Demographic Classification System",
            "civic_graph": "Civic Graph",
            "tile_server_platform": "High-Performance Geospatial Tile Server",
            "musescore_chord_library": "MuseScore",
        }
        for key, name_fragment in project_key_to_name.items():
            proj = Project.objects.filter(name__icontains=name_fragment).first()
            if proj:
                project_map[key] = proj

        archetype_descriptions = {
            "comprehensive": "Complete career overview showcasing the full breadth of experience across data science, software engineering, and political analytics. Best for senior-level positions.",
            "data_engineering": "Data infrastructure focus: federated medallion architectures, Databricks/PySpark/dbt pipelines, and geospatial data warehousing. Best for data platform and analytics engineering roles.",
            "software_engineering": "Software development expertise: full-stack systems, distributed computing, and production platforms. Best for backend, full-stack, and systems engineering roles.",
            "gis": "Mapping and spatial analysis: PostGIS, GDAL, custom tile servers, LiDAR/PointCloud processing, and geospatial ML. Best for GIS analyst and spatial data science roles.",
            "product": "Business strategy focus: team leadership, platform development, and revenue generation. Best for product management and data leadership roles.",
            "marketing": "Data-driven marketing: consumer segmentation, testing, and optimization. Best for marketing analytics and audience strategy roles.",
            "data_analysis_visualization": "Data science specialization: building analytical infrastructure, ML algorithms, demographic analysis, and spatial visualization. Best for data analyst and analytics engineer roles.",
            "polling_research_redistricting": "Research and redistricting: survey methodology, electoral prediction, and demographic modeling. Best for political research and redistricting roles.",
        }

        for type_key, config in type_defs.items():
            is_electoral = type_key == "polling_research_redistricting"
            archetype, _ = ResumeArchetype.objects.update_or_create(
                slug=type_key,
                defaults={
                    "name": type_key.replace("_", " ").title(),
                    "description": archetype_descriptions.get(type_key, ""),
                    "is_electoral": is_electoral,
                    "max_achievements": config["achievements"].get("total_max", 4),
                    "max_responsibilities_per_job": config["experience"].get("max_responsibilities_per_job", 3),
                    "siege_analytics_max": config["experience"].get("siege_analytics_max", 6),
                    "show_project_technical_details": config["projects"].get("show_technical_details", True),
                    "competency_detail_level": config["competencies"].get("detail_level", "focused"),
                },
            )

            # Professional summary
            summary_key = config.get("summary_key", type_key)
            summary_text = summaries.get(summary_key, "")
            if summary_text:
                ProfessionalSummary.objects.update_or_create(
                    archetype=archetype,
                    defaults={"text": summary_text},
                )

            # Link positions
            ResumeArchetypePosition.objects.filter(archetype=archetype).delete()
            for idx, pos_key in enumerate(config["experience"]["include_positions"]):
                if pos_key in position_map:
                    ResumeArchetypePosition.objects.create(
                        archetype=archetype,
                        position=position_map[pos_key],
                        sort_order=idx,
                    )

            # Link achievements
            ResumeArchetypeAchievement.objects.filter(archetype=archetype).delete()
            for idx, ach_slug in enumerate(config["achievements"]["include_achievements"]):
                ach = Achievement.objects.filter(slug=ach_slug).first()
                if ach:
                    ResumeArchetypeAchievement.objects.create(
                        archetype=archetype,
                        achievement=ach,
                        sort_order=idx,
                    )

            # Link projects
            ResumeArchetypeProject.objects.filter(archetype=archetype).delete()
            for idx, proj_key in enumerate(config["projects"]["include_projects"]):
                if proj_key in project_map:
                    ResumeArchetypeProject.objects.create(
                        archetype=archetype,
                        project=project_map[proj_key],
                        sort_order=idx,
                    )

            # Link skill categories
            ResumeArchetypeSkillCategory.objects.filter(archetype=archetype).delete()
            for idx, cat_slug in enumerate(config["competencies"]["include_categories"]):
                cat = SkillCategory.objects.filter(slug=cat_slug).first()
                if cat:
                    ResumeArchetypeSkillCategory.objects.create(
                        archetype=archetype,
                        skill_category=cat,
                        sort_order=idx,
                    )

        self.stdout.write(f"  Imported {len(type_defs)} archetypes with all relationships")

    def _print_counts(self):
        self.stdout.write("\nRecord counts:")
        self.stdout.write(f"  PersonalInfo:    {PersonalInfo.objects.count()}")
        self.stdout.write(f"  SocialLinks:     {SocialLink.objects.count()}")
        self.stdout.write(f"  Positions:       {Position.objects.count()}")
        self.stdout.write(f"  Responsibilities:{Responsibility.objects.count()}")
        self.stdout.write(f"  Achievements:    {Achievement.objects.count()}")
        self.stdout.write(f"  Projects:        {Project.objects.count()}")
        self.stdout.write(f"  SkillCategories: {SkillCategory.objects.count()}")
        self.stdout.write(f"  Skills:          {Skill.objects.count()}")
        self.stdout.write(f"  Archetypes:      {ResumeArchetype.objects.count()}")
        self.stdout.write(f"  Summaries:       {ProfessionalSummary.objects.count()}")
