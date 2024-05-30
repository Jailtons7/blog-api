from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.connection import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    body = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="posts")

    def __repr__(self):
        return f'f<Post {self.title}>'
