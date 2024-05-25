from fastapi import APIRouter
from blog.controllers import router

blog_router = APIRouter()
blog_router.include_router(router, prefix="/blog", tags=["blog"])
