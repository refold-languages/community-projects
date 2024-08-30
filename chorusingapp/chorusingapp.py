import os
import json
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MARKER_FOLDER'] = 'markers'
app.config['LOOP_FOLDER'] = 'loops'  # New folder for saved loops
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the upload, marker, and loop folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MARKER_FOLDER'], exist_ok=True)
os.makedirs(app.config['LOOP_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/list_files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/save_markers', methods=['POST'])
def save_markers():
    data = request.json
    filename = secure_filename(data['filename'])
    markers = data['markers']
    with open(os.path.join(app.config['MARKER_FOLDER'], f"{filename}.json"), 'w') as f:
        json.dump(markers, f)
    return jsonify({"status": "success"})

@app.route('/load_markers/<filename>')
def load_markers(filename):
    marker_file = os.path.join(app.config['MARKER_FOLDER'], f"{filename}.json")
    if os.path.exists(marker_file):
        with open(marker_file, 'r') as f:
            markers = json.load(f)
        return jsonify(markers)
    else:
        return jsonify([])

@app.route('/save_loop', methods=['POST'])
def save_loop():
    data = request.json
    loop_id = data['id']
    filename = data['filename']
    start = data['start']
    end = data['end']
    audio_src = data['audioSrc']
    
    loop_data = {
        'id': loop_id,
        'filename': filename,
        'start': start,
        'end': end,
        'audioSrc': audio_src
    }
    
    loop_file_path = os.path.join(app.config['LOOP_FOLDER'], f"{loop_id}.json")
    with open(loop_file_path, 'w') as f:
        json.dump(loop_data, f)
    
    print(f"Loop saved to: {loop_file_path}")  # Debug print
    
    return jsonify({"status": "success", "message": f"Loop saved successfully to {loop_file_path}"})

@app.route('/load_loops/<filename>')
def load_loops(filename):
    loops = []
    for file in os.listdir(app.config['LOOP_FOLDER']):
        if file.endswith('.json'):
            with open(os.path.join(app.config['LOOP_FOLDER'], file), 'r') as f:
                loop_data = json.load(f)
                if loop_data['filename'] == filename:
                    loops.append(loop_data)
    return jsonify(loops)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)