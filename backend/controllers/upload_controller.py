from flask import Blueprint, request, current_app, send_from_directory
from backend.responses import ok, error
from backend.services.file_service import save_upload

bp = Blueprint('uploads_api', __name__)


@bp.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return error('No file provided', code=400)
    f = request.files['file']
    if f.filename == '':
        return error('Empty filename', code=400)
    try:
        filename = save_upload(f)
    except ValueError as e:
        return error(str(e), code=400)
    except Exception as e:
        return error('Upload failed: '+str(e), code=500)
    url = current_app.config.get('UPLOAD_URL_PREFIX', '/uploads') + '/' + filename
    return ok(data={'url': url})


@bp.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    folder = current_app.config.get('UPLOAD_FOLDER')
    return send_from_directory(folder, filename)
