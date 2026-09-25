# AI Study Material Organizer

A beginner-friendly full-stack website that lets students upload study PDFs/text files, automatically organize them by subject, extract text, create a short summary, generate study questions, and browse saved materials.

## Features
- Upload PDF, TXT, and DOCX study material
- Automatic subject/category detection
- Text extraction
- Local AI-style summary using keyword analysis
- Automatic revision questions
- Search and filter materials
- Responsive dashboard
- SQLite database

> The included AI layer is lightweight and local. No paid API key is required.

## Run on Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:5000

## Project Structure

```text
AI_Study_Material_Organizer/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── ai_engine.py
│   ├── database.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   └── material.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── uploads/
├── requirements.txt
├── run.py
└── README.md
```
