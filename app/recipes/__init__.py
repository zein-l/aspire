from flask import Blueprint

recipes = Blueprint('recipes', __name__, template_folder='templates')

from . import routes
