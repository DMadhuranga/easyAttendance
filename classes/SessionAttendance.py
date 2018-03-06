class SessionAttendance:

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

    def addStudent(self,studentId,attended):
        self.students[studentId] = attended

    def getStudentAttendance(self):
        return self.students

    def isMarked(self):
        return self.marked