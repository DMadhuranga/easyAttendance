from flask import request, jsonify
from classes.Course import Course
from classes.Section import Section
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

    def getCourses():
        conn = courseDB.getConnection('database/example.db')
        courses = courseDB.getCourses(conn)
        if(courses==None):
            return jsonify(error="COurse information not available")
        retCourses = []
        for course in courses:
            retCourses.append({'courseId':course.getCourseId(),'courseCode':course.getCourseCode(),'courseTitle':course.getCourseTitle()})
        return jsonify(courses=retCourses)

    def addSection(request):
        conn = courseDB.getConnection('database/example.db')
        if (request.is_json):
            data = request.get_json()
            if (('courseId' in data) and (('semester' in data) and ('year' in data))):
                courseId = data['courseId']
                semester = data['semester']
                year = data['year']
                if(isinstance(year, str) and year.isdigit()):
                    year = int(year)
                if ((not isinstance(year, int)) or (year<2010 or year>2050)):
                    return jsonify(error="Invalid year")
                if (len(semester) > 50):
                    return jsonify(error="Maximum 50 characters for semester")
                conn = courseDB.getConnection('database/example.db')
                course = courseDB.getCourse(conn,courseId)
                if(course==None):
                    return jsonify(error="Invalid course")
                sectionId = courseDB.addSection(conn,courseId,year,semester)
                return jsonify(sectionId=sectionId)
        return jsonify(error="Invalid request")

    def getSections(courseId):
        conn = courseDB.getConnection('database/example.db')
        sections = courseDB.getSections(conn,courseId)
        if(sections==None):
            return jsonify(error="sections not found")
        retSections = []
        for section in sections:
            retSections.append({'sectionId': section.getSectionId(), 'courseId': section.getCourseId(),
                               'year': section.getYear(),'semester': section.getSemester()})
        return jsonify(sections=retSections)