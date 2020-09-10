FROM python:3.8-buster as base

FROM base as builder

RUN mkdir /install
# RUN apk update && apk add \
#     # for psycopg2
#     postgresql-dev \
#     gcc \
#     python3-dev \
#     musl-dev \
#     # for libsass
#     g++ \
#     # for django-imagekit
#     libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl \
#     jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt


FROM base

ENV PYTHONUNBUFFERED 1
COPY --from=builder /install /usr/local
WORKDIR /code
COPY . .
# RUN apk --no-cache add uwsgi
# RUN fc-cache -fv
RUN python manage.py collectstatic -c --noinput
