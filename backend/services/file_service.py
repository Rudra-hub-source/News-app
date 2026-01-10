import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_filename(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload(file_storage) -> str:
    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    if not upload_folder:
        raise RuntimeError('UPLOAD_FOLDER not configured')
    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(file_storage.filename)
    if not allowed_filename(filename):
        raise ValueError('Invalid file type')
    path = os.path.join(upload_folder, filename)
    file_storage.save(path)
    # return relative path for serving
    return filename
