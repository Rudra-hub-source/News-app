from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')
# Uploads
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
app.config['UPLOAD_URL_PREFIX'] = '/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Register backend middleware and API blueprint (if available)
try:
    from backend import middleware, router as api_router
    middleware.request_logger(app)
    app.register_blueprint(api_router.api_bp, url_prefix='/api')
except Exception:
    # ignore if backend package not present or import fails
    pass

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.id} {self.title}>'

@app.route('/')
def index():
    q = request.args.get('q', '')
    if q:
        articles = Article.query.filter(
            Article.title.contains(q) | Article.content.contains(q)
        ).order_by(Article.created_at.desc()).all()
    else:
        articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('index.html', articles=articles, q=q)

@app.route('/article/<int:article_id>')
def detail(article_id):
    a = Article.query.get_or_404(article_id)
    return render_template('detail.html', article=a)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        author = request.form.get('author', '').strip()
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('create'))
        a = Article(title=title, content=content, author=author)
        db.session.add(a)
        db.session.commit()
        flash('Article created.', 'success')
        return redirect(url_for('index'), 303)
    return render_template('create.html')

@app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    a = Article.query.get_or_404(article_id)
    if request.method == 'POST':
        a.title = request.form['title'].strip()
        a.content = request.form['content'].strip()
        a.author = request.form.get('author', '').strip()
        db.session.commit()
        flash('Article updated.', 'success')
        return redirect(url_for('detail', article_id=a.id), 303)
    return render_template('edit.html', article=a)

@app.route('/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    a = Article.query.get_or_404(article_id)
    db.session.delete(a)
    db.session.commit()
    flash('Article deleted.', 'success')
    return redirect(url_for('index'), 303)

@app.route('/initdb')
def initdb():
    db.create_all()
    if Article.query.count() == 0:
        sample = Article(
            title='Welcome to News Manager',
            content='This is a sample article. Edit or delete it.',
            author='Admin'
        )
        db.session.add(sample)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
