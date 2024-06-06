from typing import cast, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from db.connection import get_db
from blog.schemas import PostSchema, CompletePostSchema
from blog.models import Post
from blog.utils import PostsQueryParams
from authentication.oauth2 import get_current_user
from authentication.schemas import UserViewSchema


router = APIRouter()


@router.get("/", response_model=List[CompletePostSchema])
async def list_posts(
        db: Session = Depends(get_db),
        user: UserViewSchema = Depends(get_current_user),
        query_params: PostsQueryParams = Depends(PostsQueryParams)):
    """
    <strong>Returns a paginated list of saved posts ordered by id descending.</strong>\n
    The default length of the list is 20, but you can customize it throughout the param "limit".\n
    You can also search for expressions in the title and in the body of a <strong>Post</strong>.
    """
    posts = db.query(Post).order_by(Post.id.desc())
    if query_params.title:
        posts = posts.filter(
            cast("ColumnElement[bool]", Post.title == query_params.title)
        )
    if query_params.body:
        posts = posts.filter(
            cast("ColumnElement[bool]", Post.body == query_params.body)
        )
    if query_params.limit:
        posts.limit(query_params.limit)

    if query_params.page:
        posts = posts.offset((query_params.page - 1) * query_params.limit)
    return posts.all()


@router.get("/{post_id}", response_model=CompletePostSchema)
async def get_post(
        post_id: int,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    post = db.query(Post).filter(
        cast("ColumnElement[bool]", Post.id == post_id)
    ).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    return post


@router.post("/", response_model=CompletePostSchema, status_code=status.HTTP_201_CREATED)
async def add_post(
        post: PostSchema,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """
    Adds a new post to the database.
    Requires authentication
    """
    new_post = Post(**post.model_dump())
    new_post.creator = user
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return parse_obj_as(CompletePostSchema, new_post)


@router.put("/{post_id}", response_model=PostSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_post(
        post_id: int,
        post: PostSchema,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    posts = db.query(Post).filter(cast("ColumnElement[bool]", Post.id == post_id))
    if posts.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    posts.update(post.dict())
    db.commit()
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
        post_id: int,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    blog = db.query(Post).filter(
        cast("ColumnElement[bool]", Post.id == post_id)
    )
    if blog.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    blog.delete()
    db.commit()
    return {"msg": "Post Deleted"}
