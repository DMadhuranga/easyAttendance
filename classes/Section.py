class Section:

    # this class represents an entry in section table in the database

    sectionId = ""
    courseId = ""
    courseCode = ""
    courseTitle = ""
    year = ""
    semester = ""

    def __init__(self,courseId,courseCode,courseTitle,sectionId,year,semester):
        self.courseId = courseId
        self.sectionId = sectionId
        self.courseCode = courseCode
        self.courseTitle = courseTitle
        self.year = year
        self.semester = semester

    def getCourseId(self):
        return self.courseId

    def getSectionId(self):
        return self.sectionId

    def getSemester(self):
        return self.semester

    def getYear(self):
        return self.year

    def getCourseCode(self):
        return self.courseCode

    def getCourseTitle(self):
        return self.courseTitle

    def printCourse(self):
        # method used for testing

        print("SectionId : " + str(self.getSectionId()))
        print("CourseId : "+str(self.getCourseId()))
        print("Year : " + str(self.getYear()))
        print("Semester : " + self.getSemester())