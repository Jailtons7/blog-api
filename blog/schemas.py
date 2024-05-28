from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class PostSchema(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True


class CompletePostSchema(PostSchema):
    id: int
