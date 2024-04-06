from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai # type: ignore
from .custom_gemini_api_key import GEMINI_API_KEY

# Configure the API with your key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

@csrf_exempt
@require_http_methods(["POST"])
def askQuestion(request):
    try:
        data = json.loads(request.body)
        question = data.get('question', '')

        if not question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        # Generate content based on the provided question
        response = model.generate_content(question)
        answer = getattr(response, 'text', 'No answer found')

        return JsonResponse({'answer': answer})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except KeyError:
        return JsonResponse({'error': 'Missing question key'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)