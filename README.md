# TacoBot

Mostly just manages roles

## Usage

* build: `docker build -t tacobot .`
* run dev: `docker run --env-file ./.env -it --rm --name tacobot tacobot`
* run prod: `docker run --env-file ./.env -d --name tacobot tacobot`