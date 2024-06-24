from sqlalchemy import Column, Integer, String

from src.db import Base


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    cook_time = Column(Integer, nullable=False)
    views = Column(Integer, default=0, nullable=True)
    description = Column(String, nullable=True)
