from sqlalchemy import Column,  Integer, Sequence, String, Boolean
from src.database.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, Sequence('Id'), primary_key=True)
    email = Column('email', String(64), nullable=False) # unique index
    name = Column('name', String(64), nullable=False)
    is_admin = Column('is_admin', Boolean, nullable=True, default=False)

    def __int__(self, name, email, is_admin):
        self.name = name
        self.email = email
        self.is_admin = is_admin
