from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from backend.services.article_service import ArticleService

bp = Blueprint('articles', __name__)

@bp.route('/')
def index():
    try:
        q = request.args.get('q', '')
        articles = ArticleService.get_articles(q)
        return render_template('articles.html', articles=articles, q=q)
    except Exception as e:
        return f'Articles page error: {str(e)}', 500

@bp.route('/test')
def test():
    return 'Articles controller is working!'

@bp.route('/<int:article_id>')
def detail(article_id):
    article = ArticleService.get_article(article_id)
    from backend.models.media import Media
    article_images = Media.query.filter_by(article_id=article_id).all()
    return render_template('article_detail.html', article=article, article_images=article_images)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        author = request.form.get('author', 'Anonymous').strip() or 'Anonymous'
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('main.articles.create'))
        try:
            ArticleService.create_article(title, content, author)
            flash('Article created successfully!', 'success')
            return redirect(url_for('main.articles.index'))
        except Exception as e:
            flash(f'Error creating article: {str(e)}', 'error')
            return redirect(url_for('main.articles.create'))
    
    articles = ArticleService.get_articles()
    return render_template('article_create.html', articles=articles)

@bp.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    article = ArticleService.get_article(article_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        author = request.form.get('author', '').strip()
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('main.articles.edit', article_id=article_id))
        ArticleService.update_article(article_id, title, content, author)
        flash('Article updated successfully!', 'success')
        return redirect(url_for('main.articles.detail', article_id=article_id))
    
    from backend.models.media import Media
    article_images = Media.query.filter_by(article_id=article_id).all()
    return render_template('article_edit.html', article=article, article_images=article_images)

@bp.route('/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    ArticleService.delete_article(article_id)
    flash('Article deleted successfully!', 'success')
    return redirect(url_for('main.articles.index'))

@bp.route('/init')
def init_db():
    from backend.state import db
    db.create_all()
    flash('Database initialized!', 'success')
    return redirect(url_for('main.articles.index'))

@bp.route('/trending')
def trending():
    articles = ArticleService.get_trending_articles()
    return render_template('trending_articles.html', articles=articles)

@bp.route('/latest')
def latest():
    articles = ArticleService.get_latest_articles()
    return render_template('latest_articles.html', articles=articles)

@bp.route('/upload-image/<int:article_id>', methods=['POST'])
def upload_image(article_id):
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('main.articles.edit', article_id=article_id))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('main.articles.edit', article_id=article_id))
    
    try:
        import os
        import uuid
        from werkzeug.utils import secure_filename
        from backend.models.media import Media
        from backend.state import db
        
        # Simple upload logic
        original_filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{original_filename}"
        upload_folder = 'instance/uploads'
        file_path = os.path.join(upload_folder, filename)
        
        os.makedirs(upload_folder, exist_ok=True)
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
        
        flash('Image uploaded successfully!', 'success')
    except Exception as e:
        flash(f'Error uploading image: {str(e)}', 'error')
    
    return redirect(url_for('main.articles.edit', article_id=article_id))