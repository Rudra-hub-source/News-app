from flask import Flask
import os
from backend.state import db
from backend.router import main_bp
from backend.models.article import Article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

db.init_app(app)

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
