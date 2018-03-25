from classes.User import User
from random import *

class Tokens:
    tokens = {}
    def addToken(self,user):
        i = randint(1000000,2000000)
        while(i in self.tokens):
            i = randint(1000000, 2000000)
        self.tokens[i]=user
        return i

    def getUser(self,token):
        if(token in self.tokens):
            return self.tokens[token]
        return None

    def updateUser(self,token,user):
        if(token in self.tokens):
            self.tokens[token] = user

    def isLogged(self,headers):
        if('Token' in headers):
            token = int(headers['Token'])
            if (token in self.tokens):
                return True
        return False

    def isAdmin(self,headers):
        if('Token' in headers):
            token = int(headers['Token'])
            if (token in self.tokens):
                if(self.tokens[token].getRoleId()==0):
                    return True
        return False

    def isValidToken(self,token):
        token = int(token)
        if (token in self.tokens):
            return True
        return False

    def isValidAdminToken(self,token):
        token = int(token)
        if (token in self.tokens):
            if (self.tokens[token].getRoleId() == 0):
                return True
        return False

    def removeToken(self,token):
        if(token in self.tokens):
            self.tokens.pop(token, None)

    def getUserDetails(self,token):
        token = int(token)
        if (token in self.tokens):
            user = self.tokens[token]
            details = {'token':token,'userId':user.getUserId(),'userName':user.getUserName(),'password':user.getPassword(),'roleId':user.getRoleId()}
            if(user.getRoleId()==0):
                details['role']='Admin'
            else:
                details['role']="Staff Member"
            return details
        return None

    def cleanTokens(self):
        self.tokens.clear()