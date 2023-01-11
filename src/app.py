import logging
import bottle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle_sqlalchemy import SQLAlchemyPlugin
from database.library_db import LibraryDB


logger = logging.getLogger(__name__)
library_app = bottle.Bottle()
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

    logger.info("request register user: {}".format(bottle.request.url))
    logger.info("request body: {}".format(bottle.request.json))
    # {
    #     "user_name": "sdouek",
    #     "email": "sarimimig@gmail.com"
    # }
    user_name = bottle.request.json.get('user_name')
    email = bottle.request.json.get('email')
    # TODO
    # password
    # is admin
    db = LibraryDB().add_user(db, user_name, email)


@library_app.route('/book', method=['POST'])
def add_books():
    # {
    #     "book": {
    #                { "author_name": '',
    #                  "book_title": '' }
    # }
    db = LibraryDB()
    db.is_admin_user()

@library_app.route('/book/{book_id}', method=['DELETE'])
def delete_book():
    pass

@library_app.route('/books/catalog', method=['GET'])
def catalog():
    return 'Catalog!'


if __name__ == '__main__':
    bottle.run(library_app, host='0.0.0.0', port=8084, debug=True)

    # curl - X
    # POST
    # http: // 127.0
    # .0
    # .1: 8084 / user / register - H
    # "Content-Type: application/json" - d
    # '{"email": "ssdds", "user_name": "100"}'

# curl GET http://127.0.0:8084/books/catalog
