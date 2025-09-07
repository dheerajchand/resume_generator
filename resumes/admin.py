from django.contrib import admin
from .models import (
    CustomUser, UserProfile, UserResumeData, UserDirectory,
    ResumeTemplate, PersonalInfo, CompetencyCategory, Competency,
    Experience, Project, Education, Certification, Achievement,
    Resume, ColorScheme, ResumeGenerationJob
)
from .user_admin import CustomUserAdmin, UserProfileAdmin, UserResumeDataAdmin, UserDirectoryAdmin

# Register user models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserResumeData, UserResumeDataAdmin)
admin.site.register(UserDirectory, UserDirectoryAdmin)

# Register existing models
admin.site.register(ResumeTemplate)
admin.site.register(PersonalInfo)
admin.site.register(CompetencyCategory)
admin.site.register(Competency)
admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Achievement)
admin.site.register(Resume)
admin.site.register(ColorScheme)
admin.site.register(ResumeGenerationJob)
