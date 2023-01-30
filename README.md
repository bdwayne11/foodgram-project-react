Foodgram project
========

Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.

Адрес проекта: http://158.160.40.65

### Для ревью: http://158.160.40.65, admin@admin.ru, pass: admin


### Технологии
Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL, Yandex Cloud, Continuous Integration, Continuous Deployment

#### Развернуть проект на удаленном сервере:

* Клонировать репозиторий:

```
git@github.com:bdwayne11/foodgram-project-react.git
```

* Установить на сервере Docker, Docker Compose:

```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```

* Перенести на сервер 2 файла:

```
scp docker-compose.yml nginx.conf username@your.id.add.res:/home/username/ 
```

* Если хотите работать с github actions, необходимо добавить секреты.

```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```

* Поднять docker-compose:
```
sudo docker-compose up
```

* Выполнить миграции, создать суперпользователя, собрать статику:

```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```

* Наполнить БД ингредиентами
```
sudo docker compose exec backend python manage.py upload_ingredients
```

* Автор проекта:
Владислав Бойко
