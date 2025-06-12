# app/recipes/routes.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import RecipeStatus
from .models import Recipe
from .forms import RecipeForm
from . import recipes

@recipes.route('/', methods=['GET'])
def list_recipes():
    name = request.args.get('name', '')
    ingredient = request.args.get('ingredient', '')
    cuisine = request.args.get('cuisine', '')
    prep_time = request.args.get('prep_time', type=int)

    query = Recipe.query
    if name:
        query = query.filter(Recipe.name.ilike(f'%{name}%'))
    if ingredient:
        query = query.filter(Recipe.ingredients.ilike(f'%{ingredient}%'))
    if cuisine:
        query = query.filter(Recipe.cuisine.ilike(f'%{cuisine}%'))
    if prep_time is not None:
        query = query.filter(Recipe.prep_time <= prep_time)

    recipes_list = query.all()
    return render_template('list.html', recipes=recipes_list)


@recipes.route('/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            name=form.name.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            prep_time=form.prep_time.data,
            cuisine=form.cuisine.data,
            status=RecipeStatus[form.status.data],
            user=current_user
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added.')
        return redirect(url_for('recipes.list_recipes'))
    return render_template('form.html', form=form)


@recipes.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        recipe.prep_time = form.prep_time.data
        recipe.cuisine = form.cuisine.data
        recipe.status = RecipeStatus[form.status.data]
        db.session.commit()
        flash('Recipe updated.')
        return redirect(url_for('recipes.list_recipes'))
    return render_template('form.html', form=form, recipe=recipe)


@recipes.route('/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted.')
    return redirect(url_for('recipes.list_recipes'))


@recipes.route('/status/<int:recipe_id>/<status>', methods=['POST'])
@login_required
def change_status(recipe_id, status):
    recipe = Recipe.query.get_or_404(recipe_id)
    if status in RecipeStatus.__members__:
        recipe.status = RecipeStatus[status]
        db.session.commit()
        flash('Status changed.')
    return redirect(url_for('recipes.list_recipes'))
