def test_register(client):
    response = client.post("/auth/register", json={"username": "user1", "email": "user1@test.com", "password": "pass1"})
    assert response.status_code == 200


def test_register_duplicate(client):
    client.post("/auth/register", json={"username": "user1", "email": "user1@test.com", "password": "pass1"})
    response = client.post("/auth/register", json={"username": "user1", "email": "user1@test.com", "password": "pass1"})
    assert response.status_code == 400


def test_login(client):
    client.post("/auth/register", json={"username": "user1", "email": "user1@test.com", "password": "pass1"})
    response = client.post("/auth/login", json={"username": "user1", "password": "pass1"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid(client):
    response = client.post("/auth/login", json={"username": "nouser", "password": "wrong"})
    assert response.status_code == 401
