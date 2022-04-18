# Тестовое задание

<img src="https://github.com/alfir777/blog_api/workflows/CI/badge.svg?branch=master">
Тестовое задание

## Запуск

1. Клонировать репозиторий или форк

```
git clone https://github.com/alfir777/blog_api.git
```

2. Выполнить копирование файла .env_template на .env и выставить свои параметры

```
cd blog_api/
cp .env_template .env
```

3. Создать виртуальную среду venv

```
python3 -m venv env
source env/bin/activate
```

4. Установка зависимостей

```
pip install -r requirements.txt
```

5. Выполнить миграции

```
cd blog_api/
python3 manage.py migrate
```

6. Создать суперпользователя (при необходимости)

```
python3 manage.py createsuperuser
```

7. Запустить сам проект

```

python3 manage.py runserver

```

8. Запустить тесты

```

python3 manage.py test

```

9. Запустить линтер, предварительно установив с requirements_dev.txt

```
pip install -r requirements_dev.txt
flake8 --max-line-length 120 --exclude migrations,venv,manage.py

```

## Запуск в докере

1. Клонировать репозиторий или форк

```
git clone https://github.com/alfir777/blog_api.git
```

2. Создать сеть для изоляции БД

```
docker network create web
```

3. Развернуть контейнеры с помощью в docker-compose

```
docker-compose up -d
```

4. Выполнить миграции

```
docker exec -it web python3 manage.py migrate
```

5. Создать суперпользователя (при необходимости)

```
 docker exec -it web python3 manage.py createsuperuser
```

6. Запустить тесты в контейнере (сменить предварительно в .env TYPE_DATABASES=sqlite3)

```
docker-compose -f 'docker-compose-dev.yml' up --exit-code-from tests tests
```

7. Запустить линтер в контейнере:

```
docker-compose -f 'docker-compose-dev.yml' up --exit-code-from lint lint
```