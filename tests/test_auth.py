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

def test_register_missing_fields(client):
    # Попытка регистрации без email
    response = client.post('/register', data={
        'psw': 'secure123',
        'name': 'Incomplete User',
        'old': 30,
        'city': 'Nowhere'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Заполните все поля' in response.get_data(as_text=True)


def test_login_success(client, new_user):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'psw': 'password'
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

def test_logout(client, new_user):
    # Вход перед выходом
    client.post('/login', data={'email': 'test@example.com', 'psw': 'password'})
    response = client.get('/logout', follow_redirects=True)
    assert 'Войти' in response.data.decode('utf-8')
