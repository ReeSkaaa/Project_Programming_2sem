import pytest
import uuid
from werkzeug.security import generate_password_hash
from app import create_app, db as _db
from app.models import Users, Profiles

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        _db.create_all()  # Создаем базу данных для всего теста
        yield app
        _db.drop_all()  # Очищаем базу данных после выполнения всех тестов

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def db(app):
    return _db

@pytest.fixture()
def new_user(db):
    # Генерация уникального email для каждого теста
    unique_email = f'test{uuid.uuid4()}@example.com'
    user = Users(email=unique_email, psw=generate_password_hash('password'))
    db.session.add(user)
    db.session.flush()  # Сохраняем пользователя, но не коммитим в базу
    profile = Profiles(name='Test User', old=30, city='Test City', user_id=user.id)
    db.session.add(profile)
    db.session.commit()  # Сохраняем все изменения в базе данных
    return user
