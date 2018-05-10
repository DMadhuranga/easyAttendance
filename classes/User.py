class User:

    # this class represents an entry in user table in the database

    userName = ""
    password = ""
    userId = ""
    roleId = ""

    def __init__(self,userId,userName,password,roleId):
        self.userId = userId
        self.password = password
        self.userName = userName
        self.roleId = roleId

    def getUserName(self):
        return self.userName

    def getUserId(self):
        return self.userId

    def getPassword(self):
        return self.password

    def setUserId(self,userId):
        self.userId = userId

    def getRoleId(self):
        return self.roleId

    def printUser(self):
        # method used for testing

        print("userId",self.getUserId())
        print("userName", self.getUserName())
        print("Password", self.getPassword())
        print("roleId", self.getRoleId())

    def getJson(self):
        return ""