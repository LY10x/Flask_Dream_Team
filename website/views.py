from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Team
from . import db

views = Blueprint('views', __name__)

@views.route('/teams', methods=['GET', 'POST'])
@login_required
def teams():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        data = request.get_json()
        gk = data.get('gk')
        cb = data.get('cb')
        cm = data.get('cm')
        wf = data.get('wf')
        st = data.get('st')

        if not all([gk, cb, cm, wf, st]):
            return jsonify({"error": "All fields must be filled out"}), 400
        else:
            new_team = Team(gk=gk, cb=cb, cm=cm, wf=wf, st=st, user_id=current_user.id)
            db.session.add(new_team)
            db.session.commit()
            return jsonify({"message": "Team created successfully"}), 201

    teams = Team.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, teams=teams)

@views.route('/teams/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@login_required
def team_detail(id):
    team = Team.query.get_or_404(id)
    if team.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    if request.method == 'GET':
        return jsonify(team.serialize()), 200

    if request.method in ['PUT', 'PATCH']:
        if request.content_type != 'application/json':
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        data = request.get_json()
        if request.method == 'PUT':
            team.gk = data.get('gk', team.gk)
            team.cb = data.get('cb', team.cb)
            team.cm = data.get('cm', team.cm)
            team.wf = data.get('wf', team.wf)
            team.st = data.get('st', team.st)
            db.session.commit()
            return jsonify({'message': 'Team updated successfully'}), 200

        if request.method == 'PATCH':
            if 'gk' in data:
                team.gk = data['gk']
            if 'cb' in data:
                team.cb = data['cb']
            if 'cm' in data:
                team.cm = data['cm']
            if 'wf' in data:
                team.wf = data['wf']
            if 'st' in data:
                team.st = data['st']
            db.session.commit()
            return jsonify({'message': 'Team attribute updated successfully'}), 200

    if request.method == 'DELETE':
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team deleted successfully'}), 204

    return jsonify({'error': 'Bad request'}), 400
