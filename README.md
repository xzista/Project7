# Веб-приложение на Django

## Описание проекта
Этот проект представляет собой веб-приложение на Django, сайт для бронирования столиков в ресторане.

## 📂 Структура проекта
```
Project_7/
├── .github/
│   └── workflow/
│       └── ci.yml
├── bookings/
│   ├── migrations/
│   │   └── __int__.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_tables.py
│   │ 
│   ├── templates/
│   │   └── catalog/
│   │       ├── contacts.html
│   │       └── home.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .github/
│   ├── Dockerfile
│   └── nginx.conf
├── static/
│   └── images/
├── templates/
│   ├── bookings/
│   ├── partials/
│   └── users/
├── users/
│   ├── migrations/
│   │   └── __int__.py
│   ├── management/
│   │   └── commands/
│   │       └── csu.py
│   │ 
│   ├── templates/
│   │   └── catalog/
│   │       ├── contacts.html
│   │       └── home.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .flake8
├── .gitignore
├── .env.sample
├── Dokerfile
├── docker-compouse.yaml
├── manage.py
├── poetry.lock
├── pyproject.toml
└── README.md
```
## 🚀 Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/xzista/homework_4
cd project2
```
2. Установите зависимости:
```bash
poetry install
```
3. Примените миграции:
```bash
python manage.py migrate
```
4. Запустите сервер:
```bash
python manage.py runserver
```

## 🛠 Технологический стек

- Python 3.13
- Django 5.2.5 и выше
- Bootstrap 5
- HTML5/CSS3