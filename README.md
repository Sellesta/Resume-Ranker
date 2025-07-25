# 💼 Resume Ranker – AI-Powered Resume Screening Tool

**Resume Ranker** is an intelligent resume screening web application built with **Flask** and **Natural Language Processing (NLP)**. It helps recruiters rapidly match multiple resumes against a job description using **semantic similarity** and **skill extraction**, enabling faster, smarter, and more accurate shortlisting of candidates.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue?logo=python&style=flat-square"/>
  <img src="https://img.shields.io/badge/Flask-2.x-black?logo=flask&style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square"/>
</p>

---

## 🚀 Features

- 🔍 **AI-Based Resume Matching**  
  Uses [Sentence-BERT (SBERT)](https://www.sbert.net) to compute semantic similarity between job descriptions and resumes.

- 🧠 **Automatic Skill Extraction & Comparison**  
  Extracts relevant skills using spaCy or HuggingFace and compares them with the job requirements.

- 📊 **Smart Ranking Algorithm**  
  Generates an **ATS-style match score** by combining semantic similarity and skill overlap (50/50 weight).

- 📄 **Supports Multiple Resume Formats**  
  Accepts `.pdf`, `.docx`, and `.doc` files.

- 🖥️ **User-Friendly Interface**  
  Ranks candidates with interactive results, highlights matching/missing skills, and offers resume previews.

- 🔐 **Secure Session Tracking**  
  Manages file uploads and results securely using Flask sessions.

---

## 🧠 Tech Stack

| Layer      | Technologies Used |
|------------|-------------------|
| **Frontend** | HTML, CSS (Bootstrap), JavaScript |
| **Backend**  | Python, Flask |
| **NLP**       | Sentence-BERT, spaCy |
| **Parsing**   | PyPDF2, python-docx |
| **Database**  | MySQL (via XAMPP) |
| **Storage**   | Local file system |
| **Hosting**   | Flask (localhost), cloud-ready |

---

## ⚙️ How It Works

1. Paste a **job description** into the form.
2. Upload one or more **resumes** in PDF or DOC format.
3. The app:
   - Extracts resume text
   - Extracts and matches relevant skills
   - Uses SBERT for semantic similarity
   - Computes an overall match score
4. Displays a **ranked list of candidates** with:
   - Total match score
   - Overlapping and missing skills
   - Resume preview

---

## 🛠 Installation & Setup

Follow these steps to run Resume Ranker locally on your machine.

---

### 🚀 Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sellesta/Resume-Ranker.git
   cd Resume-Ranker
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **For spaCy**
   ```bash
   python -m spacy download en_core_web_sm
3. **Run the Flask App**
   ```bash
   python app.py

---

## 🖼 Screenshots


![Home Page](https://raw.githubusercontent.com/Sellesta/Resume-Ranker/main/Screenshot%202025-07-03%20165134.png)
![Home Page](https://raw.githubusercontent.com/Sellesta/Resume-Ranker/main/Screenshot%202025-07-03%20165231.png)
![Home Page](https://raw.githubusercontent.com/Sellesta/Resume-Ranker/main/Screenshot%202025-07-03%20164943.png)
![Result Page](https://raw.githubusercontent.com/Sellesta/Resume-Ranker/main/Screenshot%202025-07-03%20164918.png)



