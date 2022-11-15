[![Django-app workflow](https://github.com/gufin/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/gufin/foodgram-project-react/actions/workflows/main.yml)
# Foodgram

🛠 The application implements the ability to register and authenticate users. Users can publish and edit recipes, follow each other, add recipes to favorites, create shopping lists and download them in pdf format.

The following tools were used in the backend part of the project:
- Python 3.10
- Django 4
- DjangoREST Framework

The infrastructure part used:
- PostgreSQL
- Docker
- Nginx

Implemented CI/CD settings via GitHub Actions

# 🚀 Project installation

Install Docker and docker-compose:
```sh
sudo apt-get update
sudo apt install docker.io 
sudo apt-get install docker-compose-plugin
```
Clone repository:
```sh
git clone git@github.com:gufin/foodgram-project-react.git
```
When deploying to a server without using GitHub Actions, you need to create a file with the values of the .env variables in the infra folder.
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
The `your_postgres_user` and `your_postgres_user_password` fields need to fill in with your PostgreSQL database connection data. To generate the SECRET_KEY value, you can use the command: 
```sh
openssl rand -hex 32
```
When running on a server, you need to add the address of your server to the ALLOWED_HOSTS variable in the backend/foodgram/settings.py file.

##### 🐳 Running Docker containers
When you first start from the infra directory, you need to run the command:
```sh
sudo docker-compose up -d --build
```
On subsequent launches, the --build key can omit.
Next, you need to perform migrations:
```sh
sudo docker-compose exec web python manage.py migrate
```
Create django superuser:
```sh
sudo docker-compose exec web python manage.py createsuperuser
```
Collect static files:
```sh
sudo docker-compose exec web python manage.py collectstatic
```
Load ingredient data:
```sh
sudo docker-compose exec web bash load_data.sh
```
[api documentation](http://127.0.0.1/api/docs/) 

[Admin panel](http://127.0.0.1/admin/) 

### :octocat: GitHub Actions
GitHub actions will check the code for compliance with PEP8 standards, rebuild the image of the docker file and publish it to hub.docker.com and deploy the project on your server. If successful, you will receive a notification in Telegram.
When using GitHub actions, you do not need to create an .env file, but you need to define the following Secrets environment variables:

```sh
DEBUG=False
ALLOWED_HOSTS # String of allowed servers
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_user_password
DB_HOST=db
DB_PORT=5432
DOCKER_PASSWORD # Hub.docker.com user password
DOCKER_USERNAME # hub.docker.com user
DOCKER_REPO_NAME # Image name in hub.docker.com
HOST # Address of your server
PASSPHRASE # The passphrase of your ssh key (if any)
SECRET_KEY=your_secret_key
SSH_KEY # ssh key to your server
TELEGRAM_TO # Your telegram id for notifications
TELEGRAM_TOKEN # Token of your telegram bot
USER # Your server user
```

# :smirk_cat: Author
Drobyshev Ivan
