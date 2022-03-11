FROM python:3.9.1-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -U pip setuptools
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
