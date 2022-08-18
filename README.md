
![example workflow](https://github.com/eugeneshapalin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# foodgram-project-react

Сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:

https://github.com/eugeneshapalin/foodgram-project-react

* В директории infra необходимо создать .env файл с данными:<br>
    
    DB_ENGINE=django.db.backends.postgresql<br>
    DB_NAME=postgres<br>
    POSTGRES_USER=postgres<br>
    POSTGRES_PASSWORD=postgres<br>
    DB_HOST=db<br>
    DB_PORT=5432<br>
    SECRET_KEY=<секретный ключ проекта django><br>

* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:<br>
    
    DB_ENGINE=django.db.backends.postgresql<br>
    DB_NAME=postgres<br>
    POSTGRES_USER=postgres<br>
    POSTGRES_PASSWORD=postgres<br>
    DB_HOST=db<br>
    DB_PORT=5432<br>
    
    DOCKER_PASSWORD=пароль от DockerHub<br>
    DOCKER_USERNAME=имя пользователя<br>

    USER=username для подключения к серверу<br>
    HOST=ip сервера<br>
    PASSPHRASE=< для сервера, если он установлен<br>
    SSH_KEY=ваш SSH ключ (для получения: cat ~/.ssh/id_rsa)<br>

    Workflow состоит из трёх шагов:<br>
     - Проверка кода на соответствие PEP8<br>
     - Сборка и публикация образа бекенда на DockerHub.<br>
     - Автоматический деплой на удаленный сервер.<br>


* На сервере соберите docker-compose:

sudo docker-compose up -d --build

* После успешной сборки на сервере выполните команды:<br>
    sudo docker-compose exec backend python manage.py makemigrations <br>
    sudo docker-compose exec backend python manage.py migrate <br>
    sudo docker-compose exec backend python manage.py makemigrations api <br>
    sudo docker-compose exec backend python manage.py migrate api <br>
    sudo docker-compose exec backend python manage.py collectstatic --noinput <br>
    sudo docker-compose exec backend python manage.py collect_data <br>
    sudo docker-compose exec backend python manage.py createsuperuser <br> 

    - Проект будет доступен по вашему IP

## адрес проекта в интернете
Проект запущен и доступен по адресу http://shapalin-foodgram.ddns.net/ либо по ip адресу http://130.193.40.129/