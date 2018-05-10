class SessionAttendance:

    # this class represents an entry in attendance table in the database

    sectionId=""
    startingTime=""
    date = ""
    sessionId = ""
    students = {}
    marked = False


    def __init__(self,sectionId,sessionId,date,startingTime,marked):
        self.sectionId = sectionId
        self.sessionId = sessionId
        self.date = date
        self.startingTime = startingTime
        self.marked = marked

    def getSectionId(self):
        return self.sectionId

    def getDate(self):
        return self.date

    def getSessionId(self):
        return self.sessionId

    def getStartingTime(self):
        return self.startingTime

    def addStudent(self,id,studentId,studentName,attended):
        #print("Adding to "+str(self.sessionId)+" student "+str(studentName)+" attendance "+str(attended))
        self.students[id] = [studentId,studentName,attended]

    def getStudentAttendance(self):
        return self.students

    def isMarked(self):
        return self.marked

    def printStudents(self):
        for i in self.students:
            student = self.students[i]
            print(student)