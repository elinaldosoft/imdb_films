### Start Project
`virtualenv venv -p $(which python3.6)`

### Enable Environment
`source venv/bin/activate`

### Install Packges
`pip3 install -r requirements/dev.txt`

## Docker Configurations
Build
- `docker-compose up --build`

Access Docker Container
- `docker exec -i -t id-container /bin/bash`

Migrate
- `docker-compose run web python3 manage.py migrate`

Collection Static
- `docker-compose run web python3 manage.py collectstatic --noinput`

Remove Containers
- `docker rm $(docker ps -q --all)`

## Import Movies
- `docker-compose run web python3 manage.py importimdb films`

## Add Ratings in Films
- `docker-compose run web python3 manage.py importimdb ratings`