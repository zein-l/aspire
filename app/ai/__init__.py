# app/ai/__init__.py
from flask import Blueprint

ai = Blueprint('ai', __name__)

from . import utils
