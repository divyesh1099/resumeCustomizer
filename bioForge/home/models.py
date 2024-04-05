from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github = models.URLField(blank=True)
    leetcode = models.URLField(blank=True)

class Education(models.Model):
    TYPE_CHOICES = (
        ('B.Tech', 'B.Tech'),
        ('M.Tech', 'M.Tech'),
        # Add other types as needed
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    college_name = models.CharField(max_length=255)
    start_year = models.DateField()
    end_year = models.DateField()

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    start_month_year = models.DateField()
    end_month_year = models.DateField()
    city = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    description = models.TextField()

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    technical_skills = models.CharField(max_length=255)
    tools = models.CharField(max_length=255)

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    github_url = models.URLField()
    hosted_url = models.URLField()

class AwardCertification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_achievement = models.DateField()
