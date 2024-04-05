from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
from .forms import *

@login_required
def index(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        with transaction.atomic():
            profile_form = ProfileForm(request.POST, instance=user_profile)
            education_formset = EducationFormSet(request.POST, instance=user_profile)
            experience_formset = ExperienceFormSet(request.POST, instance=user_profile)
            skill_formset = SkillFormSet(request.POST, instance=user_profile)
            project_formset = ProjectFormSet(request.POST, instance=user_profile)
            award_and_certification_formset = AwardAndCertificationFormSet(request.POST, instance=user_profile)
                      
            formsets_valid = all([
                profile_form.is_valid(), 
                education_formset.is_valid(),
                experience_formset.is_valid(), 
                skill_formset.is_valid(),
                project_formset.is_valid(), 
                award_and_certification_formset.is_valid()
            ])

            if formsets_valid:
                profile_form.save()
                education_formset.save()
                experience_formset.save()
                skill_formset.save()
                project_formset.save()
                award_and_certification_formset.save()

                for skill_form in skill_formset:
                    if skill_form.instance.pk:
                        technical_skill_formset = TechnicalSkillFormSet(request.POST, instance=skill_form.instance)
                        tool_formset = ToolFormSet(request.POST, instance=skill_form.instance)
                        if technical_skill_formset.is_valid():
                            technical_skill_formset.save()
                        if tool_formset.is_valid():
                            tool_formset.save()
                
                for project_form in project_formset:
                    if project_form.instance.pk:
                        technology_formset = TechnologyFormSet(request.POST, instance=project_form.instance)
                        if technology_formset.is_valid():
                            technology_formset.save()

                return redirect('workprofile:index')
    else:
        profile_form = ProfileForm(instance=user_profile)
        education_formset = EducationFormSet(instance=user_profile)
        experience_formset = ExperienceFormSet(instance=user_profile)
        skill_formset = SkillFormSet(instance=user_profile)
        project_formset = ProjectFormSet(instance=user_profile)
        award_and_certification_formset = AwardAndCertificationFormSet(instance=user_profile)

    context = {
        'profile_form': profile_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
        'award_and_certification_formset': award_and_certification_formset,
    }

    return render(request, 'workprofile/index.html', context)
