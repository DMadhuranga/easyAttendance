class Attendance:

    # this class represents a row in attendance table in the database
    # a student's attendance of a particular session

    id = ""
    studentId = ""
    studentName = ""
    attended = ""
    # attended will be 1 of the student have attended, else 0
    sessionId = ""

    def __init__(self,id,studentId,studentName,sessionId,attended):
        self.id = id
        self.studentId = studentId
        self.studentName = studentName
        self.attended = attended
        self.sessionId = sessionId

    def getStudentName(self):
        return self.studentName

    def getStudentId(self):
        return self.studentId

    def getId(self):
        return self.id

    def getSessionId(self):
        return self.sessionId

    def getAttended(self):
        return self.attended

    def printStudent(self):
        # method used for test purposes

        print("id : " + str(self.getId()))
        print("studentId : "+self.getStudentId())
        print("studentName : " + self.getStudentName())