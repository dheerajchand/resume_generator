"""
URL smoke test — verifies all admin and public pages load without errors.
Run after any model or admin changes.
"""

import os
from django.core.management.base import BaseCommand
from django.test import Client


class Command(BaseCommand):
    help = "Smoke test all portfolio admin and public URLs"

    def handle(self, *args, **options):
        from django.conf import settings
        if "testserver" not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append("testserver")

        c = Client()
        logged_in = c.login(username="dheeraj", password="admin123")
        if not logged_in:
            self.stderr.write(self.style.ERROR("Login failed — create superuser first"))
            return

        urls = [
            ("/", "Public form"),
            ("/admin/", "Admin index"),
            ("/admin/portfolio/", "Portfolio section"),
            ("/admin/portfolio/personalinfo/", "PersonalInfo"),
            ("/admin/portfolio/position/", "Position list"),
            ("/admin/portfolio/achievement/", "Achievement list"),
            ("/admin/portfolio/project/", "Project list"),
            ("/admin/portfolio/skillcategory/", "SkillCategory list"),
            ("/admin/portfolio/resumearchetype/", "Archetype list"),
            ("/admin/portfolio/recipient/", "Recipient list"),
            ("/admin/portfolio/resumeinstance/", "Instance list"),
            ("/admin/portfolio/emailtemplate/", "EmailTemplate list"),
            ("/admin/portfolio/generationrecord/", "GenerationRecord"),
        ]

        # Add change pages for loaded data
        from portfolio.models import ResumeArchetype, Position
        for arch in ResumeArchetype.objects.all():
            urls.append((f"/admin/portfolio/resumearchetype/{arch.pk}/change/", f"Archetype: {arch.name}"))
        for pos in Position.objects.all():
            urls.append((f"/admin/portfolio/position/{pos.pk}/change/", f"Position: {pos.company}"))

        passed = 0
        failed = 0
        for url, name in urls:
            try:
                resp = c.get(url, SERVER_NAME="testserver")
                if resp.status_code == 200:
                    self.stdout.write(f"  \u2713  {name:35s}  {url}")
                    passed += 1
                else:
                    self.stderr.write(self.style.ERROR(f"  \u2717 {resp.status_code}  {name:35s}  {url}"))
                    failed += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"  \u2717 ERR  {name:35s}  {url}  -- {e}"))
                failed += 1

        self.stdout.write(f"\n{passed} passed, {failed} failed")
        if failed:
            self.stderr.write(self.style.ERROR("URL smoke test FAILED"))
        else:
            self.stdout.write(self.style.SUCCESS("URL smoke test PASSED"))
