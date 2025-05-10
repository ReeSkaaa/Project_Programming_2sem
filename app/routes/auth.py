from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users, Profiles
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()
            p = Profiles(name=request.form['name'], old=request.form['old'], city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            flash("Ошибка регистрации", "error")
        return redirect(url_for('main.index'))
    return render_template("register.html", title="Регистрация")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('psw')
        if not email or not password:
            flash("Заполните все поля.", "error")
            return render_template('login.html', title="Войти")
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.psw, password):
            session['user_email'] = user.email
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        else:
            flash("Неверный email или пароль", "error")
    return render_template("login.html", title="Войти")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route("/cabinet")
def cabinet():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = Users.query.get(session['user_id'])
    profile = Profiles.query.filter_by(user_id=user.id).first()
    return render_template('cabinet.html', user=user, profile=profile, title="Личный кабинет")
