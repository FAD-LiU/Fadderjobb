FROM python:3.7

# Stop Django from being sad when trying to create static files
ENV DJANGO_SETTINGS_MODULE=fadderjobb.settings_production

WORKDIR /srv
COPY ./ ./

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

