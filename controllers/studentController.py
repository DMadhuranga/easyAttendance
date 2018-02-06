from flask import request, jsonify
from classes.Student import Student
from database.studentDB import studentDB

class studentController:

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
                conn = studentDB.getConnection('database/example.db')
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
        conn = studentDB.getConnection('database/example.db')
        student = studentDB.getStudent(conn,id)
        if(student==None):
            return jsonify(error="student not found")
        return jsonify(id=student.getId(),studentId=student.getStudentId(),studentName=student.getStudentName())

    def getStudentByStudentId(studentId):
        conn = studentDB.getConnection('database/example.db')
        student = studentDB.getStudentByStudentId(conn,studentId)
        if(student==None):
            return jsonify(error="student not found")
        return jsonify(id=student.getId(),studentId=student.getStudentId(),studentName=student.getStudentName())

    def getStudents():
        conn = studentDB.getConnection('database/example.db')
        students = studentDB.getStudents(conn)
        if(students==None):
            return jsonify(error="Student information not available")
        retStudents = []
        for student in students:
            retStudents.append({'id':student.getId(),'studentId':student.getStudentId(),'studentName':student.getStudentName()})
        return jsonify(students=retStudents)