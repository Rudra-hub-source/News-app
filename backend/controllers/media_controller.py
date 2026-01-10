from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from backend.services.media_service import MediaService
import os

bp = Blueprint('media', __name__)

@bp.route('/')
def index():
    media_files = MediaService.get_all_media()
    return render_template('media_library.html', media_files=media_files)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        media = MediaService.upload_image(file)
        if media:
            flash('Image uploaded successfully!', 'success')
            return redirect(url_for('main.media.index'))
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP files.', 'error')
    
    return render_template('media_upload.html')

@bp.route('/<int:media_id>')
def detail(media_id):
    media = MediaService.get_media(media_id)
    return render_template('media_detail.html', media=media)

@bp.route('/edit/<int:media_id>', methods=['GET', 'POST'])
def edit(media_id):
    media = MediaService.get_media(media_id)
    if request.method == 'POST':
        alt_text = request.form.get('alt_text', '')
        description = request.form.get('description', '')
        MediaService.update_media(media_id, alt_text, description)
        flash('Media updated successfully!', 'success')
        return redirect(url_for('main.media.detail', media_id=media_id))
    
    return render_template('media_edit.html', media=media)

@bp.route('/delete/<int:media_id>', methods=['POST'])
def delete(media_id):
    MediaService.delete_media(media_id)
    flash('Media deleted successfully!', 'success')
    return redirect(url_for('main.media.index'))

@bp.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory('../instance/uploads', filename)