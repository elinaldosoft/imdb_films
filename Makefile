migrate:
	docker-compose run web python3 manage.py migrate
collectstatic:
	docker-compose run web python3 manage.py collectstatic --noinput
import-films:
	docker-compose run web python3 manage.py importimdb films
import-ratings:
	docker-compose run web python3 manage.py importimdb ratings
cache-ratings:
	docker-compose run web python3 manage.py importimdb ratings_cache
run:
	docker-compose up -d --build
stop:
	docker-compose down
clean:
	docker stop $(docker ps -a -q)
	docker rm $(docker ps -a -q)