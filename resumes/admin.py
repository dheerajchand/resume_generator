from django.contrib import admin

from .models import (
    Achievement,
    Certification,
    ColorScheme,
    Competency,
    CompetencyCategory,
    CustomUser,
    Education,
    Experience,
    PersonalInfo,
    Project,
    Resume,
    ResumeGenerationJob,
    ResumeTemplate,
    UserColorScheme,
    UserDirectory,
    UserProfile,
    UserResumeData,
)
from .user_admin import CustomUserAdmin, UserDirectoryAdmin, UserProfileAdmin, UserResumeDataAdmin

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
admin.site.register(UserColorScheme)
admin.site.register(ResumeGenerationJob)
