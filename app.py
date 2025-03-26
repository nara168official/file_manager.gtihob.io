import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set your custom upload location here
app.config['UPLOAD_FOLDER'] = r'D:\Users\YourUsername\Documents\file_uploads'  # Windows
# app.config['UPLOAD_FOLDER'] = '/home/yourusername/file_uploads'  # Linux
# app.config['UPLOAD_FOLDER'] = '/Users/yourusername/file_uploads'  # Mac

app.config['MAX_CONTENT_LENGTH'] = 10000 * 1024 * 1024 * 1024  # 1000GB max file size
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', 'doc', 'docx', 'xls', 'mp3', 'mp4'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ... [rest of the code remains the same] ...
# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'status': 'success', 'filename': filename})
    
    return jsonify({'status': 'error', 'message': 'File not allowed'})

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'File not found'})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/share/<filename>')
def share_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        share_url = f"{request.host_url}download/{filename}"
        return jsonify({'status': 'success', 'share_url': share_url})
    return jsonify({'status': 'error', 'message': 'File not found'})

@app.route('/progress', methods=['POST'])
def upload_progress():
    # This is a simplified progress handler
    # In a real application, you might use WebSockets or Server-Sent Events
    return jsonify({'progress': 100})

if __name__ == '__main__':
    app.run(debug=True)
