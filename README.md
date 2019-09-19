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

List Volumes
- `docker volume ls`

Remove Volume
- `docker volume rm volume_name`

Migrate
- `make migrate`

Collection Static
- `make collectstatic`

Remove Containers
- `docker rm $(docker ps -q --all)`

## Import Movies
- `make import-films`

## Add Ratings in Films
- `make import-ratings`