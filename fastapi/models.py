from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(Date)
