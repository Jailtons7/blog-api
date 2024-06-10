from typing import List, Union

from pydantic import BaseModel, ConfigDict

from authentication.schemas import UserViewSchema


class PostSchema(BaseModel):
    title: str
    body: str

    model_config = ConfigDict(from_attributes=True)


class CompletePostSchema(PostSchema):
    id: int
    creator: UserViewSchema

    model_config = ConfigDict(from_attributes=True)


class CommentSchema(BaseModel):
    body: str

    model_config = ConfigDict(from_attributes=True)


class CommentViewSchema(CommentSchema):
    id: int
    responses: Union[List[CommentSchema], None]
    creator: UserViewSchema
