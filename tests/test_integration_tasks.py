def test_create_task_integration(client, auth_headers):
    response = client.post("/tasks/", json={"title": "Integration task"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Integration task"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_persisted(client, auth_headers):
    client.post("/tasks/", json={"title": "Persisted task"}, headers=auth_headers)
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    titles = [t["title"] for t in response.json()]
    assert "Persisted task" in titles


def test_task_not_found_error_format(client, auth_headers):
    response = client.get("/tasks/999", headers=auth_headers)
    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    assert body["error"]["code"] == "TASK_NOT_FOUND"
    assert "message" in body["error"]


def test_create_comment(client, auth_headers):
    task = client.post("/tasks/", json={"title": "Task with comments"}, headers=auth_headers).json()
    response = client.post(f"/v1/tasks/{task['id']}/comments", json={"text": "Hello"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Hello"
    assert data["task_id"] == task["id"]


def test_get_comments(client, auth_headers):
    task = client.post("/tasks/", json={"title": "Task"}, headers=auth_headers).json()
    client.post(f"/v1/tasks/{task['id']}/comments", json={"text": "Comment 1"}, headers=auth_headers)
    client.post(f"/v1/tasks/{task['id']}/comments", json={"text": "Comment 2"}, headers=auth_headers)
    response = client.get(f"/v1/tasks/{task['id']}/comments", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_comment_on_nonexistent_task(client, auth_headers):
    response = client.post("/v1/tasks/999/comments", json={"text": "Hello"}, headers=auth_headers)
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "TASK_NOT_FOUND"
