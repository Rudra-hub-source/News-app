import os
import uuid
from werkzeug.utils import secure_filename
from backend.models.media import Media
from backend.state import db

class MediaService:
    UPLOAD_FOLDER = 'instance/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in MediaService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def upload_image(file, article_id=None):
        if not file or not MediaService.allowed_file(file.filename):
            return None
        
        original_filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{original_filename}"
        file_path = os.path.join(MediaService.UPLOAD_FOLDER, filename)
        
        os.makedirs(MediaService.UPLOAD_FOLDER, exist_ok=True)
        file.save(file_path)
        
        media = Media(
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            mime_type=file.mimetype,
            article_id=article_id
        )
        db.session.add(media)
        db.session.commit()
        return media
    
    @staticmethod
    def get_all_media():
        return Media.query.order_by(Media.created_at.desc()).all()
    
    @staticmethod
    def get_media(media_id):
        return Media.query.get_or_404(media_id)
    
    @staticmethod
    def update_media(media_id, alt_text, description):
        media = Media.query.get_or_404(media_id)
        media.alt_text = alt_text
        media.description = description
        db.session.commit()
        return media
    
    @staticmethod
    def delete_media(media_id):
        media = Media.query.get_or_404(media_id)
        if os.path.exists(media.file_path):
            os.remove(media.file_path)
        db.session.delete(media)
        db.session.commit()