from flask import request, jsonify
from classes.Student import Student
from classes.Section import Section
from database.studentDB import studentDB

dbName = 'database/example.db'

class studentController:

    # this class handles all the requests related to student details
    # uses studentDB database access class to access database

    def addStudent(request):
        if (request.is_json):
            data = request.get_json()
            if (('studentId' in data) and ('studentName' in data)):
                studentId = data['studentId']
                studentName = data['studentName']
                if(not studentId.isalnum()):
                    return jsonify(error="Invalid student id")
                if(len(studentId)>25):
                    return jsonify(error="Maximum 25 characters for student id")
                if (len(studentName) > 200):
                    return jsonify(error="Maximum 200 characters for student name")
                conn = studentDB.getConnection(dbName)
                exists = studentDB.doesStudentIdExist(conn,studentId)
                if(exists==None):
                    return jsonify(error="Database error")
                elif(exists):
                    return jsonify(error="Duplicate student id")
                else:
                    id = studentDB.addStudent(conn, studentId, studentName)
                    return jsonify(id=id)
        return jsonify(error="Invalid request")

    def getStudent(id):
        conn = studentDB.getConnection(dbName)
        student = studentDB.getStudent(conn,id)
        noOfImages = studentDB.getNumberOfImages(conn,id)
        if noOfImages==None:
            noOfImages = 0
        if(student==None):
            return jsonify(error="student not found")
        return jsonify(id=student.getId(),studentId=student.getStudentId(),studentName=student.getStudentName(),noOfImages=noOfImages)

    def getStudentByStudentId(studentId):
        conn = studentDB.getConnection(dbName)
        student = studentDB.getStudentByStudentId(conn,studentId)
        if(student==None):
            return jsonify(error="student not found")
        return jsonify(id=student.getId(),studentId=student.getStudentId(),studentName=student.getStudentName())

    def getStudents():
        conn = studentDB.getConnection(dbName)
        students = studentDB.getStudents(conn)
        if(students==None):
            return jsonify(error="Student information not available")
        retStudents = []
        for student in students:
            retStudents.append({'id':student.getId(),'studentId':student.getStudentId(),'studentName':student.getStudentName()})
        return jsonify(students=retStudents)

    def saveStudentImage(id):
        conn = studentDB.getConnection(dbName)
        return studentDB.addImage(conn,id,"jpg")

    def getStudentPictures(sessionId):
        conn = studentDB.getConnection(dbName)
        return studentDB.getSessionPhotos(conn,sessionId)

    def getEnrolledSections(id):
        conn = studentDB.getConnection(dbName)
        sections = studentDB.getEnrolledSections(conn,id)
        if(sections==None):
            return jsonify(error="Section information not available")
        retStudents = []
        for section in sections:
            retStudents.append({'courseId':section.getCourseId(),'courseCode':section.getCourseCode(),'courseTitle':section.getCourseTitle(),
                                'sectionId': section.getSectionId(), 'semester': section.getSemester(),
                                'year': section.getYear()})
        return jsonify(sections=retStudents)

    def numberOfPhotos(id):
        conn = studentDB.getConnection(dbName)
        students = studentDB.getNumberOfImages(conn,id)
        if(students==None):
            return jsonify(error="Student information not available")
        return jsonify(numberOfImages=students)

    def removeStudentImages(id):
        conn = studentDB.getConnection(dbName)
        studentDB.removeStudentImages(conn,id)
        return jsonify(success="Done")