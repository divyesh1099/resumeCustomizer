import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from workprofile.models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.core.files.storage import default_storage
from PyPDF2 import PdfReader #type:ignore
import os
import json
import re
API_URL = 'http://127.0.0.1:8000/chatgeminiapi/'

@login_required
def index(request):
    description_form = JobDescriptionForm(request.POST or None)
    file_form = FileUploadForm(request.POST, request.FILES or None)
    company_form = CompanyNameForm(request.POST or None)
    role_form = RoleForm(request.POST or None)
    context = {
        'description_form': description_form,
        'file_form': file_form,
        'company_form': company_form,
        'role_form': role_form,
    }

    if request.method == 'POST':
        if description_form.is_valid() and company_form.is_valid() and role_form.is_valid():
            job_description = description_form.cleaned_data.get('job_description')
            company_name = company_form.cleaned_data.get('company_name')
            role = role_form.cleaned_data.get('role')

            profile = Profile.objects.get(user=request.user)
            educations = profile.educations.all()
            experiences = profile.experiences.all()
            skills = profile.skills.all()
            projects = profile.projects.all()
            max_attempts = 5
            attempts = 0
            result = None

            while attempts < max_attempts and result is None:
                prompt = create_chatbot_prompt(
                    profile, educations, experiences, skills, projects, job_description, company_name, role
                )

                response = requests.post(API_URL, json={"question": prompt})
                if response.ok:
                    data = response.json().get('answer', '')
                    json_str_match = re.search(r'```json\n([\s\S]*?)\n```', data)
                    if json_str_match:
                        json_str = json_str_match.group(1)
                        try:
                            result = json.loads(json_str)
                        except json.JSONDecodeError:
                            # If JSON is invalid, break out of the loop
                            break
                    else:
                        # If no JSON structure found, increment attempts and retry
                        attempts += 1
                else:
                    # If response is not OK, break out of the loop
                    break

            if result is not None:
                if response.ok:
                    data = response.json().get('answer', '')
                    print(data)
                    try:
                        # Use regex to extract JSON from the response
                        json_str_match = re.search(r'```json\n([\s\S]*?)\n```', data)
                        if json_str_match:
                            json_str = json_str_match.group(1)
                            result = json.loads(json_str)

                            # Process result here
                            relevant_skill_ids = [int(id) for id in result.get('relevant_skills', [])]
                            relevant_project_ids = [int(id) for id in result.get('relevant_projects', [])]
                            relevant_skills = Skill.objects.filter(id__in=relevant_skill_ids)
                            relevant_projects = Project.objects.filter(id__in=relevant_project_ids)
                            relevant_experience = result.get('relevant_experience', [])

                            # Add data to context if needed and print them to the console
                            print("Relevant Skills:", list(relevant_skills))
                            print("Relevant Projects:", list(relevant_projects))
                            print("Relevant Experience:", relevant_experience)
                            # Pass data to context or directly to HttpResponse if needed
                            # Check if all relevant data lists are empty
                            if not result['relevant_skills'] and not result['relevant_projects'] and not result['relevant_experience']:
                                context['eligibility'] = False
                                return render(request, 'resume/index.html', context)
                            else:
                                request.session['relevant_skills'] = relevant_skill_ids
                                request.session['relevant_projects'] = relevant_project_ids
                                request.session['relevant_experience'] = result['relevant_experience']
                                context['eligibility'] = True
                        else:
                            # Handle the case where regex did not match
                            print("No JSON found in response.")
                            # Return an error message or set a context variable as needed
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                        # Return an error message or set a context variable as needed

                else:
                    print("Failed to get response from the AI Chatbot.")
                    # Return an error message or set a context variable as needed
            else:
                context['error'] = "Failed to obtain a valid response after several attempts."

    return render(request, 'resume/index.html', context)

def create_chatbot_prompt(profile, educations, experiences, skills, projects, job_description, company_name, role):
    # Assuming this function is inside a Django view, the `skills` print is for debug purpose
    details = {
        "user_id": profile.user.id,
        "educations": [{"id": edu.id, "detail": str(edu)} for edu in educations],
        "experiences": [{"id": exp.id, "detail": str(exp)} for exp in experiences],
        "skills": [{"id": skill.id, "name": skill.skill_name} for skill in skills],
        "projects": [{"id": proj.id, "detail": str(proj)} for proj in projects],
        "job_description": job_description,
        "company_name": company_name,
        "role": role,
    }

    # Create a string that includes JSON structure
    json_response_format = json.dumps({
        "relevant_skills": ["{{id}}"],
        "relevant_projects": ["{{id}}"],
        "relevant_experience": [{
            "id": "{{experience_id}}",
            "company_name": "{{company_name}}",
            "detail": "{{work experience detail}}"
        }]
    }, indent=2)

    prompt_template = (
        "Given the user details and job description below, identify the skills and projects most relevant to the role of a {role} at {company_name}. "
        "For experiences, provide a detailed description suitable for the role. Format the response in JSON with only IDs for skills and projects, "
        "but full details for experiences. Here are the details:\n{details}\n"
        "The expected JSON response format is:\n{json_response_format}\n"
        "Please generate the response according to this structure."
    )

    prompt = prompt_template.format(
        role=role,
        company_name=company_name,
        details=json.dumps(details, indent=2),  # Convert details to JSON formatted string
        json_response_format=json_response_format  # Insert the JSON response structure
    )

    return prompt

@login_required
def generate_resume(request):
    # Retrieve data from the session
    relevant_skill_ids = request.session.get('relevant_skills', [])
    relevant_project_ids = request.session.get('relevant_projects', [])
    relevant_experience = request.session.get('relevant_experience', [])

    # Fetch the actual objects based on the IDs stored in the session
    relevant_skills = Skill.objects.filter(id__in=relevant_skill_ids)
    relevant_projects = Project.objects.filter(id__in=relevant_project_ids)

    # Pass the data to the template context
    context = {
        'relevant_skills': relevant_skills,
        'relevant_projects': relevant_projects,
        'relevant_experience': relevant_experience,
    }

    # Render the resume data to a template
    return render(request, 'resume/generate_resume.html', context)