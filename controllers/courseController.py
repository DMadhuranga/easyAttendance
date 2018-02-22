import datetime
from flask import request, jsonify
from classes.Course import Course
from classes.Section import Section
from classes.Attendance import Attendance
from database.courseDB import courseDB
from database.studentDB import studentDB
from classes.Student import Student



def isValidTime(time):
    timeformat = "%H:%M:%S"
    try:
        validtime = datetime.datetime.strptime(time, timeformat)
        return True
    except ValueError:
        return False

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

dbName = 'database/example.db'

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
                conn = courseDB.getConnection(dbName)
                courseId = courseDB.addCourse(conn,courseCode,courseTitle)
                return jsonify(courseId=courseId)
        return jsonify(error="Invalid request")

    def getCourse(courseId):
        conn = courseDB.getConnection(dbName)
        course = courseDB.getCourse(conn,courseId)
        if(course==None):
            return jsonify(error="student not found")
        return jsonify(courseId=course.getCourseId(),courseCode=course.getCourseCode(),courseTitle=course.getCourseTitle())

    def getCourseByCode(courseCode):
        conn = courseDB.getConnection(dbName)
        course = courseDB.getCourseByCode(conn,courseCode)
        if(course==None):
            return jsonify(error="student not found")
        return jsonify(courseId=course.getCourseId(), courseCode=course.getCourseCode(),courseTitle=course.getCourseTitle())

    def getCourses():
        conn = courseDB.getConnection(dbName)
        courses = courseDB.getCourses(conn)
        if(courses==None):
            return jsonify(error="COurse information not available")
        retCourses = []
        for course in courses:
            retCourses.append({'courseId':course.getCourseId(),'courseCode':course.getCourseCode(),'courseTitle':course.getCourseTitle()})
        return jsonify(courses=retCourses)

    def addSection(request):
        conn = courseDB.getConnection(dbName)
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
                conn = courseDB.getConnection(dbName)
                course = courseDB.getCourse(conn,courseId)
                if(course==None):
                    return jsonify(error="Invalid course")
                sectionId = courseDB.addSection(conn,courseId,year,semester)
                return jsonify(sectionId=sectionId)
        return jsonify(error="Invalid request")

    def getSections(courseId):
        conn = courseDB.getConnection(dbName)
        sections = courseDB.getSections(conn,courseId)
        if(sections==None):
            return jsonify(error="sections not found")
        retSections = []
        for section in sections:
            retSections.append({'sectionId': section.getSectionId(), 'courseId': section.getCourseId(),
                               'year': section.getYear(),'semester': section.getSemester(),'courseCode': section.getCourseCode(),'courseTitle': section.getCourseTitle()})
        return jsonify(sections=retSections)

    def getSessions(sessionId):
        conn = courseDB.getConnection(dbName)
        sessions = courseDB.getSessions(conn,sessionId)
        if(sessions==None):
            return jsonify(error="sessions not found")
        retSessions = []
        for session in sessions:
            retSessions.append({'sectionId': session.getSectionId(), 'courseId': session.getCourseId(),
                               'year': session.getYear(),'semester': session.getSemester(),'courseCode': session.getCourseCode(), 'courseTitle': session.getCourseTitle(),
                               'sessionId': session.getSessionId(),'date': session.getDate(),'startingTime':session.getStartingTime(),'marked':session.getMarked()})
        return jsonify(sessions=retSessions)

    def getSection(sectionId):
        conn = courseDB.getConnection(dbName)
        section = courseDB.getSection(conn,sectionId)
        if(section==None):
            return jsonify(error="section not found")
        return jsonify(sectionId= section.getSectionId(), courseId= section.getCourseId(),
                               year= section.getYear(),semester = section.getSemester(),courseCode= section.getCourseCode(),courseTitle=section.getCourseTitle())


    def addSession(request):
        conn = courseDB.getConnection(dbName)
        if (request.is_json):
            data = request.get_json()
            if (('sectionId' in data) and (('date' in data) and ('startingTime' in data))):
                sectionId = data['sectionId']
                date = data['date']
                startingTime = data['startingTime']
                if (not validate(date)):
                    return jsonify(error="Invalid date")
                if (not isValidTime(startingTime)):
                    return jsonify(error="Invalid starting time")
                conn = courseDB.getConnection(dbName)
                section = courseDB.getSection(conn,sectionId)
                if(section==None):
                    return jsonify(error="Invalid section")
                sessionId = courseDB.addSession(conn,sectionId,date,startingTime)
                return jsonify(sessionId=sessionId)
        return jsonify(error="Invalid request")

    def getSession(sessionId):
        conn = courseDB.getConnection(dbName)
        session = courseDB.getSession(conn,sessionId)
        if(session==None):
            return jsonify(error="session not found")
        return jsonify(sectionId= session.getSectionId(), courseId= session.getCourseId(),
                               year= session.getYear(),semester = session.getSemester(),courseCode= session.getCourseCode(),courseTitle=session.getCourseTitle(),
                       date= session.getDate(),startingTime=session.getStartingTime(),marked=session.getMarked())

    def getAllSessions():
        conn = courseDB.getConnection(dbName)
        sessions = courseDB.getAllSessions(conn)
        if(sessions==None):
            return jsonify(error="sessions not found")
        retSessions = []
        for session in sessions:
            retSessions.append({'sectionId': session.getSectionId(), 'courseId': session.getCourseId(),
                               'year': session.getYear(),'semester': session.getSemester(),'courseCode': session.getCourseCode(), 'courseTitle': session.getCourseTitle(),
                               'sessionId': session.getSessionId(),'date': session.getDate(),'startingTime':session.getStartingTime(),'marked':session.getMarked()})
        return jsonify(sessions=retSessions)

    def getAttendance(sessionId):
        conn = courseDB.getConnection(dbName)
        attendances = courseDB.getAttendance(conn,sessionId)
        if(attendances==None):
            return jsonify(error="sessions not found")
        retSessions = []
        for attendance in attendances:
            retSessions.append({'id':attendance.getId(),'studentId':attendance.getStudentId(),'studentName':attendance.getStudentName(),'sessionId':attendance.getSessionId(),'attended':attendance.getAttended()})
        return jsonify(attendances=retSessions)

    def getEnrolledStudents(sectionId):
        conn = courseDB.getConnection(dbName)
        students = courseDB.getSectionStudents(conn,sectionId)
        if(students==None):
            return jsonify(error="Students not found")
        retSessions = []
        for student in students:
            retSessions.append({'id':student.getId(),'studentId':student.getStudentId(),'studentName':student.getStudentName()})
        return jsonify(students=retSessions)

    def getNotEnrolledStudents(sectionId):
        conn = courseDB.getConnection(dbName)
        students = courseDB.getNotSectionStudents(conn,sectionId)
        if(students==None):
            return jsonify(error="Students not found")
        retSessions = []
        for student in students:
            retSessions.append({'id':student.getId(),'studentId':student.getStudentId(),'studentName':student.getStudentName()})
        return jsonify(students=retSessions)

    def markAttendanceToDB(sessionId,ids):
        conn = courseDB.getConnection(dbName)
        courseDB.markAttendanceToDB(conn,sessionId,ids)

    def addStudentToSection(request):
        conn = courseDB.getConnection(dbName)
        if (request.is_json):
            data = request.get_json()
            if (('sectionId' in data) and ('id' in data)):
                sectionId = data['sectionId']
                id = data['id']
                conn = courseDB.getConnection(dbName)
                section = courseDB.getSection(conn,sectionId)
                student = studentDB.getStudent(conn,id)
                if(section==None or student==None):
                    return jsonify(error="Invalid section or student")
                courseDB.enrollStudent(conn,sectionId,id)
                return jsonify(success="Added")
        return jsonify(error="Invalid request")