run:
	webapp/manage.py runserver
	open http://127.0.0.1:8000

migrate:
	webapp/manage.py migrate

shell:
	webapp/manage.py shell
