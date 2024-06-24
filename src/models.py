from typing import List

from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import relationship, mapped_column, Mapped


from src.db import Base


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    cook_time = Column(Integer, nullable=False)
    views = Column(Integer, default=0, nullable=True)
    description = Column(String, nullable=True)
