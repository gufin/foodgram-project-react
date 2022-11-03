[![Django-app workflow](https://github.com/gufin/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/gufin/foodgram-project-react/actions/workflows/main.yml)
# Foodgram

### _Учебный проект_

В приложении реализована возможность регистрации и аутентификации пользователей. Пользователи могут публиковать и редактировать рецепты, подписываться друг на друга, добавлять рецепты в избранное, а также составлять списки покупок и скачивать их в формате pdf.

В backend части проекта использованы следующие инструменты:
- Python 3.10
- Django 4
- DjangoREST Framework

В инфраструктурной части использованы:
- PostgreSQL
- Docker
- Nginx

Реализованы настройки CI/CD через GitHub Actions

# Установка проекта

Установить Docker и docker-compose:
```sh
sudo apt-get update
sudo apt install docker.io 
sudo apt-get install docker-compose-plugin
```
Клонировать репозиторий:
```sh
git clone git@github.com:gufin/foodgram-project-react.git
```
При развертывании на сервере без использования GitHub Actions в папке infra необходимо создать файл с значениями переменных .env
```sh
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_user_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=False
```
Поля `your_postgres_user` и `your_postgres_user_password` нужно заполнить своими данными подключения к базе данных PostgreSQL. Для генерации значения SECRET_KEY можно воспользоваться командой: 
```sh
openssl rand -hex 32
```
При запуске на сервере нужно добавить адрес своего сервера в переменную ALLOWED_HOSTS в файле backend/foodgram/settings.py

##### Запуск Docker контейнеров
При первом запуске из директории infra нужно выполнить команду:
```sh
sudo docker-compose up -d --build
```
При последующих запусках ключ --build можно не использовать.
Далее необходимо выполнить миграции:
```sh
sudo docker-compose exec web python manage.py migrate
```
Создать суперпользователя django:
```sh
sudo docker-compose exec web python manage.py createsuperuser
```
Собрать статические файлы:
```sh
sudo docker-compose exec web python manage.py collectstatic
```
Загрузить данные ингредиентов:
```sh
sudo docker-compose exec web bash load_data.sh
```
[Документация api](http://127.0.0.1/api/docs/) 

[Панель администратора](http://127.0.0.1/admin/) 

### GitHub Actions
Github actions проверят кода на соответствия стандартам PEP8, пересоберут образ  docker файла и опубликуют его на hub.docker.com и задеплоит проект на вашем сервере. В случае успеха вам придёт оповещение в Telegram.
При использовании github actions не нужно создавать файл .env но нужно определить следующие переменные окружения Secrets:

```sh
DEBUG=False
ALLOWED_HOSTS # Строка разрешенных серверов
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_user_password
DB_HOST=db
DB_PORT=5432
DOCKER_PASSWORD # Пароль пользователя hub.docker.com
DOCKER_USERNAME # Пользователь hub.docker.com
DOCKER_REPO_NAME # Имя образа в hub.docker.com
HOST # Адрес вашего сервера
PASSPHRASE # Секретная фраза вашего ssh ключа (если есть)
SECRET_KEY=your_secret_key
SSH_KEY # ssh ключ к вашему серверу
TELEGRAM_TO # Ваш телеграм id для оповещений
TELEGRAM_TOKEN # Токен вашего телеграм бота
USER # Пользователь вашего сервера
```

# Автор
Дробышев Иван
