from flask import request, jsonify
from classes.User import User
from database.userDB import userDB

dbName = 'database/example.db'

class userController:

    # this class handles all the requests related to user details
    # uses both userDB database access class to access database

    def addUser(self):
        # add a new user to the system given a json with userName, password and roleId

        if (request.is_json):
            data = request.get_json()
            if ((('userName' in data) and ('password' in data)) and ('RoleId' in data)):
                userName = data['userName']
                password = data['password']
                role = data['RoleId']
                if(not userName.isalnum()):
                    return jsonify(error="Invalid student id")
                if(len(userName)>25):
                    return jsonify(error="Maximum 25 characters for student id")
                if (len(password) < 8):
                    return jsonify(error="Minimum 8 characters for password")
                conn = userDB.getConnection(dbName)
                exists = userDB.doesUserNameExist(conn,userName)
                if(exists==None):
                    return jsonify(error="Database error")
                elif(exists):
                    return jsonify(error="Duplicate userName")
                else:
                    if(role=='1'):
                        id = userDB.addStaff(conn, userName, password)
                    else:
                        id = userDB.addAdmin(conn, userName, password)
                    return jsonify(id=id)
        return jsonify(error="Invalid request")

    def getUser(userId):
        # get a json with details of a user given the userId

        conn = userDB.getConnection(dbName)
        user = userDB.getUser(conn,userId)
        if(user==None):
            return jsonify(error="user not found")
        return jsonify(userId=user.getUserId(),userName = user.getUserName(),roleId=user.getRoleId(),password= user.getPassword())

    def getUserByUserName(userName):
        # get a json with details of a user given the userName

        conn = userDB.getConnection(dbName)
        user = userDB.getUserByName(conn, userName)
        if (user == None):
            return jsonify(error="user not found")
        return jsonify(userId=user.getUserId(), userName=user.getUserName(), roleId=user.getRoleId(),password=user.getPassword())

    def getAllUsers():
        # get a json with details of all the users (list of users)

        conn = userDB.getConnection(dbName)
        users = userDB.getUsers(conn)
        if(users==None):
            return jsonify(error="User information not available")
        retStudents = []
        for user in users:
            role = "Admin"
            if(user.getRoleId()==1):
                role = "Support Staff"
            retStudents.append({'userId':user.getUserId(),'userName':user.getUserName(),'password':user.getPassword(),'role':role})
        return jsonify(users=retStudents)

    def checkValidPassword(self):
        # check for userId and password match given a json with userId and password

        if (request.is_json):
            data = request.get_json()
            if (('userId' in data) and ('password' in data)):
                userId = data['userId']
                password = data['password']
                conn = userDB.getConnection(dbName)
                user = userDB.checkPassword(conn,userId,password)
                if(user==None):
                    return jsonify(error="Database error")
                elif(user):
                    return jsonify(success="Password matching")
                else:
                    return jsonify(error="Incorrect Password")
        return jsonify(error="Invalid request")

    def changePassword(self):
        # change password of an user

        if (request.is_json):
            data = request.get_json()
            if (('userId' in data) and ('password' in data)):
                userId = data['userId']
                password = data['password']
                if (len(password) < 8):
                    return jsonify(error="Minimum 8 characters for password")
                conn = userDB.getConnection(dbName)
                userDB.changePassword(conn,userId,password)
                return jsonify(success="Password changed")
        return jsonify(error="Invalid request")