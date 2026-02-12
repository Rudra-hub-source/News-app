from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from backend.services.article_service import ArticleService

bp = Blueprint('articles', __name__)

@bp.route('/')
def index():
    try:
        q = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 9, type=int)
        
        articles, total, has_more = ArticleService.get_articles_paginated(q, page, per_page)
        return render_template('articles.html', articles=articles, q=q, page=page, total=total, has_more=has_more)
    except Exception as e:
        return f'Articles page error: {str(e)}', 500

@bp.route('/test')
def test():
    return 'Articles controller is working!'

@bp.route('/category/<category>')
def category(category):
    """Display articles filtered by category"""
    try:
        q = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 9, type=int)
        
        # Get category name for display
        categories = dict(ArticleService.get_all_categories())
        category_name = categories.get(category, category.title())
        
        articles, total, has_more = ArticleService.get_articles_paginated(q, page, per_page, category=category)
        
        return render_template(
            'articlecategory.html', 
            articles=articles, 
            category=category, 
            category_name=category_name,
            categories=ArticleService.get_all_categories(),
            q=q, 
            page=page, 
            total=total, 
            has_more=has_more
        )
    except Exception as e:
        return f'Category page error: {str(e)}', 500

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
        category = request.form.get('category', 'general').strip()
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('main.articles.create'))
        try:
            ArticleService.create_article(title, content, author, category)
            flash('Article created successfully!', 'success')
            return redirect(url_for('main.articles.index'))
        except Exception as e:
            flash(f'Error creating article: {str(e)}', 'error')
            return redirect(url_for('main.articles.create'))
    
    articles = ArticleService.get_articles()
    categories = ArticleService.get_all_categories()
    return render_template('article_create.html', articles=articles, categories=categories)

@bp.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    article = ArticleService.get_article(article_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', 'general').strip()
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('main.articles.edit', article_id=article_id))
        ArticleService.update_article(article_id, title, content, author, category)
        flash('Article updated successfully!', 'success')
        return redirect(url_for('main.articles.detail', article_id=article_id))
    
    from backend.models.media import Media
    article_images = Media.query.filter_by(article_id=article_id).all()
    categories = ArticleService.get_all_categories()
    return render_template('article_edit.html', article=article, article_images=article_images, categories=categories)

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

@bp.route('/like/<int:article_id>', methods=['POST'])
def like(article_id):
    try:
        article = ArticleService.get_article(article_id)
        article.likes += 1
        from backend.state import db
        db.session.commit()
        return jsonify({'success': True, 'likes': article.likes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/bookmark/<int:article_id>', methods=['POST'])
def bookmark(article_id):
    try:
        article = ArticleService.get_article(article_id)
        article.bookmarks += 1
        from backend.state import db
        db.session.commit()
        return jsonify({'success': True, 'bookmarks': article.bookmarks})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/api/articles')
def api_articles():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 9, type=int)
        q = request.args.get('q', '')
        
        articles, total, has_more = ArticleService.get_articles_paginated(q, page, per_page)
        
        return jsonify({
            'success': True,
            'articles': [{
                'id': a.id,
                'title': a.title,
                'content': a.content[:150] + '...' if len(a.content) > 150 else a.content,
                'author': a.author or 'Anonymous',
                'likes': a.likes,
                'bookmarks': a.bookmarks,
                'created_at': a.created_at.strftime('%b %d') if a.created_at else 'Recent'
            } for a in articles],
            'page': page,
            'total': total,
            'has_more': has_more
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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