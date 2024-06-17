from fastapi import APIRouter

from src.authentication.controllers import router

auth_router = APIRouter()
auth_router.include_router(router, prefix="/auth", tags=["auth"])
