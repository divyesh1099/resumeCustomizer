from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)
    leetcode_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    TYPE_CHOICES = [
        ('HS', 'High School'),
        ('U', 'University'),
        ('G', 'Graduate'),
        ('UG', 'Undergraduate'),
    ]
    education_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    college_name = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return f"{self.get_education_type_display()} - {self.college_name}"

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    role = models.CharField(max_length=255)
    start_month_year = models.DateField()
    end_month_year = models.DateField(blank=True, null=True) # Allows for current positions
    city = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.role} at {self.company_name}"

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return self.skill_name

class TechnicalSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='technical_skills')
    technical_skill_name = models.CharField(max_length=255)

    def __str__(self):
        return self.technical_skill_name

class Tool(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='tools')
    tool_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tool_name

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True) # Allows for ongoing projects

    def __str__(self):
        return self.project_name
    
class Technology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AwardAndCertification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='awards_and_certifications')
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    date_awarded = models.DateField()

    def __str__(self):
        return f"{self.name} by {self.issuer}"
