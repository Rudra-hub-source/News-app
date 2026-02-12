from backend.state import db
from backend.models.article import Article, ARTICLE_CATEGORIES, Category
from datetime import datetime, timedelta

class ArticleService:
    # Import ARTICLE_CATEGORIES for use in templates
    CATEGORIES = ARTICLE_CATEGORIES
    
    @staticmethod
    def get_all_categories():
        """Get all categories (predefined + custom)"""
        # Start with predefined categories
        all_cats = list(ARTICLE_CATEGORIES)
        
        # Add custom categories from database
        try:
            custom_cats = Category.query.order_by(Category.created_at.desc()).all()
            for cat in custom_cats:
                # Avoid duplicates
                if not any(c[0] == cat.name for c in all_cats):
                    all_cats.append((cat.name, cat.display_name))
        except Exception:
            pass
        
        return all_cats
    
    @staticmethod
    def get_or_create_category(category_name):
        """Get or create a custom category"""
        # Check if it's a predefined category
        predefined = [c[0] for c in ARTICLE_CATEGORIES]
        if category_name.lower() in predefined:
            return category_name.lower()
        
        # Check if custom category exists
        try:
            existing = Category.query.filter_by(name=category_name.lower()).first()
            if existing:
                return existing.name
            
            # Create new custom category
            new_cat = Category(
                name=category_name.lower(),
                display_name=category_name.title()
            )
            db.session.add(new_cat)
            db.session.commit()
            return new_cat.name
        except Exception as e:
            db.session.rollback()
            return category_name.lower()
    
    @staticmethod
    def get_articles(q=''):
        if q:
            articles = Article.query.filter(
                Article.title.contains(q) | Article.content.contains(q)
            ).order_by(Article.created_at.desc()).all()
        else:
            articles = Article.query.order_by(Article.created_at.desc()).all()
        return articles

    @staticmethod
    def get_articles_by_category(category, q=''):
        """Get articles filtered by category"""
        query = Article.query.filter_by(category=category)
        if q:
            query = query.filter(
                Article.title.contains(q) | Article.content.contains(q)
            )
        return query.order_by(Article.created_at.desc()).all()

    @staticmethod
    def get_article(article_id):
        article = Article.query.get_or_404(article_id)
        article.view_count = (article.view_count or 0) + 1
        db.session.commit()
        return article

    @staticmethod
    def get_trending_articles(limit=10):
        return Article.query.order_by(Article.view_count.desc()).limit(limit).all()
    
    @staticmethod
    def get_latest_articles(limit=10):
        return Article.query.order_by(Article.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_latest_by_category(category, limit=5):
        """Get latest articles by category"""
        return Article.query.filter_by(category=category).order_by(Article.created_at.desc()).limit(limit).all()

    @staticmethod
    def create_article(title, content, author='Anonymous', category='general'):
        # Ensure category exists (either predefined or custom)
        category = ArticleService.get_or_create_category(category)
        a = Article(title=title, content=content, author=author or 'Anonymous', category=category)
        db.session.add(a)
        db.session.commit()
        return a

    @staticmethod
    def update_article(article_id, title, content, author, category='general'):
        # Ensure category exists (either predefined or custom)
        category = ArticleService.get_or_create_category(category)
        a = Article.query.get_or_404(article_id)
        a.title = title
        a.content = content
        a.author = author or 'Anonymous'
        a.category = category
        db.session.commit()
        return a

    @staticmethod
    def delete_article(article_id):
        a = Article.query.get_or_404(article_id)
        db.session.delete(a)
        db.session.commit()
    
    @staticmethod
    def get_articles_paginated(q='', page=1, per_page=9, category=None):
        query = Article.query
        if q:
            query = query.filter(
                Article.title.contains(q) | Article.content.contains(q)
            )
        if category:
            query = query.filter_by(category=category)
        query = query.order_by(Article.created_at.desc())
        
        total = query.count()
        articles = query.limit(per_page).offset((page - 1) * per_page).all()
        has_more = total > (page * per_page)
        
        return articles, total, has_more
