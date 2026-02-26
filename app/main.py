"""ATS Resume Agent - Main Application"""
import sys
import os
from werkzeug.utils import secure_filename
import PyPDF2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, render_template, jsonify
from services.evaluation_service import evaluate
from services.claude_service import optimize_resume

# When this file is run as a script, Flask's root_path is the `app` directory.
# Templates live in `app/templates` and static files in `app/static`, so we
# point Flask directly at those directories.
BASE_DIR = os.path.dirname(__file__)
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'doc'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_pdf_text(filepath):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_docx_text(filepath):
    """Extract text from DOCX file"""
    try:
        from docx import Document
        doc = Document(filepath)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

def extract_text_file(filepath):
    """Extract text from TXT file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading TXT: {str(e)}")

def extract_file_text(filepath, filename):
    """Extract text from various file formats"""
    ext = filename.rsplit('.', 1)[1].lower()
    
    if ext == 'pdf':
        return extract_pdf_text(filepath)
    elif ext in ['docx', 'doc']:
        return extract_docx_text(filepath)
    elif ext == 'txt':
        return extract_text_file(filepath)
    else:
        raise Exception(f"Unsupported file format: {ext}")

@app.route('/', methods=['GET'])
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze resume against job description"""
    data = request.get_json()
    resume = data.get('resume', '')
    jd = data.get('jd', '')
    
    if not resume or not jd:
        return jsonify({'error': 'Missing resume or job description'}), 400
    
    results = evaluate(resume, jd)
    
    try:
        ai_suggestions = optimize_resume(resume, jd)
    except Exception as e:
        ai_suggestions = f"Note: Claude API disabled in demo. Error: {str(e)}"
    
    return jsonify({
        'results': results,
        'ai_suggestions': ai_suggestions
    })

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: PDF, DOCX, TXT'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        text = extract_file_text(filepath, filename)
        
    
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'text': text,
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/upload-jd', methods=['POST'])
def upload_jd():
    """Handle job description file upload"""
    try:
        if 'jd' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['jd']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: PDF, DOCX, TXT'}), 400
        
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
       
        text = extract_file_text(filepath, filename)
        
        
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'text': text,
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/health', methods=['GET'])
def health():
    """Lightweight health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'ATS Resume Agent'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)