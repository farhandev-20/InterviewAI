# InterviewAI – AI Interview Preparation Platform

InterviewAI is a production-ready SaaS web application powered by **Google Gemini AI** designed for technical and HR interview preparation, ATS resume auditing, job matching, and candidate analytics. Inspired by the sleek aesthetic of Linear, Stripe Dashboard, and Notion, InterviewAI provides software engineers with real-time AI interview simulations, 5-metric response evaluations, voice dictation, speech replay, resume auditing, and job description skill matching.

---

## 🚀 Features (Phases 1 - 4)

- **Resume Intelligence & ATS Scoring**: Upload PDF or Word (.docx) resumes to extract skills, education, experience, and projects. Calculates an automated **7-metric ATS Score** (Skills, Keywords, Experience, Projects, Education, Readability, Formatting) with actionable improvement suggestions.
- **Job Description Matcher**: Compare candidate resumes against target job postings (PDF, DOCX, or text) to derive overall match %, hiring probability, missing keywords, and skill gap learning paths.
- **Personalized Resume-Based Interviews**: Generate interview questions tailored directly to the candidate's uploaded resume projects and technical history.
- **Gemini AI Interview Engine**: Dynamic question generation for 9 supported roles (Python, Frontend, Backend, Full Stack, Java, UI/UX, Data Analyst, ML Engineer, HR) and 5 question types (Technical, HR, Behavioral, Scenario Based, Problem Solving).
- **5-Metric Answer Evaluation**: Real-time scoring across **Technical Accuracy**, **Communication**, **Confidence**, **Grammar**, and **Relevance**.
- **Voice Capabilities**: Web Speech API integration for **Voice Dictation** (microphones) and **Speech Replay** (listening to questions spoken aloud).
- **Reports & Skill Analytics**: Interactive Chart.js radar charts and printable PDF evaluation reports.
- **Authentication System**: Registration, PBKDF2:SHA256 password hashing, Flask-Login user sessions, and Remember Me support.

---

## 📂 Supported Resume File Formats

- **PDF Documents** (`.pdf`) via `pypdf`
- **Microsoft Word Documents** (`.docx`, `.doc`) via `python-docx`
- **Plain Text Files** (`.txt`, `.md`)

---

## 🔑 Gemini API Setup

1. Obtain a free or paid API key from [Google AI Studio](https://aistudio.google.com/).
2. Add your API key to your `.env` file:
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```
*Note: If `GEMINI_API_KEY` is missing or network is offline, InterviewAI automatically uses its resilient structured fallback evaluation engine so the application never crashes.*

---

## 📄 `.env` Example

```env
SECRET_KEY=interviewai_super_secret_key_9837492817398127391
FLASK_ENV=development
DATABASE_URL=sqlite:///interviewai.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS3 (CSS Variables, Glassmorphism), Vanilla JavaScript, Web Speech API
- **Backend**: Python Flask
- **Database & ORM**: SQLite, SQLAlchemy ORM (`Flask-SQLAlchemy`)
- **Document Parsing**: `pypdf`, `python-docx`
- **Authentication**: `Flask-Login`, `Werkzeug.security`
- **AI Integration**: Google Gemini API (`services/gemini_service.py`)
- **Visualization & Icons**: Chart.js, Font Awesome 6

---

## ⚡ Installation & Setup Guide

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```

Navigate to `http://127.0.0.1:5000` in your web browser.
