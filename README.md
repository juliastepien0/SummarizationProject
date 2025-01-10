# Project Name: Text Summarization App

## Introduction

This project is a Django-based web application that allows users to summarize text in various formats. The app supports input from:

- Plain text
- Uploaded files (TXT, PDF)
- URLs

The summaries are generated using a generative AI model.

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
2. Add the necessary sensitive variables to config.json (e.g., API keys).
   
Example config.json format:

```json
{
  "api_key": "your_api_key_here",
  "other_config": "your_other_value_here"
}

```
