from django.contrib import admin
from .models import *

# Define your inlines here
class EducationInline(admin.TabularInline):
    model = Education
    extra = 0

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0

class AwardAndCertificationInline(admin.TabularInline):
    model = AwardAndCertification
    extra = 0

class TechnicalSkillInline(admin.TabularInline):
    model = TechnicalSkill
    extra = 0

class ToolInline(admin.TabularInline):
    model = Tool
    extra = 0

class TechnologyInline(admin.TabularInline):
    model = Technology
    extra = 0

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'skill_name')
    inlines = [TechnicalSkillInline, ToolInline]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'state', 'city')
    inlines = [EducationInline, ExperienceInline, ProjectInline, AwardAndCertificationInline]

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'education_type', 'college_name', 'start_year', 'end_year')
    list_filter = ('education_type', 'start_year', 'end_year')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'role', 'company_name', 'start_month_year', 'end_month_year', 'city')
    list_filter = ('start_month_year', 'end_month_year', 'city')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('profile', 'project_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    inlines = [TechnologyInline]

@admin.register(AwardAndCertification)
class AwardAndCertificationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'issuer', 'date_awarded')
    list_filter = ('date_awarded',)

# Make sure you don't register Skill or any other model more than once.
