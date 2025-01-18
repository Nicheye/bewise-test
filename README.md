Запуск - docker compose up --build 

docs - http://localhost:8000/docs#/, но напишу и руками)

Создание - POST http://localhost:8000/applications
```
Request:
{
  "user_name": "misha",
  "description": "misha descr"
}
Response:
{
    "user_name": "misha",
    "description": "misha",
    "id": 18,
    "created_at": "2025-01-18T13:52:45.532809"
}
```
Получение - GET http://localhost:8000/applications
```
[
    {
        "user_name": "JohnDoe",
        "description": "Description of the request",
        "id": 1,
        "created_at": "2025-01-18T13:26:30.932526"
    },
    {...},
    .....
]
Фильтры по name, page, size передаются через query параметры (?name=some&...)
```
