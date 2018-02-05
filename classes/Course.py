class Course:
    courseId = ""
    courseCode = ""
    courseTitle = ""

    def __init__(self,courseId,courseCode,courseTitle):
        self.courseId = courseId
        self.courseTitle = courseTitle
        self.courseCode = courseCode

    def getCourseId(self):
        return self.courseId

    def getCourseCode(self):
        return self.courseCode

    def getCourseTitle(self):
        return self.courseTitle

    def printCourse(self):
        print("CourseId : "+str(self.getCourseId()))
        print("CourseCode : " + self.getCourseCode())
        print("CourseTitle : " + self.getCourseTitle())