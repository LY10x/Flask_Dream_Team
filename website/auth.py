from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify # type: ignore
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from . import db
from flask_login import login_user, login_required, logout_user, current_user # type: ignore

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True) 
                response = redirect(url_for('views.teams'))
                response.status_code = 200
                return response
            else:
                return jsonify({'error': 'Incorrect password, try again.'}), 400
        else:
            return jsonify({'error': 'Email does not exist.'}), 404

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        email = data.get('email')
        first_name = data.get('firstName')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'error': 'User already exists'}), 400

        if len(email) < 4:
            return jsonify({"error": "Email must be longer than 3 characters"}), 400
        elif len(first_name) < 2:
            return jsonify({"error": "First name must be longer than 2 characters"}), 400
        elif password1 != password2:
            return jsonify({"error": "Passwords don't match"}), 400
        elif len(password1) < 7:
            return jsonify({"error": "Password must be longer than 7 characters"}), 400
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            response = redirect(url_for('views.teams'))
            response.status_code = 201
            return response

    return render_template("sign_up.html", user=current_user)
