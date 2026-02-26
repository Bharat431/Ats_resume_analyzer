
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, render_template, jsonify, send_from_directory
from app.services.evaluation_service import evaluate
from app.services.claude_service import optimize_resume

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'app/templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'app/static'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        resume = data.get('resume', '')
        jd = data.get('jd', '')
        
        if not resume or not jd:
            return jsonify({'error': 'Missing resume or job description'}), 400
        
        results = evaluate(resume, jd)
        
        try:
            ai_suggestions = optimize_resume(resume, jd)
        except Exception as e:
            ai_suggestions = f"Note: Claude API disabled in demo mode."
        
        return jsonify({
            'success': True,
            'results': results,
            'ai_suggestions': ai_suggestions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'ATS Resume Agent'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" "*10 + "ATS RESUME AGENT - WEB SERVER")
    print("="*60)
    print("\nStarting Flask server...")
    print("Open browser and go to: http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
