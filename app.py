from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from sentence_transformers import SentenceTransformer, util
from werkzeug.utils import secure_filename
import os
import uuid
import PyPDF2
import docx
from extract_skills import extract_skills

app = Flask(__name__)
app.secret_key = 'resume_matcher_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Add context processor to provide user status to templates
@app.context_processor
def inject_user():
    return dict(current_user=None, user_authenticated=False)

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# Initialize the model
try:
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading SentenceTransformer model: {e}")
    sbert_model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(path):
    text = ""
    try:
        with open(path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(path):
    text = ""
    try:
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def analyze_resume(job_description, resume_text, resume_name, resume_id):
    try:
        # Extract skills from job description and resume content
        job_skills = extract_skills(job_description)
        resume_skills = extract_skills(resume_text)

        # Default similarity score
        similarity_score = 0.5

        # Compute semantic similarity using SBERT if available
        if sbert_model:
            job_embed = sbert_model.encode(job_description, convert_to_tensor=True)
            resume_embed = sbert_model.encode(resume_text, convert_to_tensor=True)
            similarity_score = util.pytorch_cos_sim(job_embed, resume_embed).item()
        
        # Cap similarity to avoid overfitting to semantic content
        similarity_score = min(similarity_score, 0.90)

        # Skill matching ratio
        matching_skills = [skill for skill in resume_skills if skill in job_skills]
        missing_skills = [skill for skill in job_skills if skill not in resume_skills]
        skill_match_score = len(matching_skills) / len(job_skills) if job_skills else 0

        # Final weighted ATS score (50% semantic + 50% skill match)
        final_score = ((similarity_score * 50) + (skill_match_score * 50)) * 100
        final_score = min(round(final_score, 2), 100.0)

        # Return result with detailed scoring components
        return {
    'id': resume_id,
    'name': resume_name,
    'match_score': final_score,
    'semantic_score': round(similarity_score * 100, 2),  # Add this
    'skill_score': round(skill_match_score * 100, 2),     # And this
    'matching_skills': matching_skills,
    'missing_skills': missing_skills,
    'content': resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
    'full_content': resume_text
}


    except Exception as e:
        print(f"Error analyzing resume {resume_name}: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'job_description' not in request.form or not request.form['job_description'].strip():
            flash('Please enter a job description.', 'danger')
            return redirect(url_for('index'))

        if 'resumes' not in request.files:
            flash('Please select at least one resume file.', 'danger')
            return redirect(url_for('index'))

        job_description = request.form['job_description'].strip()
        session['job_description'] = job_description
        
        try:
            job_skills = extract_skills(job_description)
            session['job_skills'] = job_skills
        except Exception as e:
            print(f"Error extracting job skills: {e}")
            session['job_skills'] = []

        batch_id = str(uuid.uuid4())
        session['batch_id'] = batch_id

        files = request.files.getlist('resumes')
        results = []
        processed_count = 0
        error_count = 0

        for file in files:
            if file and file.filename and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    file_id = str(uuid.uuid4())
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
                    file.save(file_path)

                    # Extract text based on file type
                    text = ""
                    if filename.lower().endswith('.pdf'):
                        text = extract_text_from_pdf(file_path)
                    elif filename.lower().endswith(('.docx', '.doc')):
                        text = extract_text_from_docx(file_path)

                    # Clean up the file after processing
                    try:
                        os.remove(file_path)
                    except:
                        pass

                    if text and text.strip():
                        result = analyze_resume(job_description, text, filename, file_id)
                        if result:
                            results.append(result)
                            processed_count += 1
                        else:
                            error_count += 1
                    else:
                        error_count += 1
                        print(f"No text extracted from {filename}")

                except Exception as e:
                    error_count += 1
                    print(f"Error processing file {file.filename}: {e}")

        session['results'] = results
        session['results_count'] = len(results)
        session['processed_count'] = processed_count
        session['error_count'] = error_count

        if results:
            # Sort by match score (highest first)
            results.sort(key=lambda x: x['match_score'], reverse=True)
            for idx, resume in enumerate(results):
                resume['rank'] = idx + 1  # 1-based ranking
            session['results'] = results
            flash(f'Successfully processed {processed_count} resumes!', 'success')
            if error_count > 0:
                flash(f'Warning: {error_count} files could not be processed.', 'warning')
            return redirect(url_for('results'))
        else:
            flash('No valid resumes were processed. Please check your files and try again.', 'danger')
            return redirect(url_for('index'))

    except Exception as e:
        print(f"Upload error: {e}")
        flash('An error occurred while processing your request. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    if 'results' not in session or not session['results']:
        flash('No results to display. Please upload resumes first.', 'warning')
        return redirect(url_for('index'))
    
    return render_template(
        'results.html',
        results=session['results'],
        results_count=session['results_count'],
        job_skills=session.get('job_skills', []),
        job_description=session.get('job_description', ''),
        processed_count=session.get('processed_count', 0),
        error_count=session.get('error_count', 0)
    )

@app.route('/resume/<resume_id>')
def view_resume(resume_id):
    if 'results' not in session:
        flash('No results available.', 'warning')
        return redirect(url_for('index'))
    
    resume = None
    for result in session['results']:
        if result['id'] == resume_id:
            resume = result
            break
    
    if not resume:
        flash('Resume not found.', 'danger')
        return redirect(url_for('results'))
    
    return render_template('resume.html', resume=resume, job_skills=session.get('job_skills', []))

@app.route('/clear')
def clear():
    session.clear()
    flash('Session cleared successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'model_loaded': sbert_model is not None,
        'upload_folder_exists': os.path.exists(UPLOAD_FOLDER)
    })

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum file size is 16MB.', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    flash('A server error occurred. Please try again.', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    flash('Page not found.', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)