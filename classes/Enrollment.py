class Enrollment:

    sectionId = ""
    id = ""

    def __init__(self,sectionId,id):
        self.id = id
        self.sectionId = sectionId

    def getId(self):
        return self.id

    def getSectionId(self):
        return self.sectionId

    def printCourse(self):
        print("SectionId : " + str(self.getSectionId()))
        print("Id : "+str(self.getId()))