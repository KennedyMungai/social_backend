"""The script that contains all our model definitions"""
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Post(Base):
    """The Post template

    Args:
        Base (Class): The parent class for the Post class
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    rating = Column(Integer)