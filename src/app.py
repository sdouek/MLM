import os
from bottle import Bottle, auth_basic, request, run
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle_sqlalchemy import SQLAlchemyPlugin
from database.library_db import LibraryDB
from http import HTTPStatus

library_app = Bottle()
# TODO: validate None input for db configuration
uri = "mysql+pymysql://{}:{}@{}:{}/{}".format(os.getenv("DB_USER"), os.getenv("DB_PASSWD"), os.getenv("DB_HOST"),
                                              os.getenv("DB_PORT"), os.getenv("DB_NAME"))
engine = create_engine(uri)
sm = sessionmaker(bind=engine)
plugin = SQLAlchemyPlugin(engine, create_session=sm, keyword='db')
library_app.install(plugin)


@library_app.route('/user/register', method='POST')
def registration(db):

    print("request register user: {}".format(request.url))
    print("request body: {}".format(request.json))
    body = request.json
    user_name = body.get('user_name')
    # email is the password
    email = body.get('email')
    is_admin = body.get('is_admin')
    # Before crete user , check if the user already exist
    existing_user = LibraryDB().get_user(db, user_name, email)
    if existing_user:
        return {'status_code': HTTPStatus.CONFLICT.value, 'message': 'User already exist'}
    # Create new user
    user = LibraryDB().add_user(db, user_name, email, is_admin)
    if user:
        return {'status_code': HTTPStatus.OK.value, 'message': 'Successful registration'}


def validate_user_credentials(username, email):
    db = sm()
    user = LibraryDB.get_user(db, username, email)
    return user is not None
    # if not user:
    #     raise Exception({'status_code': '401', 'message': 'Unauthorized: bad credentials'})
    # return True


@library_app.route('/book', method='POST')
@auth_basic(validate_user_credentials)
def add_book(db):
    username = request.auth[0]
    email = request.auth[1]
    is_admin_user = LibraryDB().is_admin_user(db, username, email)
    # Only admin user can add book
    if is_admin_user:
        body = request.json
        if not body:
            return {'status_code': HTTPStatus.BAD_REQUEST.value, 'message': 'Bad Request: not book details provided in json request'}
        book_title = body.get('book_title')
        author_name = body.get('author_name')
        book_id = LibraryDB.add_book(db,  author_name, book_title)
        if book_id:
            return {'status_code': HTTPStatus.OK.value, 'message': 'Book id : {} added successfully'.format(book_id)}
    else:
        return {'status_code': HTTPStatus.FORBIDDEN.value, 'message': 'Forbidden for a non admin permission to add new book to the catalog'}


@library_app.route('/book/<book_id>', method='DELETE')
@auth_basic(validate_user_credentials)
def delete_book(db, book_id):
    username = request.auth[0]
    email = request.auth[1]
    is_admin_user = LibraryDB().is_admin_user(db, username, email)
    # Only admin user can delete book
    if is_admin_user:
        book_removed = LibraryDB.remove_book(db, book_id)
        if book_removed:
            return {'status_code': HTTPStatus.OK.value, 'message': 'Book removed successfully'}
    else:
        return {'status_code':  HTTPStatus.FORBIDDEN.value, 'message': 'Forbidden for a non admin permission to remove book from the catalog'}


@library_app.route('/catalog', method='GET')
@auth_basic(validate_user_credentials)
def get_catalog(db):
    body = request.json
    if not body:
        return {'status_code': HTTPStatus.BAD_REQUEST.value, 'message': 'Bad Request: not book details provided in json request'}
    book_title = body.get('book_title')
    author_name = body.get('author_name')
    is_available = body.get('is_available') # TODO: validate is a boolean input
    catalog = LibraryDB.get_catalog(db, author_name, book_title, is_available)
    if not catalog:
        return {'status_code': HTTPStatus.NOT_FOUND.value, 'message': 'Not books found for this filter'}
    return {'status_code': HTTPStatus.OK.value, 'message': 'Catalog for your filter: {}'.format(catalog)}


@library_app.route('/checkout/book/<book_id>', method='PUT')
@auth_basic(validate_user_credentials)
def checkout_book(db, book_id):
    user = LibraryDB.get_user(db, request.auth[0], request.auth[1])
    checked_out_book, msg = LibraryDB.checkout_book_by_id(db, book_id, user.id)
    if not checked_out_book:
        return {'status_code': HTTPStatus.TOO_MANY_REQUESTS.value, 'message': msg}
    return {'status_code': HTTPStatus.OK.value, 'message': 'Book: {} checked out for user: {} successfully'.format(book_id, request.auth[0])}


@library_app.route('/return/book/<book_id>', method='PUT')
@auth_basic(validate_user_credentials)
def return_book(db, book_id):
    user = LibraryDB.get_user(db, request.auth[0], request.auth[1])
    book_returned, msg = LibraryDB.return_book(db, book_id, user.id)
    if not book_returned:
        return {'status_code':  HTTPStatus.CONFLICT.value, 'message': msg}
    return {'status_code': HTTPStatus.OK.value, 'message': 'Book: {} returned successfully'.format(book_id)}


@library_app.route('/checked_out/book', method='GET')
@auth_basic(validate_user_credentials)
def view_checked_out_books(db):
    username = request.auth[0]
    email = request.auth[1]
    body = request.json
    is_admin_user = LibraryDB().is_admin_user(db, username, email)
    if not is_admin_user and not username == body.get('username'):
        return {'status_code': HTTPStatus.FORBIDDEN.value,
                'message': 'Forbidden for a non admin permission to view checked out books from other users'}
    user = LibraryDB.get_user(db, body.get('user_name'), body.get('email')) if is_admin_user \
            else LibraryDB.get_user(db, request.auth[0], request.auth[1])
    if not user:
        return {'status_code': HTTPStatus.NOT_FOUND.value, 'message': 'Not found user'}
    checked_out_books = LibraryDB.get_checked_out_by_user(db, user.id)
    if not checked_out_books:
        return {'status_code': HTTPStatus.FORBIDDEN.value, 'message': 'Not books found for user {}'.format(user.name)}
    return {'status_code': HTTPStatus.OK.value, 'message': 'Books checked out by user {} : {}'.format(user.name, checked_out_books)}


if __name__ == '__main__':
    run(library_app, host='0.0.0.0', port=8084, debug=True)