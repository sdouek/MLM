import unittest
from bottle import Bottle, request
from src.database.library_db import LibraryDB

# TODO - add unittest

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.app = LibraryDB.library_app
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}



if __name__ == '__main__':
    unittest.main()
#python -m unittest test_app.py





