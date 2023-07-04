from flask import render_template
from app import app

@app.route('/')
def homePage():

    people = ['Shoha','Sarah','Edward','Renat','Nick','Paul','Troy','Ousama']

    pokemons = [{
        'name': 'pikachu',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png'
    },{
        'name': 'ditto',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/132.png'
    }]
    
    return render_template('index.html', peeps = people, pokemons = pokemons)

@app.route('/contact')
def contactPage():
    return render_template('contact.html')

@app.route('/test')
def testPage():
    return {
        'test': 'testing'
    }

@app.route('/test2')
def testPage2():
    return {
        'test': 'testing'
    }