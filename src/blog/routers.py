from fastapi import APIRouter
from src.blog.controllers import posts_router, comments_router

blog_router = APIRouter()
blog_router.include_router(posts_router, prefix="/posts", tags=["posts"])
blog_router.include_router(comments_router, prefix="/comments", tags=["comments"])
