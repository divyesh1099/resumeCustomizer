# forms.py
from django.forms import ModelForm, inlineformset_factory, DateInput
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'state', 'city', 'linkedin_url', 'github_url', 'leetcode_url']

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['education_type', 'college_name', 'start_year', 'end_year']

# Formset for educations, allowing multiple educations to be submitted at once
EducationFormSet = inlineformset_factory(
    Profile, Education, form=EducationForm,
    extra=1, can_delete=True)

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['role', 'start_month_year', 'end_month_year', 'city', 'company_name', 'description']
        widgets = {
            'start_month_year': DateInput(attrs={'type': 'date'}),
            'end_month_year': DateInput(attrs={'type': 'date'}),
        }

ExperienceFormSet = inlineformset_factory(
    Profile, Experience, form=ExperienceForm,
    extra=1, can_delete=True)

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']

SkillFormSet = inlineformset_factory(
    Profile, Skill, form=SkillForm,
    extra=1, can_delete=True)

class TechnicalSkillForm(ModelForm):
    class Meta:
        model = TechnicalSkill
        fields = ['technical_skill_name']

TechnicalSkillFormSet = inlineformset_factory(
    Skill, TechnicalSkill, form=TechnicalSkillForm,
    extra=1, can_delete=True)

class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ['tool_name']

ToolFormSet = inlineformset_factory(
    Skill, Tool, form=ToolForm,
    extra=1, can_delete=True)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

ProjectFormSet = inlineformset_factory(
    Profile, Project, form=ProjectForm,
    extra=1, can_delete=True)

class TechnologyForm(ModelForm):
    class Meta:
        model = Technology
        fields = ['name']

TechnologyFormSet = inlineformset_factory(
    Project, Technology, form=TechnologyForm,
    extra=1, can_delete=True)

class AwardAndCertificationForm(ModelForm):
    class Meta:
        model = AwardAndCertification
        fields = ['name', 'issuer', 'date_awarded']
        widgets = {
            'date_awarded': DateInput(attrs={'type': 'date'}),
        }

AwardAndCertificationFormSet = inlineformset_factory(
    Profile, AwardAndCertification, form=AwardAndCertificationForm,
    extra=1, can_delete=True)