from sqlalchemy import Column, Integer, String, Boolean

from db.connection import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    body = Column(String(500), nullable=False)

    def __repr__(self):
        return f'f<Post {self.title}>'
