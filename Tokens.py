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