from flask import Blueprint, render_template, request
from backend.services.news_api_service import NewsAPIService

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    try:
        category = request.args.get('category', '')
        q = request.args.get('q', '')

        if q:
            news_data = NewsAPIService.get_everything(q)
        else:
            news_data = NewsAPIService.get_top_headlines(category=category if category else None)

        articles = news_data.get('articles', [])
        return render_template('home.html', articles=articles, category=category, q=q)
    except Exception as e:
        return render_template('home.html', articles=[], error=str(e))

@bp.route('/category/<category>')
def category_news(category):
    try:
        news_data = NewsAPIService.get_top_headlines(category=category)
        articles = news_data.get('articles', [])
        return render_template('category.html', articles=articles, category=category)
    except Exception as e:
        return render_template('category.html', articles=[], category=category, error=str(e))