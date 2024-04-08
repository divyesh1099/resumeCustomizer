from django.urls import path
from . import views
app_name = 'latexEditor'

urlpatterns = [
    path('', views.index, name='index'),
    path('compile/', views.compile_latex, name='compile_latex'),
    path('load-file/<str:filename>/', views.load_file, name='load_file'),
]