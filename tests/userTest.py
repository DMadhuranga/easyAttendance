import unittest
from database.userDB import userDB
from classes.User import User
import sqlite3


class GetConnectionTestCase(unittest.TestCase):
    def test_with_valid_db_details(self):
        self.assertIsInstance(userDB.getConnection('../database/example.db'),sqlite3.Connection)

    def test_with_invalid_db_details(self):
        self.assertEqual(userDB.getConnection('/database/example.db'),None,"Incorect, database connect details are wrong")

class GetUserTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = userDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_getUsers(self):
        users = userDB.getUsers(self.conn)
        self.assertIsInstance(users[0],User)

    def test_getUser(self):
        user = userDB.getUser(self.conn,"1")
        self.assertEqual(user.getUserName(), "admin","Incorrect user object")

    def test_getUserByName(self):
        user = userDB.getUserByName(self.conn,"admin")
        self.assertEqual(user.getUserName(), "admin","Incorrect user object")

class DoesUserNameExistTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = userDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_exist_username(self):
        self.assertEqual(userDB.doesUserNameExist(self.conn,'admin'),True,"Incorrect, user name exists")

    def test_non_exist_username(self):
        self.assertEqual(userDB.doesUserNameExist(self.conn,'admin12'),False,"Incorrect, user does not exists")

class checkLoginTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = userDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_valid_login_details(self):
        self.assertIsInstance(userDB.checkLogin(self.conn,"admin","superadmin"),User)

    def test_invalid_login_details_with_valid_username(self):
        self.assertEqual(userDB.checkLogin(self.conn, "admin", "supedmin"), False,"Incorrect, login details are not valid")

    def test_invalid_login_details_with_non_existing_user(self):
        self.assertEqual(userDB.checkLogin(self.conn, "adn", "supedmin"), False,"Incorrect, login details are not valid")

class checkPasswordTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = userDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_valid_details(self):
        self.assertEqual(userDB.checkPassword(self.conn,"1","superadmin"),True,"Incorrect, password is valid")

    def test_invalid_password_with_valid_username(self):
        self.assertEqual(userDB.checkPassword(self.conn, "1", "supe12dmin"), False, "Incorrect, password is not valid")

    def test_invalid_password_with_non_existing_user(self):
        self.assertEqual(userDB.checkPassword(self.conn, "0", "superadmin"), False, "Incorrect, password is not valid")