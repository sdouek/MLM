from sqlalchemy import Column,  Integer, Sequence, String, Boolean
from database.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, Sequence('Id'), primary_key=True)
    password = Column('password', String(64), nullable=False) # unique index
    name = Column('name', String(64), nullable=False)
    is_admin = Column('is_admin', Boolean, nullable=True, default=False)

    def __init__(self, name, password, is_admin):
        self.name = name
        self.password = password
        self.is_admin = is_admin
