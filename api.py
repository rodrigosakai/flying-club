"""
Flask API
"""
from flask import Flask
from src.blueprints.auth import auth_bp
from src.blueprints.users import users_bp

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp, url_prefix="/users")
