from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
import os
from flask import session, flash
from werkzeug.security import check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100), nullable=True)
    extra_information = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route("/main")
@app.route("/")
def index():
    info = []
    posts = []
    try:
        info = Users.query.all()
        posts = Post.query.order_by(Post.id.desc()).all()
    except Exception as e:
        print("Ошибка чтения из БД:", e)

    return render_template("index.html", title="Главная", list=info, posts=posts)


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('index'))

    return render_template("register.html", title="Регистрация")

@app.route('/create', methods=['POST', 'GET'])
def create():
    if 'user_id' not in session:
        flash("Сначала войдите в аккаунт, чтобы создать пост.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        post = Post(title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'При добавлении статьи произошла ошибка!'
    else:
        return render_template('create.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Проверяем, есть ли в запросе параметр email
        email = request.form.get('email')  # Используем .get() чтобы избежать ошибки KeyError
        password = request.form.get('psw')  # То же самое для пароля

        # Если параметр email не найден в запросе
        if not email or not password:
            flash("Заполните все поля.", "error")
            return render_template('login.html', title="Войти")

        # Пытаемся найти пользователя по email
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.psw, password):
            # Если пользователь найден и пароль совпадает, устанавливаем сессию
            session['user_email'] = user.email
            session['user_id'] = user.id
            return redirect(url_for('index'))  # Перенаправление на главную страницу или страницу личного кабинета

        else:
            # Если email или пароль неправильные
            flash("Неверный email или пароль", "error")

    return render_template('login.html', title="Войти")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/cabinet')
def cabinet():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = Users.query.get(session['user_id'])
    profile = Profiles.query.filter_by(user_id=user.id).first()

    return render_template('cabinet.html', user=user, profile=profile, title="Личный кабинет")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
