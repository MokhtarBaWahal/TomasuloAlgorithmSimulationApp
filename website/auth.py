from datetime import date

import flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website._init_ import db
from flask_login import login_user, login_required, logout_user, current_user
#import mysql.connector

auth = Blueprint('auth', __name__)


def print_hello():
    return "Hello"


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        data = User.query.all()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                session['email'] = email
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        UserName = request.form.get('UserName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        birthdate = request.form.get('birthdate')
        favoriteteam = request.form.get('favoriteteam')
        gender = request.form.get('gender')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(UserName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=UserName,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            try:
                db.session.commit()
            except Exception as e:
                flash('Email already exists.', category='error')
                return redirect(url_for('auth.sign_up'))
            login_user(new_user, remember=True)
            today = date.today()
            age = birthdate.split("-")
            fa_age = date(int(age[0]), int(age[1]), int(age[2]))
            age_final = today.year - fa_age.year - ((today.month, today.day) < (fa_age.month, fa_age.day))
            print(age_final)

            try:
                session['email'] = email
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            except Exception as e:
                print(e)
                print("Error data not entered")
                flash('Error!', category='error')

    return render_template("sign_up.html", user=current_user)








