from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.connection import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    posts = relationship("Post", back_populates="creator")

    def __repr__(self):
        return f'f<User {self.username}>'

    def set_password(self, password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_pwd = pwd_context.hash(password)
        self.password = hashed_pwd

    def check_password(self, password: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.password)
