from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
import os

bp = Blueprint('media', __name__)

@bp.route('/')
def index():
    try:
        from backend.models.media import Media
        from backend.state import db
        media_files = Media.query.order_by(Media.created_at.desc()).all()
        return render_template('media_library_simple.html', media_files=media_files)
    except Exception as e:
        # Fallback if there's any issue
        return render_template('media_library_simple.html', media_files=[])

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return redirect(url_for('main.media.index'))
    
    try:
        from backend.services.article_service import ArticleService
        articles = ArticleService.get_articles()
    except:
        articles = []
    
    return render_template('media_upload_simple.html', articles=articles)

@bp.route('/test')
def test():
    return 'Media section is working!'

@bp.route('/delete/<int:media_id>', methods=['POST'])
def delete(media_id):
    try:
        from backend.services.media_service import MediaService
        MediaService.delete_media(media_id)
        flash('Image deleted successfully!', 'success')
    except:
        flash('Error deleting image', 'error')
    
    # Redirect back to the referring page
    return redirect(request.referrer or url_for('main.media.index'))

@bp.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory('instance/uploads', filename)