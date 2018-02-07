class Session:

    sectionId=""
    year = ""
    semester = ""
    courseId = ""
    courseCode = ""
    courseTitle = ""
    startingTime=""
    date = ""
    sessionId = ""
    marked = ""


    def __init__(self,courseId,courseCode,courseTitle,sectionId,year,semester,sessionId,date,startingTime,marked):
        self.courseId = courseId
        self.courseTitle = courseTitle
        self.courseCode = courseCode
        self.sectionId = sectionId
        self.semester = semester
        self.year = year
        self.sessionId = sessionId
        self.date = date
        self.startingTime = startingTime
        self.marked = marked

    def getCourseId(self):
        return self.courseId

    def getCourseCode(self):
        return self.courseCode

    def getCourseTitle(self):
        return self.courseTitle

    def getSectionId(self):
        return self.sectionId

    def getYear(self):
        return self.year

    def getDate(self):
        return self.date

    def getSemester(self):
        return self.semester

    def getSessionId(self):
        return self.sessionId

    def getStartingTime(self):
        return self.startingTime

    def getMarked(self):
        return self.marked

    def printCourse(self):
        print("CourseId : "+str(self.getCourseId()))
        print("CourseCode : " + self.getCourseCode())
        print("CourseTitle : " + self.getCourseTitle())