from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Team
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        gk = request.form.get('gk')
        cb = request.form.get('cb')
        cm = request.form.get('cm')
        wf = request.form.get('wf')
        st = request.form.get('st')

        if not all([gk, cb, cm, wf, st]):
            flash("All fields must be filled out", category='error')
        else:
            new_team = Team(gk=gk, cb=cb, cm=cm, wf=wf, st=st, user_id=current_user.id)
            db.session.add(new_team)
            db.session.commit()
            flash("Team posted", category='success')
            return redirect(url_for('views.home'))

    teams = Team.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, teams=teams)

@views.route('/teams/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def update_or_delete_team(id):
    team = Team.query.get_or_404(id)
    if team.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    if request.method == 'PUT':
        data = request.get_json()
        team.gk = data.get('gk', team.gk)
        team.cb = data.get('cb', team.cb)
        team.cm = data.get('cm', team.cm)
        team.wf = data.get('wf', team.wf)
        team.st = data.get('st', team.st)
        db.session.commit()
        return jsonify({'message': 'Team updated successfully'}), 200

    if request.method == 'DELETE':
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team deleted successfully'}), 204

    return jsonify({'error': 'Bad request'}), 400
