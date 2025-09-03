# API-сервис для вопросов и ответов

REST API для управления вопросами и ответами с использованием Django REST Framework, PostgreSQL и строгой типизацией.

## Описание

API-сервис предоставляет функциональность для создания, просмотра и удаления вопросов и ответов. Реализовано каскадное удаление, валидация данных и полная типизация кода.

## Быстрый старт

### Клонирование репозитория
```bash
git clone <repository-url>
```

```bash
cd qa_service
```

### Запуск через Docker Compose
```bash
docker-compose up --build
```

### Применение миграций
```bash
docker-compose exec web python manage.py migrate
```

### Создание суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```

## Технологии

- Django 4.2 с Django REST Framework
- PostgreSQL 15 в Docker контейнере  
- Python 3.11 с полной типизацией
- Docker и docker-compose для развертывания
- pytest для тестирования

## Структура проекта

```
qa_service/
├── docker-compose.yml         
├── Dockerfile                 
├── requirements.txt           
├── pytest.ini               
├── README.md                 
├── manage.py                 
├── qa_service/               
│   ├── __init__.py
│   ├── settings.py           
│   ├── urls.py              
│   └── wsgi.py              
└── qa_api/                  
    ├── __init__.py
    ├── models.py            
    ├── serializers.py       
    ├── views.py             
    ├── urls.py              
    ├── validators.py        
    └── tests.py             
```

## API Endpoints

### Вопросы

**Получить список всех вопросов**
```bash
GET /api/questions/
```

**Создать новый вопрос**
```bash
POST /api/questions/
```

**Получить вопрос с ответами**
```bash
GET /api/questions/{id}/
```

**Удалить вопрос с ответами**
```bash
DELETE /api/questions/{id}/
```

### Ответы

**Добавить ответ к вопросу**
```bash
POST /api/questions/{id}/answers/
```

**Получить конкретный ответ**
```bash
GET /api/answers/{id}/
```

**Удалить ответ**
```bash
DELETE /api/answers/{id}/
```

## Тестирование API

### Веб-интерфейс DRF
```
http://localhost:8000/api/questions/
```

### Создание вопроса через curl
```bash
curl -X POST http://localhost:8000/api/questions/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Как настроить Django с PostgreSQL?"}'
```

### Получение списка вопросов
```bash
curl http://localhost:8000/api/questions/
```

### Создание ответа
```bash
curl -X POST http://localhost:8000/api/questions/1/answers/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Нужно установить psycopg2-binary и настроить DATABASES в settings.py",
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### Получение вопроса с ответами
```bash
curl http://localhost:8000/api/questions/1/
```

### Удаление вопроса
```bash
curl -X DELETE http://localhost:8000/api/questions/1/
```

## Запуск тестов


### Django test runner
```bash
docker-compose exec web python manage.py test
```

### Конкретный тест
```bash
docker-compose exec web python -m pytest qa_api/tests.py::QuestionAPITest::test_create_question
```

## Работа с базой данных

### Подключение к PostgreSQL
```bash
docker-compose exec postgres psql -U qa_user -d qa_db
```

### Просмотр таблиц
```sql
\dt
```

### Просмотр данных
```sql
SELECT * FROM qa_api_question;
```

```sql
SELECT * FROM qa_api_answer;
```

### Создание миграций
```bash
docker-compose exec web python manage.py makemigrations
```

### Применение миграций
```bash
docker-compose exec web python manage.py migrate
```

## Мониторинг и отладка

### Просмотр логов Django
```bash
docker-compose logs web
```

### Мониторинг в реальном времени
```bash
docker-compose logs -f web
```

### Проверка статуса контейнеров
```bash
docker-compose ps
```

### Подключение к контейнеру
```bash
docker-compose exec web bash
```

## Разработка

### Остановка контейнеров
```bash
docker-compose down
```

### Пересборка с изменениями
```bash
docker-compose up --build
```

### Сброс базы данных
```bash
docker-compose down -v
```

```bash
docker-compose up --build
```

## Особенности реализации

- Строгая типизация всех функций и методов
- Кастомные валидаторы для текстов и UUID
- Каскадное удаление при удалении вопроса
- Логирование всех операций CRUD
- Пагинация списков по 10 элементов
- Транзакционные операции для критических изменений
- Browsable API для тестирования через веб-интерфейс

## Примеры запросов и ответов

### Создание вопроса

**Запрос:**
```json
POST /api/questions/
{
  "text": "Как работает Django ORM?"
}
```

**Ответ:**
```json
HTTP 201 Created
{
  "id": 1,
  "text": "Как работает Django ORM?",
  "created_at": "2025-09-03T18:30:00Z",
  "answers_count": 0
}
```

### Создание ответа

**Запрос:**
```json
POST /api/questions/1/answers/
{
  "text": "Django ORM использует паттерн Active Record для работы с базой данных",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Ответ:**
```json
HTTP 201 Created
{
  "id": 1,
  "question": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "Django ORM использует паттерн Active Record для работы с базой данных",
  "created_at": "2025-09-03T18:31:00Z"
}
```

## Обработка ошибок

### Валидация вопроса
```json
HTTP 400 Bad Request
{
  "text": ["Текст вопроса должен содержать минимум 10 символов"]
}
```

### Невалидный UUID
```json
HTTP 400 Bad Request
{
  "user_id": ["Некорректный формат UUID"]
}
```

### Несуществующий вопрос
```json
HTTP 404 Not Found
{
  "detail": "Не найдено."
}
```



