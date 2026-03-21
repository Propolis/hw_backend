# Task Manager 

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python run.py
```

Сервис будет доступен на `http://127.0.0.1:8000`


## Тестирование

### Регистрация

```bash
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"username": "user1", "email": "user1@mail.com", "password": "pass1"}'
```

### Вход

```bash
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username": "user1", "password": "pass1"}'
```

Вернёт токен: `{"access_token": "...", "token_type": "bearer"}`

### Создание задачи

```bash
curl -X POST http://127.0.0.1:8000/tasks/ -H "Content-Type: application/json" -H "auth-token: <токен>" -d '{"title": "Зайти в гости", "description": "Улица труляля дом два"}'
```

### Получение всех задач

```bash
curl http://127.0.0.1:8000/tasks/ -H "auth-token: <токен>"
```

### Получение задачи по id

```bash
curl http://127.0.0.1:8000/tasks/1 -H "auth-token: <токен>"
```

### Обновление задачи

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -H "auth-token: <токен>" -d '{"title": "Купить хлеб", "completed": true}'
```

### Удаление задачи

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1 -H "auth-token: <токен>"
```

### Удаление несуществующей задачи

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/999 -H "auth-token: <токен>"
```

Вернёт `404`: `{"detail":"Задача не найдена"}`
