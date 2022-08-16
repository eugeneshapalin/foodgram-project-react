
![example workflow](https://github.com/eugeneshapalin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# foodgram-project-react

Сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:

https://github.com/eugeneshapalin/foodgram-project-react

* В директории infra необходимо создать .env файл с данными:
    
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432

* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    
    DOCKER_PASSWORD=пароль от DockerHub
    DOCKER_USERNAME=имя пользователя

    USER=username для подключения к серверу
    HOST=ip сервера
    PASSPHRASE=< для сервера, если он установлен
    SSH_KEY=ваш SSH ключ (для получения: cat ~/.ssh/id_rsa)

    Workflow состоит из трёх шагов:
     - Проверка кода на соответствие PEP8
     - Сборка и публикация образа бекенда на DockerHub.
     - Автоматический деплой на удаленный сервер.


* На сервере соберите docker-compose:

sudo docker-compose up -d --build

* После успешной сборки на сервере выполните команды:
    sudo docker-compose exec backend python manage.py makemigrations
    sudo docker-compose exec backend python manage.py migrate
    sudo docker-compose exec backend python manage.py makemigrations api
    sudo docker-compose exec backend python manage.py migrate api
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    sudo docker-compose exec backend python manage.py collect_data
    sudo docker-compose exec backend python manage.py createsuperuser

    - Проект будет доступен по вашему IP

## адрес проекта в интернете
Проект запущен и доступен по адресу http://shapalin.ddns.net/ либо по ip адресу http://158.160.1.127/