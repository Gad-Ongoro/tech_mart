FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./server/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./server /app

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
