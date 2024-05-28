from fastapi import Query
from enum import Enum


class LimitOptions(int, Enum):
    ten = 10
    twenty = 20
    fifty = 50
    hundred = 100


class PostsQueryParams:
    def __init__(
        self,
        title: str = None,
        body: str = None,
        limit: LimitOptions = Query(default=LimitOptions.twenty, le=100),
        page: int = 1
    ):
        self.title = title
        self.body = body
        self.limit = limit
        self.page = page
