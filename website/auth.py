from flask import Blueprint, render_template, request, flash  # type: ignore

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')

        if len(email) < 4:
            flash("email must be longer than 3 letters", category='error')
        elif len(fname) < 2:
            flash("Firstname must be longer than 2 letters", category='error')
        elif pass1 != pass2:
            flash("passwords dont match", category='error')
        elif len(pass1) < 7:
             flash("passwords must be longer than 7 char", category='error')
        else:
            flash('Account created!', category='success')
    return render_template("sign_up.html")