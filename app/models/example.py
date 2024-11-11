from typing import Any

from sqlalchemy import (
    Column, 
    Integer,
    String
)

from app import db


class Example(db.Model):
    __tablename__ = 'table_example_name'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return 'Example(id=%s, name=%s)' %(self.id, self.name)
    
    def to_dict(self) -> dict[str, Any]:
        return { 'id': self.id, 'name': self.name }
