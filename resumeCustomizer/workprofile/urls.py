from django.urls import path
from . import views
app_name = 'workprofile'

urlpatterns = [
    path('', views.index, name='index'),
]