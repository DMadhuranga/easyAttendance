from flask import request, jsonify
from classes.User import User
from database.userDB import userDB

class userController:
    def addStaff(self):
        if (request.is_json):
            data = request.get_json()
            if (('userName' in data) and ('password' in data)):
                userName = data['userName']
                password = data['password']
                if(not userName.isalnum()):
                    return jsonify(error="Invalid student id")
                if(len(userName)>25):
                    return jsonify(error="Maximum 25 characters for student id")
                if (len(password) < 8):
                    return jsonify(error="Minimum 8 characters for password")
                conn = userDB.getConnection('database/example.db')
                exists = userDB.doesUserNameExist(conn,userName)
                if(exists==None):
                    return jsonify(error="Database error")
                elif(exists):
                    return jsonify(error="Duplicate userName")
                else:
                    id = userDB.addStaff(conn,userName,password)
                    return jsonify(id=id)
        return jsonify(error="Invalid request")

    def getUser(userId):
        conn = userDB.getConnection('database/example.db')
        user = userDB.getUser(conn,userId)
        if(user==None):
            return jsonify(error="user not found")
        return jsonify(userId=user.getUserId(),userName = user.getUserName(),roleId=user.getRoleId(),password= user.getPassword())

    def getUserByUserName(userName):
        conn = userDB.getConnection('database/example.db')
        user = userDB.getUserByName(conn, userName)
        if (user == None):
            return jsonify(error="user not found")
        return jsonify(userId=user.getUserId(), userName=user.getUserName(), roleId=user.getRoleId(),password=user.getPassword())
