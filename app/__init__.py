# app/__init__.py

from flask import Flask, redirect, url_for
from .config import config_by_name
from .extensions import db, migrate, login_manager
from .recipes import recipes as recipes_blueprint
from .users import users as users_blueprint
from .ai import ai as ai_blueprint

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    # ─── Flask-Login user loader ────────────────────────────────
    @login_manager.user_loader
    def load_user(user_id):
        from app.users.models import User
        return User.query.get(int(user_id))
    # ──────────────────────────────────────────────────────────────

    # Register blueprints
    app.register_blueprint(recipes_blueprint, url_prefix='/recipes')
    app.register_blueprint(users_blueprint, url_prefix='/auth')
    app.register_blueprint(ai_blueprint, url_prefix='/ai')

    # Redirect root to /recipes/
    @app.route('/')
    def index():
        return redirect(url_for('recipes.list_recipes'))

    return app
