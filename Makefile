run:
	pip install -r requirements/prod.txt
	python manage.py migrate
	python manage.py importimdb films
	python manage.py importimdb ratings

runserver:
	gunicorn --workers=3 --threads=2 --worker-connections=100 config.wsgi