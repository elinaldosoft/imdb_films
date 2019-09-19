FROM python:3

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y python3-dev
RUN python -m pip install --upgrade pip

WORKDIR /usr/src/app

COPY . .
RUN python -m pip install -r requirements/prod.txt