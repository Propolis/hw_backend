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

### Создание задачи

```bash
curl -X POST http://127.0.0.1:8000/tasks/ -H "Content-Type: application/json" -d '{"title": "Зайти в гости", "description": "Улица труляля дом два"}'
```

### Получение всех задач

```bash
curl http://127.0.0.1:8000/tasks/
```

### Получение задачи по id

```bash
curl http://127.0.0.1:8000/tasks/1
```

### Обновление задачи

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"title": "Купить хлеб", "completed": true}'
```

### Удаление задачи

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

### Удаление несуществующей задачи

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/999
```

Вернёт `404`: `{"detail":"Not found"}`
