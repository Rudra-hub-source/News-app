from flask import Blueprint
from backend.controllers.article_controller import bp as articles_bp

api_bp = Blueprint('api', __name__)

# Register controllers under /api
api_bp.register_blueprint(articles_bp, url_prefix='/articles')
