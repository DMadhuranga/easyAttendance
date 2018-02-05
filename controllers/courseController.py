from flask import request, jsonify
from classes.Course import Course
from database.courseDB import courseDB

class courseController:

    def addCourse(request):
        if (request.is_json):
            data = request.get_json()
            if (('courseCode' in data) and ('courseTitle' in data)):
                courseCode = data['courseCode']
                courseTitle = data['courseTitle']
                if (not courseCode.isalnum()):
                    return jsonify(error="Invalid course code")
                if (len(courseCode) > 25):
                    return jsonify(error="Maximum 25 characters for course code")
                if (len(courseTitle) > 200):
                    return jsonify(error="Maximum 200 characters for course title")
                conn = courseDB.getConnection('database/example.db')
                courseId = courseDB.addCourse(conn,courseCode,courseTitle)
                return jsonify(courseId=courseId)
        return jsonify(error="Invalid request")

    def getCourse(courseId):
        conn = courseDB.getConnection('database/example.db')
        course = courseDB.getCourse(conn,courseId)
        if(course==None):
            return jsonify(error="student not found")
        return jsonify(courseId=course.getCourseId(),courseCode=course.getCourseCode(),courseTitle=course.getCourseTitle())

    def getCourseByCode(courseCode):
        conn = courseDB.getConnection('database/example.db')
        course = courseDB.getCourseByCode(conn,courseCode)
        if(course==None):
            return jsonify(error="student not found")
        return jsonify(courseId=course.getCourseId(), courseCode=course.getCourseCode(),courseTitle=course.getCourseTitle())