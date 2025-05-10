def login(client):
    client.post('/login', data={
        'email': 'test@example.com',
        'psw': 'password'
    }, follow_redirects=True)

def test_create_post_success(client, db, new_user):
    login(client)
    response = client.post('/create', data={
        'title': 'Test Post',
        'text': 'This is a test post.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Test Post' in response.data.decode('utf-8')

