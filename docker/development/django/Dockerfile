FROM python:3.7-stretch

ENV PYTHONUNBUFFERED 1

RUN apk update \
    # Install 'psycopg2' and other build dependencies.
    && apk add --virtual build-deps gcc python3-dev musl-dev make build-base libmemcached-dev \
    && apk add postgresql-dev \
    # Install Pillow dependencies.
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    # Install CFFI dependencies
    && apk add libffi-dev py-cffi \
    # Install dependencies for translations.
    && apk add gettext \
    # Install the 'psql' client for administrating the PostgreSQL database.
    && apk add postgresql-client

# Requirements are installed here to ensure that they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/docker-development.txt

COPY ./docker/development/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/development/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
