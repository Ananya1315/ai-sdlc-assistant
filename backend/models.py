from sqlalchemy import Column, Integer, Text
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    requirement = Column(Text)
    user_stories = Column(Text)
    acceptance_criteria = Column(Text)
    test_cases = Column(Text)
    user_id = Column(Integer)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, index=True)
    password = Column(Text)
    is_pro = Column(Integer, default=0)