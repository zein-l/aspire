from app.extensions import db
from app.models import RecipeStatus

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer, nullable=True)
    cuisine = db.Column(db.String(64), nullable=True)
    status = db.Column(db.Enum(RecipeStatus), default=RecipeStatus.TO_WRITE, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('recipes', lazy=True))
