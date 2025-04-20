# Project Name: AI Summarizer

## Introduction

This project is a Django-based web application that allows users to summarize text in various formats. The app supports input from:

- Plain text
- Uploaded text files and documents (TXT, PDF, DOCX)
- Uploaded audio files (WAV)
- URLs

Users are provided with various options of **summary configuration**, allowing choice of language, form (text or bullet points), length and level of detail. \
The summaries are generated using a generative AI model Gemini.

## Live application

This project is currently **deployed** on Render. \
**Go to https://ipz.onrender.com/ to try  it out.**
![audioSummary.png](Screenshots%2FaudioSummary.png)
## Installation

Follow the steps below to set up the project:

### 1. Clone the repository

Clone the repository from GitHub:

```bash
git clone https://github.com/juliastepien0/SummarizationProject.git
cd SummarizationProject
```

### 2. Set up the virtual environment

Create a virtual environment for the project:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

Install the required dependencies using requirements.txt:

```bash
pip install -r requirements.txt
```

## Configuration

This project uses a config.json file to store sensitive variables, such as API keys.

To configure the application:
1. Create a config.json file in the root directory of the project.
2. Add the necessary sensitive variables to config.json.
   
Needed config.json format:

```json
{
  "GEMINI_KEY": "your_api_key_here"
}

```
