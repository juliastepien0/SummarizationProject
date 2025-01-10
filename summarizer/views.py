from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import extract_text_from_input_field, extract_text_from_txt, extract_text_from_pdf, extract_text_from_url, generate_summary

@csrf_exempt
def summarize_text(request):
    """
    This view handles the summarization of text based on the input type.
    It supports text, file (txt/pdf), and URL inputs.

    Args:
        request (HttpRequest): The HTTP request object containing the data.

    Returns:
        JsonResponse: A response with either the summary or an error message.
    """
    if request.method == 'POST':
        try:
            # Parsing the incoming JSON data from the frontend
            data = json.loads(request.body)
            input_type = data.get('input_type')  # 'text', 'file', 'url'
            form = data.get('form')  # 'text' or 'bullet points'
            length = data.get('length')  # 'short', 'medium', 'long'
            language = data.get('language')  # e.g., 'english', 'polish'
            text = None

            # Extract text based on input type
            if input_type == 'text':
                text = extract_text_from_input_field(data.get('text'))
            elif input_type == 'file':
                uploaded_file = request.FILES.get('file')
                if uploaded_file:
                    text = process_uploaded_file(uploaded_file)
                else:
                    return JsonResponse({'error': 'No file provided'}, status=400)
            elif input_type == 'url':
                text = extract_text_from_url(data.get('url'))

            if not text:
                return JsonResponse({'error': 'No valid text found'}, status=400)

            # Generate summary from the extracted text
            summary = generate_summary(form=form, length=length, language=language, text=text)

            # Return the summary in the response
            return JsonResponse({'summary': summary}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def process_uploaded_file(uploaded_file) -> str:
    """
    Process the uploaded file based on its extension and extract text.

    Args:
        uploaded_file (InMemoryUploadedFile): The uploaded file object.

    Returns:
        str: Extracted text from the file, or an error message if the format is unsupported.
    """
    try:
        if uploaded_file.name.endswith('.txt'):
            return extract_text_from_txt(uploaded_file)
        elif uploaded_file.name.endswith('.pdf'):
            return extract_text_from_pdf(uploaded_file)
        else:
            return None
    except Exception as e:
        return f"Error processing file: {e}"