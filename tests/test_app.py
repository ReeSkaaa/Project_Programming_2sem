import pytest
from app import create_app, db
from app.models import Users, Profiles, Post
from werkzeug.security import check_password_hash


# --- Фикстура приложения ---
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


# --- Фикстура клиента ---
@pytest.fixture
def client(app):
    return app.test_client()


# --- Тест: главная страница ---
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Главная" in response.data.decode("utf-8")


# --- Тест: регистрация пользователя и профиля ---
def test_register_user(client, app):
    response = client.post('/register', data={
        'email': 'test@example.com',
        'psw': 'secure_password',
        'name': 'John Doe',
        'old': 30,
        'city': 'Moscow'
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        user = Users.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert check_password_hash(user.psw, 'secure_password')

        profile = Profiles.query.filter_by(user_id=user.id).first()
        assert profile is not None
        assert profile.name == 'John Doe'
        assert profile.city == 'Moscow'


# --- Тест: создание поста ---
def test_create_post(client, app):
    response = client.post('/create', data={
        'title': 'Test Post',
        'text': 'This is the content of the post.'
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        post = Post.query.filter_by(title='Test Post').first()
        assert post is not None
        assert post.text == 'This is the content of the post.'
