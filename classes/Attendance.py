class Attendance:
    id = ""
    studentId = ""
    studentName = ""
    attended = ""
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
        print("id : " + str(self.getId()))
        print("studentId : "+self.getStudentId())
        print("studentName : " + self.getStudentName())