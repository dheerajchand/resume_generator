"""
Cache invalidation signals — clear cached resume data when content changes.
"""

import logging

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save

from .models import (
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
)

logger = logging.getLogger(__name__)

# All models whose changes should invalidate the resume cache
CACHE_INVALIDATING_MODELS = [
    PersonalInfo, Position, Responsibility, Achievement,
    Project, ProjectTechnology, SkillCategory, Skill,
    ResumeArchetype, ProfessionalSummary,
    ResumeArchetypePosition, ResumeArchetypeAchievement,
    ResumeArchetypeProject, ResumeArchetypeSkillCategory,
]


def invalidate_resume_cache(sender, **kwargs):
    """Clear all cached resume data when any content model changes."""
    # Clear all resume_data cache keys
    # Since we can't enumerate cache keys portably, we use a version key
    current_version = cache.get("resume_cache_version", 0)
    cache.set("resume_cache_version", current_version + 1, timeout=None)

    # Also clear archetype metadata cache
    cache.delete("archetype_metadata")

    logger.info(f"Resume cache invalidated (triggered by {sender.__name__})")


# Register signals for all content models
for model in CACHE_INVALIDATING_MODELS:
    post_save.connect(invalidate_resume_cache, sender=model)
    post_delete.connect(invalidate_resume_cache, sender=model)
