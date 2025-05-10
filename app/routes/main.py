from flask import Blueprint, render_template
from app.models import Users, Post

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/main")
def index():
    info = []
    posts = []
    try:
        info = Users.query.all()
        posts = Post.query.order_by(Post.id.desc()).all()
    except Exception as e:
        print("Ошибка чтения из БД:", e)

    return render_template("index.html", title="Главная", list=info, posts=posts)
