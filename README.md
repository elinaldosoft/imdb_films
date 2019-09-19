### Start Project
`virtualenv venv -p $(which python3.6)`

### Enable Environment
`source venv/bin/activate`

### Install Packges
`pip3 install -r requirements/dev.txt`

## Docker Useful
Build
- `docker-compose up --build`

Access Docker Container
- `docker exec -i -t id-container /bin/bash`

List Volumes
- `docker volume ls`

Remove Volume
- `docker volume rm volume_name`

Remove Containers
- `docker rm $(docker ps -q --all)`

## Configuration 
Migrate
1 - `make migrate`

Collection Static
2 - `make collectstatic`

Import Movies
- `make import-films` 
```
    Time average to import 00:06:43
```

Add Ratings in Films
- `make import-ratings`
```
    Time average to import 00:18:38
```



```
UPDATE films
SET cache_average_rating=subquery.average_rating,
    cache_num_votes=subquery.num_votes
FROM (SELECT tconst, average_rating, num_votes
      FROM ratings) AS subquery
WHERE films.tconst=subquery.tconst;
```