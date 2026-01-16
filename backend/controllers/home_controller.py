from flask import Blueprint, render_template, request, jsonify
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
        if category == 'india':
            news_data = NewsAPIService.get_indian_news()
        else:
            news_data = NewsAPIService.get_top_headlines(category=category)
        articles = news_data.get('articles', [])
        return render_template('category.html', articles=articles, category=category)
    except Exception as e:
        return render_template('category.html', articles=[], category=category, error=str(e))

@bp.route('/api/refresh/<category>')
def refresh_news(category):
    try:
        if category == 'india':
            news_data = NewsAPIService.get_indian_news()
        else:
            news_data = NewsAPIService.get_top_headlines(category=category)
        articles = news_data.get('articles', [])
        return jsonify({'success': True, 'articles': articles})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api/category/<category>/load-more')
def load_more_category_news(category):
    try:
        page = request.args.get('page', 1, type=int)
        
        if category == 'india':
            news_data = NewsAPIService.get_indian_news(page_size=20)
        else:
            news_data = NewsAPIService.get_top_headlines(category=category, page=page)
        
        articles = news_data.get('articles', [])
        return jsonify({'success': True, 'articles': articles})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'articles': []})

@bp.route('/api/news/load-more')
def load_more_news():
    try:
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', '')
        q = request.args.get('q', '')
        
        if q:
            news_data = NewsAPIService.get_everything(q, page=page)
        else:
            news_data = NewsAPIService.get_top_headlines(category=category if category else None, page=page)
        
        articles = news_data.get('articles', [])
        return jsonify({'success': True, 'articles': articles})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'articles': []})