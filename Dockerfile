FROM python:3

WORKDIR /app

COPY bot ./bot
COPY crontab ./crontab
COPY manage.py .
COPY problems ./problems
COPY scraper ./scraper
COPY config ./config
COPY static ./static
COPY media ./media
COPY requirements.txt .
COPY .env .

RUN pip install -r requirements.txt

RUN ./manage.py collectstatic --no-input

CMD ./manage.py runserver 0.0.0.0:80