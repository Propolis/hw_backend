def test_create_task(client, auth_headers):
    response = client.post("/tasks/", json={"title": "Test task"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test task"


def test_get_tasks(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_task(client, auth_headers):
    created = client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers).json()
    response = client.get(f"/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 200


def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers):
    created = client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers).json()
    response = client.put(f"/tasks/{created['id']}", json={"title": "Updated", "completed": True}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_delete_task(client, auth_headers):
    created = client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers).json()
    response = client.delete(f"/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 200


def test_tasks_require_auth(client):
    response = client.get("/tasks/")
    assert response.status_code == 401
