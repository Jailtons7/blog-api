from sqlalchemy import Column, Integer, String, Boolean

from db.connection import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f'f<User {self.username}>'


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    body = Column(String(500), nullable=False)

    def __repr__(self):
        return f'f<Post {self.title}>'
