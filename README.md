# BLOG API

In this project I use Python and FasAPI to develop a simple Blog API.
My main goal here is to practice FastAPI features, to know how it automatically 
generates docs, how to connect it with postgres database throughout psycopg2,
how to implement Oauth2 authentication, how to design a FastAPI application etc.

## Running with docker
First of all, copy the content of `.env.example` into a `.env` file and finally

```shell
docker compose build
```

```shell
docker compose up
```

## Running without docker
Running with docker is highly recommended, but if you want follow the next steps to run locally:

Create and activate a virtual environment
```shell
python -m venv venv && source venv/bin/activate
```

Install the dependencies:

```shell
pip install -r requirements.txt
```

Copy the `.env.example` into a `.env` file and finally:

```shell
uvicorn app:app --reload
```
