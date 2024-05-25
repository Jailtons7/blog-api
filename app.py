from fastapi import FastAPI

from blog.routers import blog_router

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "A simple Blog API"}


app.include_router(blog_router)
