# How to run the project in Production mode (In this order)
To you run in production, need the docker and docker-compose installed
- `git clone https://github.com/elinaldosoft/imdb_films.git`
- `cd imdb_films`
- `mv .env.example .env`
- `make run`
- `make migrate`
- `make collectstatic`
- `make import-films`
- `make import-ratings`
- `make cache-ratings`

```
listen in http://localhost:5000
user: admin | passwd: admin

Access postgres:
$psql -h 127.0.0.1 -p 54320 -U postgres

Tips:
Do you can add password in Postgres
environment:
    POSTGRES_PASSWORD: example
```

# How to run the project in Development mode
`virtualenv venv -p $(which python3.6)`
### Enable Environment
`source venv/bin/activate`
### Install Packages
`pip3 install -r requirements/dev.txt`
### Running Migrate
`python manage.py migrate`

## Explanation
- make run:
    - This command create 3 containers
        - Postgres
        - Web (Django)
        - Nginx (Reverse proxy server - Load Balance)
    - Each container has its own volume

- make import-films:
    - This command call the method [`import_films`](https://github.com/elinaldosoft/imdb_films/blob/master/web/app/movies/management/commands/importimdb.py#L53). Steps:
        - Download movies from IMDB `https://datasets.imdbws.com/title.basics.tsv.gz`
        - Process file
        - Insert in Database

- make import-ratings:
    - This command call the method [`import_ratings`](https://github.com/elinaldosoft/imdb_films/blob/master/web/app/movies/management/commands/importimdb.py#L24). Steps:
        - Download ratings from IMDB `https://datasets.imdbws.com/title.ratings.tsv.gz`
        - Process file
        - Insert in Database

- make cache-ratings:
    - This command run a query SQL that update the values of average the films
    ```
    UPDATE films
    SET cache_average_rating=subquery.average_rating,
        cache_num_votes=subquery.num_votes
    FROM (SELECT tconst, average_rating, num_votes
        FROM ratings) AS subquery
    WHERE films.tconst=subquery.tconst;
    ```

### Obs:
`This process can to be slow, because are 6M of titles`

### Docker Useful
- `docker-compose up --build` (Build)
- `docker exec -i -t id-container /bin/bash` (Access Docker Container)
- `docker volume ls` (List Volumes)
- `docker volume rm volume_name` (Remove Volume)
- `docker rm $(docker ps -q --all)` (Remove containers)
- `docker stop $(docker ps -a -q)` (Stop all containers)
- `docker volume rm $(docker volume ls -q)` (Remove all volumes)