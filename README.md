
# Log Monitoring API

### Technologies and Tools
* Python 3.8
* Django 4.0
* Django Rest Framework 3.13
* simplejwt 5.1
* Redis 4.1
* drf-yasg 1.20 (Swagger/Redoc)
* Pre-commit 2.17
* Docker


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

### Swagger/Redoc API Documentation

- http://localhost:8000/swagger/
- http://localhost:8000/redoc/


### Django Admin Dashboard

You can create a super user to access admin Dashboard

```
docker exec -it daft_api_1 python manage.py createsuperuser
```

http://localhost:8000/admin


### Sample cURL Requests

#### Register Request (/register)

```
curl --location --request POST 'http://localhost:8000/register/' \
--header 'Content-Type: application/json' \
--data-raw '{"username":"admin", "password":"admin1234x", "password2":"admin1234x", "email":"admin@example.com", "company":"testcompany1"}'
```

#### Token Request (/token)

"username" field accepts either username and email

```
curl --location --request POST 'http://localhost:8000/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "admin@example.com",
    "password": "admin1234x"
}'
```

```
curl --location --request POST 'http://localhost:8000/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "admin",
    "password": "admin1234x"
}'
```

#### Login Request (/login)

Creating dummy login data

```
curl --location --request POST 'http://localhost:8000/login/' \
--header 'Authorization: Bearer VERY_LONG_BEARER_ACCESS_TOKEN'
```

#### Logout Request (/logout)

Creating dummy logout data

```
curl --location --request POST 'http://localhost:8000/login/' \
--header 'Authorization: Bearer VERY_LONG_BEARER_ACCESS_TOKEN'
```

#### Log Request (/log)

```
curl --location --request GET 'http://localhost:8000/log/?q=test&is_active=True&user_id=1,2&created=2022-03-12,2022-03-13&log_type=login&company=1,2' \
--header 'Authorization: Bearer VERY_LONG_BEARER_ACCESS_TOKEN'
```
