from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from base import Base



class Book(Base):
    __table_name__ = 'book'

    id = Column('id', Integer, Sequence('Id'), primary_key=True)
    book_title = Column('book_title', String(64), nullable=False) # unique index
    author_name = Column('author_name', String(64), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    # TODO checked_out_date

    def __int__(self, author_name, book_title):
        self.book_title = book_title
        self.author_name = author_name

