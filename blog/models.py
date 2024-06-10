from typing import cast

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.connection import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    body = Column(Text(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return f'f<Post {self.title}>'


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    body = Column(Text(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)

    creator = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    responses = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")
    parent = relationship("Comment", back_populates="responses", remote_side=[cast("ColumnClause", id)])

    def __repr__(self):
        return f'f<Comment {self.id}>'
