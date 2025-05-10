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

