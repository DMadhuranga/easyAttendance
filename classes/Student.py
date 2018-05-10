class Student:

    # this class represents an entry in student table in the database

    id = ""
    studentId = ""
    studentName = ""

    def __init__(self,id,studentId,studentName):
        self.id = id
        self.studentId = studentId
        self.studentName = studentName

    def getStudentName(self):
        return self.studentName

    def getStudentId(self):
        return self.studentId

    def getId(self):
        return self.id

    def printStudent(self):
        # method used for testing

        print("id : " + str(self.getId()))
        print("studentId : "+self.getStudentId())
        print("studentName : " + self.getStudentName())