from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os
import subprocess
from tempfile import NamedTemporaryFile
import json
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
    
def compile_latex(request):
    if request.method == 'POST':
        # Decode the request body and parse the JSON
        data = json.loads(request.body.decode('utf-8'))
        
        latex_code = data.get('code', '')
        filename = data.get('file', '').replace('.tex', '')  # Safety measure

        # Create a temporary file to hold the LaTeX code
        with NamedTemporaryFile(suffix=".tex", delete=False) as texfile:
            texfile.write(latex_code.encode('utf-8'))
            texfile_path = texfile.name

        # Attempt to compile the LaTeX code, capturing output and errors
        try:
            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', texfile_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            # Return detailed error message if compilation fails
            return JsonResponse({'error': 'Failed to compile LaTeX.', 'details': e.stderr}, status=500)


        # Assuming the PDF has the same name as the .tex file, but with .pdf extension
        pdf_path = texfile_path.replace('.tex', '.pdf')

        # Return the PDF file
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                response = HttpResponse(pdf_content, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
                return response
        except IOError:
            return JsonResponse({'error': 'Failed to compile LaTeX.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)