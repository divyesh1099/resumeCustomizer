from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings
import os
import subprocess
from tempfile import NamedTemporaryFile
import json
from django.views.decorators.csrf import csrf_exempt
import shutil
from django.templatetags.static import static
from django.contrib.staticfiles import finders

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
    
@csrf_exempt
def compile_latex(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        latex_code = data.get('code', '')
        filename = data.get('file', '')
        base_filename = os.path.splitext(filename)[0]

        # Find the path to 'resume.cls' in your static files
        cls_file_path = finders.find('load-file/resume.cls')

        # If the file is not found, return an error
        if cls_file_path is None:
            return JsonResponse({'error': 'resume.cls file not found in static directories.'}, status=400)

        with NamedTemporaryFile(suffix=".tex", delete=False) as texfile:
            texfile.write(latex_code.encode('utf-8'))
            texfile_path = texfile.name
        
        # Copy the cls file to the same directory as the tex file
        shutil.copy(cls_file_path, os.path.dirname(texfile_path))
        
        # Set up the environment for subprocess
        env = os.environ.copy()
        env['TEXINPUTS'] = os.path.dirname(cls_file_path) + "//:" + env.get('TEXINPUTS', '')
        
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', texfile_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(texfile_path),
                env=env  # Pass the modified environment to subprocess
            )
        except subprocess.CalledProcessError as e:
            error_details = {
                'stdout': e.stdout,
                'stderr': e.stderr,
            }
            print(f"pdflatex failed with stdout: {e.stdout} and stderr: {e.stderr}")
            return JsonResponse({'error': 'Failed to compile LaTeX.', 'details': error_details}, status=400)
        except Exception as e:
            os.unlink(texfile_path)  # Cleanup temp file
            return JsonResponse({
                'error': 'An error occurred during compilation.',
                'details': str(e)
            }, status=500)
        
        pdf_path = texfile_path.replace('.tex', '.pdf')

        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{base_filename}.pdf"'
            os.unlink(texfile_path)  # Cleanup temp .tex file
            os.unlink(pdf_path)  # Cleanup temp .pdf file
            return response
        else:
            os.unlink(texfile_path)  # Cleanup temp file
            return JsonResponse({
                'error': 'PDF file not generated.',
                'details': result.stderr
            }, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)