Resume Ranker – NLP based tool
**Resume Ranker** is an intelligent resume screening web application built using Flask and NLP. It allows recruiters to upload multiple resumes and match them against a job description using semantic similarity and skill comparison. This speeds up the hiring process and improves candidate shortlisting accuracy.


🚀 Features

- 🔍 **AI-Based Resume Matching**  
  Leverages [Sentence-BERT (SBERT)](https://www.sbert.net) to calculate semantic similarity between resumes and job descriptions.

- 🧠 **Skill Extraction & Comparison**  
  Automatically extracts skills from resumes and job descriptions using spaCy or HuggingFace and compares overlap.

- 📊 **Smart Ranking System**  
  Calculates an **ATS-like match score** combining semantic and skill match (50/50 weighting).

- 📄 **Multi-Format Resume Support**  
  Upload resumes in `.pdf`, `.docx`, or `.doc` formats.

- 🖥️ **Modern UI with Visual Results**  
  View ranked results with match scores, matched/missing skills, and resume previews.

- 🔐 **Session-Based Tracking**  
  Secure session management for uploads and results.



🛠️ Tech Stack

| Layer      | Technology |
|------------|------------|
| Frontend   | HTML, CSS (Bootstrap), JavaScript |
| Backend    | Python (Flask) |
| NLP        | Sentence-BERT, spaCy |
| Parsing    | PyPDF2, python-docx |
| Database   | MySQL via XAMPP |
| Storage    | Local file system |
| Hosting    | Localhost (Flask), ready for cloud |



📸 Screenshots

![image]()
![image]()


⚙️ How It Works

1. Enter/paste a job description.
2. Upload one or more resumes.
3. The app:
   - Parses resume content (PDF/DOC/DOCX)
   - Extracts and compares skills
   - Uses SBERT for semantic similarity
   - Combines both into a final match score
4. Displays ranked resumes with skill insights and preview.


🔧 Setup Instructions

🖥️ Prerequisites
- Python 3.7+
- pip
- XAMPP (for MySQL) or any MySQL DB
- virtualenv (recommended)


Install dependencies
pip install -r requirements.txt


Credits
SBERT (Sentence-BERT)

spaCy NLP Toolkit


