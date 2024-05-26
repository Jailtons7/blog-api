from environs import Env
from pydantic_settings import BaseSettings


env = Env()
env.read_env()


class Settings(BaseSettings):
    DATABASE_URL: str = env.str("DATABASE_URL")
