from flask.ext.pymongo import PyMongo

import os
import unittest

from aniseasons.app import app, mongo
from aniseasons.manage import createuser, deleteuser

class AniseasonsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_createuser(self):
        with app.app_context():
            self.assertEqual(createuser('testington', 'test'), 'testington was successfully created')

    def test_deleteuser(self):
        with app.app_context():
            self.assertEqual(deleteuser('testington'), 'testington was successfully deleted')

if __name__ == '__main__':
    unittest.main()
