from django.urls import path
from . import views
app_name = 'resume'

urlpatterns=[
    path('', views.index, name='index'),
    path('generate_resume/', views.generate_resume, name='generate_resume'),
]