import sqlite3
from sqlite3 import Error
from classes.User import User
from passlib.hash import pbkdf2_sha256

class userDB:

    # userDB class is the database access class for all the user related information

    def getConnection(db_file):
        # initialize database connection and return database connector

        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def createTable(conn):
        # create all the database datatables if they do not exists already

        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id integer PRIMARY KEY AUTOINCREMENT,username varchar(25) NOT NULL, password varchar(200) NOT NULL,role_id integer(1) NOT NULL, deleted integer(1) DEFAULT 0)")

    def addAdmin(conn,userName,password):
        # add a new admin (new user table entry with role id 0)

        array = [userName, pbkdf2_sha256.hash(password),0]
        cursor = conn.cursor()
        cursor.execute("insert into user (username,password,role_id) values (?,?,?)", array)
        conn.commit()
        return cursor.lastrowid

    def addStaff(conn,userName,password):
        # add a new staff member (new user table entry with role id 1)

        array = [userName, pbkdf2_sha256.hash(password),1]
        cursor = conn.cursor()
        cursor.execute("insert into user (username,password,role_id) values (?,?,?)", array)
        conn.commit()
        return cursor.lastrowid

    def getUsers(conn):
        # get details of all the users (list of user objects)

        if(conn):
            cursor = conn.cursor()
            cursor.execute("select * from user where deleted='0'")
            rows = cursor.fetchall()
            users = []
            for row in rows:
                user = User(row[0], row[1], row[2], row[3])
                users.append(user)
            return users
        return None

    def getUser(conn,userId):
        # get details of a user (user object) given the userId

        if (conn):
            cursor = conn.cursor()
            array = [userId]
            cursor.execute("select * from user where user_id=? and deleted='0'",array)
            rows = cursor.fetchall()
            if(len(rows)==1):
                user = User(rows[0][0],rows[0][1],rows[0][2],rows[0][3])
                return user
        return None

    def getUserByName(conn,userName):
        # get details of a user (user object) given the userName

        if (conn):
            cursor = conn.cursor()
            array = [userName]
            cursor.execute("select * from user where username=? and deleted='0'",array)
            rows = cursor.fetchall()
            if(len(rows)==1):
                user = User(rows[0][0],rows[0][1],rows[0][2],rows[0][3])
                return user
        return None

    def doesUserNameExist(conn,userName):
        # check whether a user exists with the given userName

        if(conn):
            cursor = conn.cursor()
            array = [userName]
            cursor.execute("select * from user where username=? and deleted='0'", array)
            rows = cursor.fetchall()
            if (len(rows)>0):
                return True
            return False
        return None

    def deleteUser(conn,userId):
        # delete the user (mark user as deleted in database) given the userId

        if(conn):
            cursor = conn.cursor()
            array = [userId]
            cursor.execute("update user set deleted='1' where user_id=?", array)
            conn.commit()

    def checkLogin(conn,username,password):
        # check whether given username and password match and return the user details if they match

        if (conn):
            cursor = conn.cursor()
            array = [username]
            cursor.execute("select * from user where username=? and deleted='0'", array)
            rows = cursor.fetchall()
            if (len(rows) == 1):
                ret_password = rows[0][2]
                if(pbkdf2_sha256.verify(password, ret_password)):
                    user = User(rows[0][0],rows[0][1],rows[0][2],rows[0][3])
                    return user
            return False
        return None

    def checkPassword(conn,userId,password):
        # check whether given userId and password match

        if (conn):
            cursor = conn.cursor()
            array = [userId]
            cursor.execute("select * from user where user_id=? and deleted='0'", array)
            rows = cursor.fetchall()
            if (len(rows) == 1):
                ret_password = rows[0][2]
                if(pbkdf2_sha256.verify(password, ret_password)):
                    return True
            return False
        return None

    def changePassword(conn,userId,password):
        # cheange the password of a given user

        array = [pbkdf2_sha256.hash(password),userId]
        cursor = conn.cursor()
        cursor.execute("update user set password=? where user_id=? and deleted='0'", array)
        conn.commit()