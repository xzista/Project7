# Сайт для бронирования столиков в ресторане

## Описание проекта
Этот проект представляет собой веб-приложение на Django, сайт для бронирования столиков в ресторане.
С возможностью регистрации с подтверждением почты. Авторизации пользователей по почте и паролю, а также восстановление пароля через почту.
Также у пользователей есть разделение на клиентов и персонал:
- Клинеты могут бронировать, просматривать и отменять свои бронирования и оставлять отзовы.
- Персонал может видеть все бронирования, подтверждать или отменять бронирования, модерировать отзывы и обновлять меню ресторана.

## 📂 Структура проекта
```
Project7/
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
git clone https://github.com/xzista/Project7.git 
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

## ⚙️ Настройка CI/CD и деплоя
1. Подготовка сервера
   - Установить зависимости:
   ```
   sudo apt update
   sudo apt install -y docker docker-compose git
   ```
   - Клонировать проект:
   ```
   cd /opt
   sudo git clone https://github.com/xzista/Project7.git Project7
   cd education-platform
   ```
   - Создать .env на основе шаблона:
   ```
   cp .env.sample .env
   ```
   - Запустить проект:
   ```
   docker-compose -f docker-compose.prod.yaml up -d --build
   ```
2. GitHub Actions Workflow
    - Файл workflow находится по пути:
   ```
   .github/workflows/ci.yml
   ```
   - Деплой запускается автоматически при push в ветку main.
3. GitHub Secrets

Для корректной работы CI/CD необходимо добавить в Settings → Secrets → Actions следующие секреты:

```
Название	        Пример значения	        Назначение

SERVER_HOST	        51.250.xxx.xxx	        IP сервера
SERVER_USER	        ubuntu	                SSH-пользователь
SERVER_SSH_KEY	        приватный SSH-ключ	Подключение к серверу
SECRET_KEY	        django-insecure-abc123	Ключ Django
NAME_DB	                education_db	        Имя БД
USER_DB	postgres	Пользователь            БД
PASSWORD_DB	        strongpassword	        Пароль БД
STRIPE_API_KEY	        sk_test_...	        Ключ Stripe
EMAIL_HOST_USER	        example@yandex.ru       Email
EMAIL_HOST_PASSWORD	app-password	        Пароль почты
TEST_SECRET_KEY	        test-secret-key	        Для тестов
TEST_NAME_DB	        test_db	                Для тестов
TEST_USER_DB	        test_user	        Для тестов
TEST_PASSWORD_DB	test_password	        Для тестов
```
