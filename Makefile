run:
	src/manage.py runserver
	open http://127.0.0.1:8000

migrate:
	src/manage.py migrate

shell:
	src/manage.py shell

build:
	docker build . -t s15
