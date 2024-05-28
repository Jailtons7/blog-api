from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True


class CompletePostSchema(PostSchema):
    id: int
