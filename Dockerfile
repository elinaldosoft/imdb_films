FROM python:3

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y python3-dev

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements/prod.txt

EXPOSE 8000
CMD [ "make", "runserver" ]