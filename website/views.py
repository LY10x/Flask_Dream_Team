from flask import Blueprint, render_template, request, flash
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

        if len(gk) < 1:
            flash("not a real player", category='error')
        elif len(cb) < 1:
            flash("not a real player", category='error')
        elif len(cm) < 1:
            flash("not a real player", category='error')
        elif len(wf) < 1:
            flash("not a real player", category='error')
        elif len(st) < 1:
            flash("not a real player", category='error')
        else:
            new_team = Team(gk=gk, cb=cb, cm=cm, wf=wf, st=st, user_id=current_user.id)
            db.session.add(new_team)
            db.session.commit()
            flash("Team posted", category='success')

    teams = Team.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", user=current_user, teams=teams)
