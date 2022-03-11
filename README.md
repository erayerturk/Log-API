# Django Rest Framework - Redis - Postgres - Docker


### Technologies and Tools
* Python 3.8
* Django 4.0
* Django Rest Framework 3.13
* simplejwt 5.1
* Redis 4.1
* drf-yasg 1.20 (Swagger/Redoc)
* Pre-commit 2.17


### Run the app in Docker

Everything is containerized. So all you need is Docker installed, and then you can build and run:

```
docker-compose up -d --build
```

And your app will be up on the *port 8000*

### Test

```
docker exec -it daft_api_1 python manage.py test
```

### Swagger/Redoc API Doc

http://localhost:8000/swagger/
http://localhost:8000/redoc/


### Django Admin Dashboard

You can create a super user to access admin Dashboard

```
docker exec -it daft_api_1 python manage.py createsuperuser
```

http://localhost:8000/admin
