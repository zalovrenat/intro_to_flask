from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from app import app
from .forms import LoginForm, SignUpForm, PostForm
from .models import User, db, Post, like2
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

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

@app.route('/login', methods=['GET','POST'])
def loginPage():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            
            # check if user is in database
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('homePage'))
                else:
                    flash('Incorrect username or password.', 'danger')
            else:
                flash('Incorrect username.', 'danger')
        else:
            flash('An error has occurred. Please submit a valid form.', 'danger')

            # return redirect(url_for('loginPage'))

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signUpPage():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            # add user to database
            user = User(username,email,password)

            db.session.add(user)
            db.session.commit()
            flash('Successfully created user.', 'success')
            return redirect(url_for('loginPage'))
        flash('An error has occurred. Please submit a valid form.', 'danger')
    
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('loginPage'))

# POSTS