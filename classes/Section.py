class Section:

    sectionId = ""
    courseId = ""
    year = ""
    semester = ""

    def __init__(self,sectionId,courseId,year,semester):
        self.courseId = courseId
        self.sectionId = sectionId
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

    def printCourse(self):
        print("SectionId : " + str(self.getSectionId()))
        print("CourseId : "+str(self.getCourseId()))
        print("Year : " + str(self.getYear()))
        print("Semester : " + self.getSemester())