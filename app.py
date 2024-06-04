import uvicorn
from fastapi import FastAPI, responses

from db.connection import engine, Base
from authentication.routers import auth_router
from blog.routers import blog_router

app = FastAPI(title="Blogs API", version="0.0.1")
Base.metadata.create_all(engine)


@app.get("/")
async def redirect_to_documentation():
    return responses.RedirectResponse(url="/docs")

app.include_router(auth_router)
app.include_router(blog_router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
