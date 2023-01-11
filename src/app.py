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
    user_name = request.json.get('user_name')
    # email is the password
    email = request.json.get('email')
    is_admin = request.json.get('is_admin')
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
def add_books(db):
    username = request.auth[0]
    email = request.auth[1]
    is_admin_user = LibraryDB().is_admin_user(db, username, email)
    if is_admin_user:
        print(is_admin_user)
        # TODO: add book
        return {'status_code': '200', 'message': 'TODO'}
    else:
        return {'status_code': '403', 'message': 'Forbidden for a non admin permission to add new book to the catalog'}

@library_app.route('/book/{book_id}', method=['DELETE'])
def delete_book():
    pass

@library_app.route('/books/catalog', method=['GET'])
def catalog():
    return 'Catalog!'


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
