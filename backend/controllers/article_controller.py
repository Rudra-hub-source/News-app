from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.services.article_service import ArticleService

bp = Blueprint('articles', __name__)

@bp.route('/')
def index():
    q = request.args.get('q', '')
    articles = ArticleService.get_articles(q)
    return render_template('index.html', articles=articles, q=q)

@bp.route('/article/<int:article_id>')
def detail(article_id):
    article = ArticleService.get_article(article_id)
    return render_template('detail.html', article=article)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        author = request.form.get('author', '').strip()
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('articles.create'))
        ArticleService.create_article(title, content, author)
        flash('Article created successfully!', 'success')
        return redirect(url_for('articles.index'))
    return render_template('create.html')

@bp.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    article = ArticleService.get_article(article_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        author = request.form.get('author', '').strip()
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('articles.edit', article_id=article_id))
        ArticleService.update_article(article_id, title, content, author)
        flash('Article updated successfully!', 'success')
        return redirect(url_for('articles.detail', article_id=article_id))
    return render_template('edit.html', article=article)

@bp.route('/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    ArticleService.delete_article(article_id)
    flash('Article deleted successfully!', 'success')
    return redirect(url_for('articles.index'))

@bp.route('/initdb')
def initdb():
    from backend.state import db
    from backend.models.article import Article
    db.create_all()
    if Article.query.count() == 0:
        sample = Article(
            title='Welcome to News Manager',
            content='This is a sample article. Edit or delete it.',
            author='Admin'
        )
        db.session.add(sample)
        db.session.commit()
    return redirect(url_for('articles.index'))