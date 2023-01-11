from database.book import Book
from database.user import User
from sqlalchemy import func


class LibraryDB:

    @classmethod
    def get_user(cls, db, user_name, email):
        user = db.query(User).filter(User.name == user_name, User.email == email).first()
        return user

    @classmethod
    def is_admin_user(cls, db, user_name, email):
        user = LibraryDB.get_user(db, user_name, email)
        return user.is_admin

    @classmethod
    def add_user(cls, db, name, email, is_admin=False):
        user = User(name, email, is_admin)
        LibraryDB.add_row(db, user)
        db.commit()
        return True

    @classmethod
    def add_book(cls, db, author_name, book_title):
        book = Book(author_name, book_title)
        LibraryDB.add_row(db, book)
        db.commit()
        return True

    @classmethod
    def get_book(cls, db, author_name, book_title):
        book = db.query(Book).filter(Book.author_name == author_name, Book.book_title == book_title).first()
        return book

    @classmethod
    def remove_book(cls, db, book_id):
        db.query(Book).filter(Book.id == book_id).delete()
        db.commit()
        return True

    @classmethod
    def add_row(cls, db, obj):
        db.add(obj)
        db.commit()

    @classmethod
    def get_books(cls, db, author_name, book_title, is_available):
        try:
            query_filter = db.query.filter()
            if author_name:
                query_filter = query_filter.fiter(Book.author_name == author_name)
            if book_title:
                query_filter = query_filter.fiter(Book.book_title == book_title)
            if is_available:
                query_filter = query_filter.fiter(Book.user_id == 'None')

            books = db.query(Book).filter(query_filter).all()
        except Exception as e:
            raise e
        return books

    @classmethod
    def checkout_book_by_id(cls, db, user_id, book_id):
        book = LibraryDB.get_book_by_id(db, book_id)
        if book and book.user_id is None:
            total_checkout = LibraryDB.get_total_checked_out_books(db, user_id)
            if total_checkout >= 10:
                return False, 'max limit of checkout books'
            book.user_id = user_id
            db.commit()
            return True
        return False

    @classmethod
    def get_book_by_id(cls, db, book_id):
        book = db.query(Book).filter(Book.id == book_id)
        return book

    @classmethod
    def get_total_checked_out_books(cls, db, user_id):
        total_checked_out = db.query(func.count(Book)).filter(Book.user_id == user_id).scalar()
        return total_checked_out

    @classmethod
    def return_book(cls, db, book_id, user_id):
        book = LibraryDB.get_book_by_book_id(db, book_id)
        if book.user_id == user_id:
            book.user_id = None
            db.commit()
            return True
        return False

    @classmethod
    def view_checked_out_books_by_userid(cls, db, user_id):
        checked_out_book = db.query(Book).filter(Book.user_id == user_id).all()
        return checked_out_book







