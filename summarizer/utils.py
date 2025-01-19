import google.generativeai as genai
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
import json

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
        form (str): The desired form of the summary ('text' or 'bullet points').
        length (str): The desired length of the summary ('short', 'medium', 'long').
        language (str): The language in which the summary should be written (e.g., 'english', 'polish').
        text (str): The input text to be summarized.

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
        elif form == "bullet points":
            prompt = f"Summarize the given text in {language} in form of {length} bullet points with key information, the summary should be {granularity}: {text}."
            response = model.generate_content(prompt)
            cleaned_response = " ".join(response.text.split())  # Clean up extra spaces
            return cleaned_response
    except Exception as e:
        return f"Error generating summary: {e}"