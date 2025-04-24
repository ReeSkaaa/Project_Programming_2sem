from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from .models import Users, Profiles, Post
from . import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/main")
def index():
    info = []
    posts = []
    try:
        info = Users.query.all()
        posts = Post.query.order_by(Post.date.desc()).all()
    except Exception as e:
        print("Ошибка чтения из БД:", e)

    return render_template("index.html", title="Главная", list=info, posts=posts)

@main.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
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

        return redirect(url_for('main.index'))
    return render_template("register.html", title="Регистрация")

@main.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        post = Post(title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.index'))
        except:
            return 'При добавлении статьи произошла ошибка!'
    return render_template("create.html")

