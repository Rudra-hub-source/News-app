from flask import Flask, render_template, request
import os
from pathlib import Path
from backend.state import db
from backend.router import main_bp
from backend.models.article import Article
from backend.models.media import Media

# Get the absolute path to the database
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / 'database' / 'instance' / 'news.db'

app = Flask(__name__, 
           template_folder='frontend/templates',
           static_folder='frontend/static')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

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
