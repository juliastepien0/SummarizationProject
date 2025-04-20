import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import bleach
from django.core.exceptions import ValidationError
import re
import magic
import speech_recognition as sr

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 52428800
# 100MB - 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "52428800"
ALLOWED_MIME_TYPES = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "wav": "audio/x-wav",
}

# Configuring the generative AI model with the provided API key
with open("config.json", "r") as config_file:
    config = json.load(config_file)
key = config["GEMINI_KEY"]
if not key:
    raise Exception("API key not found in config.json")

genai.configure(api_key=key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def extract_text_from_input_field(text: str) -> str:
    """
    Extracts and returns text provided through an input field.

    Args:
        text (str): The input text to be returned.

    Returns:
        str: The same input text.
    """
    return text


def extract_text_from_txt(file) -> str:
    """
    Extracts text from a TXT file.

    Args:
        file: A file-like object representing the TXT file.

    Returns:
        str: Extracted text from the file, or an error message if reading fails.
    """
    try:
        text = file.read()  # Reading file content
        return text
    except Exception as e:
        return f"Error reading TXT file: {e}"


def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file: A file-like object representing the PDF file.

    Returns:
        str: Extracted text from the PDF, or an error message if reading fails.
    """
    try:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_docx(file) -> str:
    """
        Extracts text from a DOCX file.

        Args:
            file: A file-like object representing the DOCX file.

        Returns:
            str: Extracted text from the PDF, or an error message if reading fails.
    """
    try:
        doc = Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_audio(file) -> str:
    """
        Extracts text from an audio file using speech recognition.

        Args:
            file (str): A file-like object representing the audio file (mp3, wav, etc.)

        Returns:
            str: Transcribed text from the audio file.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Error understanding the audio."
    except sr.RequestError:
        return "Error connecting to the service."


def extract_text_from_url(url: str) -> str:
    """
    Extracts and returns the text content from a URL.

    Args:
        url (str): The URL from which to extract text.

    Returns:
        str: Extracted text from the webpage, or an error message if fetching fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure successful request
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except requests.RequestException as e:
        return f"Error fetching content from URL: {e}"


def generate_summary(form: str, length: str, language: str, text: str, granularity: str) -> str:
    """
    Generates a summary for the provided text based on specified parameters.

    Args:
        form (str): The desired form of the summary ('text' or 'bullet').
        length (str): The desired length of the summary as number of sentences (1-30).
        language (str): The language in which the summary should be written (e.g., 'en', 'pl').
        text (str): The input text to be summarized.
        granularity (str): The granularity in which the summary should be written ('general', 'detailed').

    Returns:
        str: The generated summary.
    """
    try:
        # Generating the summary using the generative AI model
        if form == "text":
            prompt = f"Summarize the given text in {language} in form of a {length} sentence text, the summary should be {granularity}: {text}."
            response = model.generate_content(prompt)
            cleaned_response = " ".join(response.text.split())  # Clean up extra spaces
            return cleaned_response
        elif form == "bullet":
            prompt = f"Summarize the given text in {language} in form of {length} bullet points with key information, the summary should be {granularity}: {text}."
            response = model.generate_content(prompt)
            response_list = response.text.split()
            for i in range(len(response_list)):
                if response_list[i] == "*":
                    response_list[i] = "\n*"
            formatted_response = " ".join(response_list)
            return formatted_response

    except Exception as e:
        return f"Error generating summary: {e}"

def extract_and_validate_url(text: str) -> str:
    """
    Extracts the first valid URL from the provided text and removes everything after it.

    Args:
        text (str): The input text potentially containing a URL.

    Returns:
        str: The extracted URL if valid, otherwise an empty string.
    """
    url_pattern = re.compile(r'https?://[^\s]+')
    match = url_pattern.search(text)

    if match:
        url = match.group()
        parsed_url = urlparse(url)
        if parsed_url.scheme in ["http", "https"]:
            return url

    return ""

def sanitize_input(text):
    """
        Sanitizes the input text by removing potentially harmful HTML while preserving allowed tags.

        Args:
            text (str): The input text to sanitize.

        Returns:
            str: The sanitized text with only the allowed HTML tags and attributes.
    """
    allowed_tags = ['b', 'i', 'u', 'strong', 'em', 'p']
    allowed_attributes = {'a': ['href'], 'img': ['src']}

    sanitized_text = bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes, strip=True)

    return sanitized_text

def validate_uploaded_file(file):
    """
        Validates an uploaded file based on its size, extension, and MIME type.

        Args:
            file: The uploaded file object.

        Raises:
            ValidationError: If the file exceeds the maximum allowed size,
                             has an unsupported extension, or its MIME type does not match expectations.

        Returns:
            file: The validated file object if it passes all checks.
    """
    if file.size > int(MAX_UPLOAD_SIZE):
        raise ValidationError(f"File is too large! Max size is {int(MAX_UPLOAD_SIZE)/(1024*1024)}MB.")

    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in ALLOWED_MIME_TYPES:
        raise ValidationError(f"File extension {file_extension} is not supported.")

    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(2048))
    file.seek(0)

    expected_mime = ALLOWED_MIME_TYPES.get(file_extension)
    if file_mime_type != expected_mime:
        raise ValidationError(f"Invalid file format. Expected {expected_mime}, but got {file_mime_type}.")

    return file