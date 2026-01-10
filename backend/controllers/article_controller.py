from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from backend.services.article_service import ArticleService

bp = Blueprint('articles', __name__)

@bp.route('/')
def index():
    q = request.args.get('q', '')
    articles = ArticleService.get_articles(q)
    return render_template('articles.html', articles=articles, q=q)

@bp.route('/<int:article_id>')
def detail(article_id):
    article = ArticleService.get_article(article_id)
    return render_template('article_detail.html', article=article)

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
    return render_template('article_create.html')

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
    return render_template('article_edit.html', article=article)

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