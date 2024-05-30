from fastapi import APIRouter

from authentication.controllers import router

auth_router = APIRouter()
auth_router.include_router(router, prefix="/auth", tags=["auth"])
