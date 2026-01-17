from flask import Flask, render_template, request
import os
from pathlib import Path

# Database configuration with fallback
def get_database_uri():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    return 'postgresql://postgres:password@localhost:5432/news_app'

DATABASE_URI = get_database_uri()

# Ensure upload directory exists
upload_dir = Path('instance/uploads')
upload_dir.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, 
           template_folder='frontend/templates',
           static_folder='frontend/static')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

# Import after app creation to avoid circular imports
from backend.state import db
from backend.router import main_bp
from backend.models.article import Article
from backend.models.media import Media

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main_bp)

@app.route('/articles')
def articles_redirect():
    from backend.services.article_service import ArticleService
    q = request.args.get('q', '')
    articles = ArticleService.get_articles(q)
    return render_template('articles.html', articles=articles, q=q)

@app.route('/initdb')
def init_db():
    db.create_all()
    # Create a test article if none exist
    from backend.services.article_service import ArticleService
    if len(ArticleService.get_articles()) == 0:
        ArticleService.create_article('Test Article', 'This is a test article content.', 'Test Author')
    return 'Database initialized with test data!'

@app.route('/debug')
def debug():
    from backend.services.article_service import ArticleService
    articles = ArticleService.get_articles()
    return f'Found {len(articles)} articles in database'

if __name__ == '__main__':
    # Run on development port
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')
