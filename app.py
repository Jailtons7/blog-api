import uvicorn
from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware

from settings import Settings
from src.requests_limit import lifespan
from src.db.connection import engine, Base
from src.authentication.routers import auth_router
from src.blog.routers import blog_router


settings = Settings()

app = FastAPI(title="Blogs API", version="0.0.1", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(engine)


@app.get("/")
async def redirect_to_documentation():
    return responses.RedirectResponse(url="/docs")

app.include_router(auth_router)
app.include_router(blog_router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
