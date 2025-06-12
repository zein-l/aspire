import pytest
from app.extensions import db
from app.recipes.models import Recipe
from app.models import RecipeStatus

REGISTER_DATA = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'password',
    'confirm_password': 'password'
}
LOGIN_DATA = {
    'email': 'test@example.com',
    'password': 'password'
}

def register_and_login(client):
    client.post('/auth/register', data=REGISTER_DATA, follow_redirects=True)
    client.post('/auth/login', data=LOGIN_DATA, follow_redirects=True)


def test_no_recipes_shows_empty_message(client):
    response = client.get('/recipes/')
    assert response.status_code == 200
    assert b'No recipes found' in response.data


def test_create_recipe(client, db):
    register_and_login(client)
    response = client.post('/recipes/new', data={
        'name': 'Test Recipe',
        'ingredients': 'Ing1, Ing2',
        'instructions': 'Mix well',
        'prep_time': 15,
        'cuisine': 'TestCuisine',
        'status': 'TO_WRITE'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Recipe added.' in response.data

    recipe = Recipe.query.filter_by(name='Test Recipe').first()
    assert recipe is not None
    assert recipe.ingredients == 'Ing1, Ing2'
    assert recipe.prep_time == 15
    assert recipe.cuisine == 'TestCuisine'
    assert recipe.status == RecipeStatus.TO_WRITE


def test_search_recipe_by_name_and_ingredient(client, db):
    register_and_login(client)
    # create two recipes
    r1 = Recipe(
        name='Apple Pie',
        ingredients='apple, sugar, flour',
        instructions='Bake',
        prep_time=30,
        cuisine='American',
        status=RecipeStatus.TO_WRITE
    )
    r2 = Recipe(
        name='Banana Bread',
        ingredients='banana, sugar, flour',
        instructions='Bake',
        prep_time=45,
        cuisine='American',
        status=RecipeStatus.TO_WRITE
    )
    db.session.add_all([r1, r2])
    db.session.commit()

    # search by name
    resp1 = client.get('/recipes/?name=Apple')
    assert b'Apple Pie' in resp1.data
    assert b'Banana Bread' not in resp1.data

    # search by ingredient
    resp2 = client.get('/recipes/?ingredient=banana')
    assert b'Banana Bread' in resp2.data
    assert b'Apple Pie' not in resp2.data


def test_edit_recipe(client, db):
    register_and_login(client)
    recipe = Recipe(
        name='Old Name',
        ingredients='ing',
        instructions='do',
        prep_time=10,
        cuisine='X',
        status=RecipeStatus.TO_WRITE
    )
    db.session.add(recipe)
    db.session.commit()

    response = client.post(f'/recipes/edit/{recipe.id}', data={
        'name': 'New Name',
        'ingredients': 'ing updated',
        'instructions': 'do updated',
        'prep_time': 20,
        'cuisine': 'Y',
        'status': 'TO_TRY'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Recipe updated.' in response.data

    updated = Recipe.query.get(recipe.id)
    assert updated.name == 'New Name'
    assert updated.ingredients == 'ing updated'
    assert updated.prep_time == 20
    assert updated.cuisine == 'Y'
    assert updated.status == RecipeStatus.TO_TRY


def test_change_status_and_delete_recipe(client, db):
    register_and_login(client)
    recipe = Recipe(
        name='Status Test',
        ingredients='x',
        instructions='y',
        prep_time=5,
        cuisine='Z',
        status=RecipeStatus.TO_WRITE
    )
    db.session.add(recipe)
    db.session.commit()

    # change status
    resp_status = client.post(f'/recipes/status/{recipe.id}/TO_TRY', follow_redirects=True)
    assert resp_status.status_code == 200
    assert b'Status changed.' in resp_status.data
    assert Recipe.query.get(recipe.id).status == RecipeStatus.TO_TRY

    # delete
    resp_del = client.post(f'/recipes/delete/{recipe.id}', follow_redirects=True)
    assert resp_del.status_code == 200
    assert b'Recipe deleted.' in resp_del.data
    assert Recipe.query.get(recipe.id) is None
