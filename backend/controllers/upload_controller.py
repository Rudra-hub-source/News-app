from flask import Blueprint, request, jsonify
from backend.services.file_service import FileService

bp = Blueprint('uploads', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = FileService.save_file(file)
        return jsonify({'filename': filename}), 200
