from django.urls import path
from . import views
app_name = 'chatgeminiapi'

urlpatterns = [
    path('', views.askQuestion, name='index'),
]