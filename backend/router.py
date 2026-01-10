
from flask import Blueprint
from backend.controllers.home_controller import bp as home_bp
from backend.controllers.article_controller import bp as articles_bp
from backend.controllers.upload_controller import bp as uploads_bp

main_bp = Blueprint('main', __name__)

# Register controllers
main_bp.register_blueprint(home_bp)
main_bp.register_blueprint(articles_bp, url_prefix='/articles')
main_bp.register_blueprint(uploads_bp, url_prefix='/uploads')
