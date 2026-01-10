import os
from werkzeug.utils import secure_filename

class FileService:
    UPLOAD_FOLDER = 'instance/uploads'

    @staticmethod
    def save_file(file):
        if not os.path.exists(FileService.UPLOAD_FOLDER):
            os.makedirs(FileService.UPLOAD_FOLDER)
        filename = secure_filename(file.filename)
        file_path = os.path.join(FileService.UPLOAD_FOLDER, filename)
        file.save(file_path)
        return filename
