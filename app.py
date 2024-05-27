from environs import Env
from fastapi import FastAPI

from blog.routers import blog_router
from blog.models import Base
from db.connection import engine

env = Env()
env.read_env()

app = FastAPI()
Base.metadata.create_all(engine)


@app.get("/")
async def root():
    return {"msg": "A simple Blog API"}


app.include_router(blog_router)
