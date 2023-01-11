import logging
from bottle import Bottle, auth_basic, request, run
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle_sqlalchemy import SQLAlchemyPlugin
from database.library_db import LibraryDB


logger = logging.getLogger(__name__)
library_app = Bottle()
# TODO: get params from env
user = 'm_user'
passwd = 'a:123456'
host = '127.0.0.1'
port = 3307
db_name = 'MLM_DB'
uri = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, passwd, host, port, db_name)
engine = create_engine(uri)
sm = sessionmaker(bind=engine)

plugin = SQLAlchemyPlugin(engine, create_session=sm, keyword='db')
library_app.install(plugin)


@library_app.route('/user/register', method=['POST'])
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
        return {'status_code': '409', 'message': 'User already exist'}
    # Create new user
    user = LibraryDB().add_user(db, user_name, email, is_admin)
    if user:
        return {'status_code': '200', 'message': 'Successful registration'}


def validate_user_credentials(username, email):
    db = sm()
    user = LibraryDB.get_user(db, username, email)
    return user is not None
    # if not user:
    #     raise Exception({'status_code': '401', 'message': 'Unauthorized: bad credentials'})
    # return True


@library_app.route('/book', method=['POST'])
@auth_basic(validate_user_credentials)
def add_book(db):
    username = request.auth[0]
    email = request.auth[1]
    is_admin_user = LibraryDB().is_admin_user(db, username, email)
    if is_admin_user:
        body = request.json
        if not body:
            return {'status_code': '400', 'message': 'Bad Request: not book details provided in json request'}
        book_title = body.get('book_title')
        author_name = body.get('author_name')
        book_id = LibraryDB.add_book(db,  author_name, book_title)
        if book_id:
            return {'status_code': '200', 'message': 'Book id : {} added successfully'.format(book_id)}
    else:
        return {'status_code': '403', 'message': 'Forbidden for a non admin permission to add new book to the catalog'}


@library_app.route('/book/<book_id>', method=['DELETE'])
@auth_basic(validate_user_credentials)
def delete_book(db, book_id):
    username = request.auth[0]
    email = request.auth[1]
    is_admin_user = LibraryDB().is_admin_user(db, username, email)
    if is_admin_user:
        book_removed = LibraryDB.remove_book(db, book_id)
        if book_removed:
            return {'status_code': '200', 'message': 'Book removed successfully'}
    else:
        return {'status_code': '403', 'message': 'Forbidden for a non admin permission to remove book from the catalog'}


@library_app.route('/catalog', method=['GET'])
@auth_basic(validate_user_credentials)
def get_catalog(db):
    body = request.json
    if not body:
        return {'status_code': '400', 'message': 'Bad Request: not book details provided in json request'}
    book_title = body.get('book_title')
    author_name = body.get('author_name')
    is_available = body.get('is_available') # TODO: validate is a boolean input
    catalog = LibraryDB.get_catalog(db, author_name, book_title, is_available)
    if not catalog:
        return {'status_code': '404', 'message': 'Not books found for this filter'}
    return {'status_code': '200', 'message': 'Catalog for your filter: {}'.format(catalog)}


if __name__ == '__main__':
    run(library_app, host='0.0.0.0', port=8084, debug=True)

    # curl - X
    # POST
    # http: // 127.0
    # .0
    # .1: 8084 / user / register - H
    # "Content-Type: application/json" - d
    # '{"email": "ssdds", "user_name": "100"}'

# curl GET http://127.0.0:8084/books/catalog
