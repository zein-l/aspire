from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from app.models import RecipeStatus

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    prep_time = IntegerField('Prep Time (minutes)', validators=[Optional(), NumberRange(min=0)])
    cuisine = StringField('Cuisine', validators=[Optional()])
    status = SelectField(
        'Status',
        choices=[(status.name, status.value) for status in RecipeStatus],
        default=RecipeStatus.TO_WRITE.name
    )
    submit = SubmitField('Submit')
