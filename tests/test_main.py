from app.models import Users, Profiles
import pytest
from werkzeug.security import check_password_hash
def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Главная' in response.data.decode('utf-8')

def test_create_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert 'Регистрация' in response.data.decode('utf-8')

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Войти' in response.data.decode('utf-8')

def test_register_success(client, db):
    response = client.post('/register', data={
        'email': 'newuser@example.com',
        'psw': 'secure123',
        'name': 'New User',
        'old': 25,
        'city': 'New York'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Главная' in response.data.decode('utf-8')

def test_register_success(client, db):
    response = client.post('/register', data={
        'email': 'newuser2@example.com',
        'psw': '12345',
        'name': 'New',
        'old': 100,
        'city': 'Seatle'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Главная' in response.data.decode('utf-8')

def test_login_failure(client):
    # Попытка входа с неправильными данными
    response = client.post('/login', data={
        'email': 'test@example.com',
        'psw': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Неверный email или пароль' in response.data.decode('utf-8')

def test_login_failure(client):
    # Попытка входа с неправильными данными
    response = client.post('/login', data={
        'email': 'test2@example.com',
        'psw': 'yyy'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Неверный email или пароль' in response.data.decode('utf-8')

def test_logout(client, new_user):
    # Вход перед выходом
    client.post('/login', data={'email': 'test@example.com', 'psw': 'password'})
    response = client.get('/logout', follow_redirects=True)
    assert 'Войти' in response.data.decode('utf-8')


def test_user_model(db, new_user):
    # Проверяем, что пользователь создан
    user = Users.query.filter_by(email=new_user.email).first()
    assert user is not None
    assert user.email == new_user.email
    assert check_password_hash(user.psw, 'password') is True

    # Проверяем связь с профилем
    assert user.pr is not None
    assert user.pr.name == 'Test User'
    assert user.pr.old == 30


def test_profile_model(db, new_user):
    profile = Profiles.query.filter_by(user_id=new_user.id).first()
    assert profile is not None
    assert profile.name == 'Test User'
    assert profile.old == 30
    assert profile.city == 'Test City'
    assert profile.users == new_user


def test_logout(client, new_user):
    # Вход перед выходом
    client.post('/login', data={'email': 'test2@example.com', 'psw': '123456'})
    response = client.get('/logout', follow_redirects=True)
    assert 'Войти' in response.data.decode('utf-8')
