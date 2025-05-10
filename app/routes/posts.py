from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Post
from app import db

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        flash("Сначала войдите в аккаунт, чтобы создать пост.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        post = Post(title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.index'))
        except:
            return 'Ошибка при добавлении поста!'
    return render_template('create.html')
