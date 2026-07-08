from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import os, uuid
from pathlib import Path
from pprint import pprint

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(__file__), 'results')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

session_photos = []
analysis_results = []

prompt_path = "openai_prompt.txt"
with open(prompt_path, "r", encoding="utf-8") as f:
    mildew_prompt = f.read()


@app.route('/')
def index():
    return redirect(url_for('upload'))

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    files = request.files.getlist('photos')
    if not files:
        return jsonify({'error': 'No files received'}), 400
    added = []
    for f in files:
        if f and f.filename:
            ext = Path(f.filename).suffix.lower()
            if ext not in ['.jpg','.jpeg','.png','.gif','.bmp','.tiff','.webp','.heic','.heif']:
                continue
            uid = uuid.uuid4().hex[:8]
            safe_name = f"{uid}_{Path(f.filename).name}"
            dest = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
            f.save(dest)
            entry = {'id': uid, 'filename': safe_name, 'original_name': f.filename,
                     'filepath': dest, 'url': f'/uploads/{safe_name}'}
            session_photos.append(entry)
            added.append(entry)
    return jsonify({'added': len(added), 'total': len(session_photos), 'photos': added})

@app.route('/api/photos')
def api_photos():
    return jsonify({'photos': session_photos})

@app.route('/api/clear', methods=['POST'])
def api_clear():
    for p in session_photos, analysis_results:
        try: os.remove(p['filepath'])
        except: pass
    session_photos.clear()
    analysis_results.clear()
    return jsonify({'ok': True})

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/analyze')
def analyze():
    return render_template('analyze.html', default_analysis_message=mildew_prompt)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    message = data.get('message', '')
    photos = list(session_photos)
    if not photos:
        return jsonify({'error': 'No photos to analyze'}), 400
    try:
        import analysis_backend
        results = analysis_backend.run(photos, message, app.config['RESULTS_FOLDER'])
    except Exception as e:
        return jsonify({'error': f'Backend error: {str(e)}'}), 500
    analysis_results.clear()
    analysis_results.extend(results)
    return jsonify({'ok': True, 'count': len(results)})

@app.route('/api/results')
def api_results():
    return jsonify({'results': analysis_results})

@app.route('/map')
def map_view():
    statistics_dict = {}
    try:
        import analysis_backend
        print("Running analysis")
        statistics_dict = analysis_backend.pull_statistics(analysis_results)
    except Exception as e:
        return jsonify({'error': f'Backend error: {str(e)}'}), 500
    
    pprint(statistics_dict, indent=4)
    return render_template('map.html', statistics = statistics_dict)

@app.route('/results/<path:filename>')
def serve_result(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
