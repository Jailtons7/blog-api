from typing import cast, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session, query
from pydantic import TypeAdapter

from src.db.connection import get_db
from src.blog.schemas import (
    PostSchema, CompletePostSchema, CommentSchema, CommentViewSchema,
)
from src.blog.models import Post, Comment
from src.blog.utils import PostsQueryParams, CommentsQueryParams
from src.constants import REQUESTS_LIMIT_GET_POSTS
from src.authentication.oauth2 import get_current_user
from src.authentication.schemas import UserViewSchema


posts_router = APIRouter()


@posts_router.get(
    "",
    response_model=List[CompletePostSchema],
    dependencies=[Depends(RateLimiter(
        times=REQUESTS_LIMIT_GET_POSTS["TIMES"],
        seconds=REQUESTS_LIMIT_GET_POSTS["SECONDS"],
    ))]
)
async def list_posts(
        db: Session = Depends(get_db),
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
    adapter = TypeAdapter(List[CompletePostSchema])
    return adapter.validate_python(posts)


@posts_router.get(
    "/{post_id}",
    response_model=CompletePostSchema,
    dependencies=[Depends(RateLimiter(
        times=REQUESTS_LIMIT_GET_POSTS["TIMES"],
        seconds=REQUESTS_LIMIT_GET_POSTS["SECONDS"],
    ))]
)
async def get_post(
        post_id: int,
        db: Session = Depends(get_db)):
    """ Get a saved post by post_id """
    post = db.query(Post).filter(
        cast("ColumnElement[bool]", Post.id == post_id)
    ).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found"
        )
    adapter = TypeAdapter(CompletePostSchema)
    return adapter.validate_python(post)


@posts_router.post("", response_model=CompletePostSchema, status_code=status.HTTP_201_CREATED)
async def add_post(
        post: PostSchema,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """ Adds a new post into the database. """
    new_post = Post(**post.model_dump())
    new_post.creator = user
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    adapter = TypeAdapter(CompletePostSchema)
    return adapter.validate_python(new_post)


async def get_post_from_user(db: Session, post_id: int, user: UserViewSchema) -> query.Query:
    posts = db.query(Post).filter(cast("ColumnElement[bool]", Post.id == post_id))
    if posts.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found"
        )
    posts = posts.filter(Post.creator == user)
    if posts.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You cannot edit someone else's post"
        )
    return posts


@posts_router.put("/{post_id}", response_model=CompletePostSchema, status_code=status.HTTP_200_OK)
async def update_post(
        post_id: int,
        post: PostSchema,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """ Updates a post """
    posts = await get_post_from_user(db=db, post_id=post_id, user=user)
    posts.update(post.model_dump())
    db.commit()
    adapter = TypeAdapter(CompletePostSchema)
    return adapter.validate_python(posts.first())


@posts_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: int,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """ Deletes a post from the database. """
    post = await get_post_from_user(db=db, post_id=post_id, user=user)
    post.delete()
    db.commit()
    return {"msg": "Post Deleted"}


comments_router = APIRouter()


@comments_router.post("/{post_id}", response_model=CommentViewSchema, status_code=status.HTTP_201_CREATED)
async def add_comment(
        post_id: int,
        comment: CommentSchema,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """ Add a comment to the specified post. """
    new_comment = Comment(**comment.model_dump())
    new_comment.user_id = user.id
    new_comment.post_id = post_id
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    adapter = TypeAdapter(CommentViewSchema)
    return adapter.validate_python(new_comment)


@comments_router.get("/{post_id}", response_model=List[CommentViewSchema], status_code=status.HTTP_200_OK)
async def list_comments(
        post_id: int,
        query_params: CommentsQueryParams = Depends(CommentsQueryParams),
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """ Returns all comments for a specific post. """
    comments = db.query(Comment).filter(cast("ColumnElement", Comment.post_id == post_id))
    if query_params.limit and query_params.limit:
        comments.limit(query_params.limit)
        comments.offset((query_params.page - 1) * query_params.limit)
    comments = comments.all()
    adapter = TypeAdapter(List[CommentViewSchema])
    return adapter.validate_python(comments)


@comments_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        comment_id: int,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Deletes a comment with the provided <comment_id> from the database.
    """
    comment = db.query(Comment).filter(cast("ColumnElement", Comment.id == comment_id))
    if comment.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment not found"
        )
    comment.delete()
    db.commit()
    return {"msg": "Comment Deleted"}
