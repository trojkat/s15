FROM python:3.8-buster as base

FROM base as builder

RUN mkdir /install
WORKDIR /install
COPY src/requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt


FROM base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
COPY --from=builder /install /usr/local
WORKDIR /code
COPY src .
RUN python manage.py collectstatic -c --noinput
RUN python manage.py compilemessages
CMD ["daphne", "-b", "0.0.0.0", "s15.asgi:application"]
