from math import ceil

import redis.asyncio as redis
from contextlib import asynccontextmanager

from settings import Settings
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi_limiter import FastAPILimiter


settings = Settings()


async def custom_callback(_: Request, __: Response, expire: int):
    """
    default callback for handle too many requests
    :param _: a Request object
    :param __: a Response object
    :param expire: the remaining time in milliseconds
    :return:
    """
    expire = ceil(expire / 1000)
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=f"Too many requests. Try again in {expire} seconds",
        headers={"Retry-After": f"{expire} seconds"}
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_conn = redis.from_url(settings.REDIS_URL, encoding="utf-8")
    await FastAPILimiter.init(
        redis=redis_conn,
        http_callback=custom_callback
    )
    yield
    await FastAPILimiter.close()
