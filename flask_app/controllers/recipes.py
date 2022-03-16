import re
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route ('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)

    # todos los formularios se reciben con request.form ['key'] puedo enviar mi formlario completo
    return render_template('/new_recipe.html', user=user)

@app.route ('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')

    # fourmulario ={
    #     'name': request.form['name'],
    #     'description': request.form['description'],
    #     'instructions': request.form['instructions'],
    #     'date_made': request.form['date_made'],
    #     'user_id': request.form['user_id'],
    #     'under30': request.form['under30']
    # }

    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    Recipe.save(request.form)
    return redirect ('/dashboard')

@app.route ('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)
    data_receta = {
        'id':id
    }
    recipe =Recipe.get_by_id(data_receta)

    # todos los formularios se reciben con request.form ['key'] puedo enviar mi formlario completo
    return render_template('/edit_recipe.html', user=user, recipe=recipe)

@app.route ("/update/recipe", methods=["POST"])
def update_recipe():
    if 'user_id' not in session:
        return redirect ('/')

    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id'])
    
    Recipe.update(request.form)

    return redirect ("/dashboard")

@app.route ('/show/recipe/<int:id>')
def show_recipe (id):
    if 'user_id' not in session:
        return redirect('/')

    data_receta = {
        "id": id
    }
    recipe = Recipe.get_by_id(data_receta)

    return render_template("show_recipe.html", recipe=recipe)


@app.route ("/delete/recipe/<int:id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        "id":id
    }

    Recipe.delete (data)
    return redirect("/dashboard")

