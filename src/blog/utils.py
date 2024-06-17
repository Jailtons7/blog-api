from fastapi import Query
from enum import Enum


class LimitOptions(int, Enum):
    ten = 10
    twenty = 20
    fifty = 50
    hundred = 100


class PaginationQueryParams:
    """ Inherit from this class everytime you need pagination query params """
    def __init__(
            self,
            limit: LimitOptions = Query(default=LimitOptions.twenty, le=100),
            page: int = 1
    ):
        self.limit = limit
        self.page = page


class PostsQueryParams(PaginationQueryParams):
    def __init__(
            self,
            title: str = None,
            body: str = None,
            limit: LimitOptions = Query(default=LimitOptions.twenty, le=100),
            page: int = 1
    ):
        super().__init__(limit=limit, page=page)
        self.title = title
        self.body = body


class CommentsQueryParams(PaginationQueryParams):
    def __init__(
            self,
            limit: LimitOptions = Query(default=LimitOptions.twenty, le=100),
            page: int = 1
    ):
        super().__init__(limit=limit, page=page)
