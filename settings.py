from typing import List

from environs import Env
from pydantic_settings import BaseSettings


env = Env()
env.read_env()


class Settings(BaseSettings):
    ALLOWED_HOSTS: List[str] = env.list("ALLOWED_HOSTS")
    DATABASE_URL: str = env.str("DATABASE_URL")
    DEBUG: bool = env.bool("DEBUG")
    SECRET_KEY: str = env.str("SECRET_KEY")
    ALGORITHM: str = env.str("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")
    REDIS_URL: str = env.str("REDIS_URL")
