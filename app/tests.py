import pytest
from flask import Flask, url_for
from app import ppp, db, Users, Profiles, Post
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем базу данных в памяти для тестов
    app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестов

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Создаем таблицы в базе данных
        yield client
        with app.app_context():
            db.drop_all()  # Удаляем таблицы после завершения теста

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Главная" in response.data.decode('utf-8')