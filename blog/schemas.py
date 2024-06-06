from pydantic import BaseModel

from authentication.schemas import UserViewSchema


class PostSchema(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True


class CompletePostSchema(PostSchema):
    id: int
    creator: UserViewSchema
