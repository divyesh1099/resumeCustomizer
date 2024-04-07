from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os

# Create your views here.
def index(request):
    return render(request, 'latexEditor/index.html')


def load_file(request, filename):
    file_path = os.path.join(settings.STATIC_ROOT, 'load-file', filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return HttpResponse(file.read(), content_type='text/plain')
    else:
        return HttpResponse('File not found.', status=404)