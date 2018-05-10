import datetime
from flask import request, jsonify
from classes.Course import Course
from classes.Section import Section
from classes.Attendance import Attendance
from database.courseDB import courseDB
from database.studentDB import studentDB
from classes.Student import Student
from classes.SessionAttendance import SessionAttendance



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

    # this class handles all the requests related to course details
    # uses both courseDB and studentDB database access classes to access database

    def addCourse(request):
        # add a course to course table given a json with courseCode and courseTitle

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
        # return a json with details of a course with given courseId

        conn = courseDB.getConnection(dbName)
        course = courseDB.getCourse(conn,courseId)
        if(course==None):
            return jsonify(error="student not found")
        return jsonify(courseId=course.getCourseId(),courseCode=course.getCourseCode(),courseTitle=course.getCourseTitle())

    def getCourseByCode(courseCode):
        # return a json with details of a course with given courseCode

        conn = courseDB.getConnection(dbName)
        course = courseDB.getCourseByCode(conn,courseCode)
        if(course==None):
            return jsonify(error="student not found")
        return jsonify(courseId=course.getCourseId(), courseCode=course.getCourseCode(),courseTitle=course.getCourseTitle())

    def getCourses():
        # return a json with details of all courses (list of courses)

        conn = courseDB.getConnection(dbName)
        courses = courseDB.getCourses(conn)
        if(courses==None):
            return jsonify(error="Course information not available")
        retCourses = []
        for course in courses:
            retCourses.append({'courseId':course.getCourseId(),'courseCode':course.getCourseCode(),'courseTitle':course.getCourseTitle()})
        return jsonify(courses=retCourses)

    def addSection(request):
        # add a new section given a json with courseId, semester and year

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
        # return a json with details of all sections (list of sections) of a given course

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
        # return a json with details of all sessions (list of sessions) of a given section

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
        # return a json with the details of a section given the sectionId

        conn = courseDB.getConnection(dbName)
        section = courseDB.getSection(conn,sectionId)
        if(section==None):
            return jsonify(error="section not found")
        return jsonify(sectionId= section.getSectionId(), courseId= section.getCourseId(),
                               year= section.getYear(),semester = section.getSemester(),courseCode= section.getCourseCode(),courseTitle=section.getCourseTitle())


    def addSession(request):
        # add a new session given a json with sectionId, date and startingTime

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
        # get a json with details of a session given the sessionId

        conn = courseDB.getConnection(dbName)
        session = courseDB.getSession(conn,sessionId)
        if(session==None):
            return jsonify(error="session not found")
        return jsonify(sectionId= session.getSectionId(), courseId= session.getCourseId(),
                               year= session.getYear(),semester = session.getSemester(),courseCode= session.getCourseCode(),courseTitle=session.getCourseTitle(),
                       date= session.getDate(),startingTime=session.getStartingTime(),marked=session.getMarked())

    def getAllSessions():
        # get a json with details of all session (list of sessions)

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
        # get a json with attendance details of a session (list of students with their attendance)

        conn = courseDB.getConnection(dbName)
        attendances = courseDB.getAttendance(conn,sessionId)
        if(attendances==None):
            return jsonify(error="sessions not found")
        retSessions = []
        for attendance in attendances:
            retSessions.append({'id':attendance.getId(),'studentId':attendance.getStudentId(),'studentName':attendance.getStudentName(),'sessionId':attendance.getSessionId(),'attended':attendance.getAttended()})
        return jsonify(attendances=retSessions)

    def getEnrolledStudents(sectionId):
        #

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

    def getSectionAttendanceSummary(sectionId):
        conn = courseDB.getConnection(dbName)
        sessions = courseDB.getSectionAttendanceSummary(conn,sectionId)
        if(sessions==None):
            return jsonify(error="Date not found")
        retSessions = []
        for session in sessions.keys():
            students = []
            for student in sessions[session].getStudentAttendance().keys():
                students.append({'id':student,'studentId':sessions[session].getStudentAttendance()[student][0],'studentName':sessions[session].getStudentAttendance()[student][1],'attended':sessions[session].getStudentAttendance()[student][2]})
            retSessions.append({'students':students ,'sessionId':sessions[session].getSessionId(),'date':sessions[session].getDate(),'startingTime':sessions[session].getStartingTime(),'marked':sessions[session].isMarked()})
        return jsonify(sessions=retSessions)

    def getStudentAttendanceSummary(sectionId):
        conn = courseDB.getConnection(dbName)
        sessions = courseDB.getSectionAttendanceSummary(conn,sectionId)
        if(sessions==None):
            return jsonify(error="Date not found")
        students = {}
        for session in sessions.keys():
            for student in sessions[session].getStudentAttendance().keys():
                if student not in students.keys():
                    students[student] = {'presentDays':0,'conductedDays':0,'id':student,'studentId':sessions[session].getStudentAttendance()[student][0],'studentName':sessions[session].getStudentAttendance()[student][1]}
                print(str(student)+" ============ attendance before ========"+str(students[student]['presentDays']))
                print(str(student) + " ============ conduct before ========" + str(students[student]['conductedDays']))
                print(sessions[session].getStudentAttendance()[student])
                students[student]['conductedDays']+=1
                students[student]['presentDays'] += sessions[session].getStudentAttendance()[student][2]
                print(str(student) + " ============ attendance after ========" + str(students[student]['presentDays']))
                print(str(student) + " ============ conduct after ========" + str(students[student]['conductedDays']))
        return jsonify(students=students)

    def getStudentAttendanceSummaryJSON(sectionId):
        conn = courseDB.getConnection(dbName)
        sessions = courseDB.getSectionAttendanceSummary(conn,sectionId)
        if(sessions==None):
            return jsonify(error="Date not found")
        students = {}
        for session in sessions.keys():
            if(sessions[session]["marked"]==1):
                for student in sessions[session]["students"]:
                    if student[0] not in students.keys():
                        students[student[0]] = {'presentDays':0,'conductedDays':0,'id':student[0],'studentId':student[1],'studentName':student[2]}
                    students[student[0]]['conductedDays']+=1
                    students[student[0]]['presentDays'] += student[3]
        return jsonify(students=students)

    def getSessionAttendanceSummaryJSON(sectionId):
        conn = courseDB.getConnection(dbName)
        sessions = courseDB.getSectionAttendanceSummary(conn,sectionId)
        if(sessions==None):
            return jsonify(error="Date not found")
        ret_Session = []
        for session in sessions.keys():
            if (sessions[session]["marked"] == 1):
                numberOfTotalStudents = 0
                numberOfAttendance = 0
                for student in sessions[session]["students"]:
                    numberOfTotalStudents+=1
                    numberOfAttendance += student[3]
                ret_Session.append({"sessionId":session,"date":sessions[session]["date"],"startingTime":sessions[session]["startingTime"],"numberOfAttendance":numberOfAttendance,"numberOfTotalStudents":numberOfTotalStudents})
        return jsonify(sessions=ret_Session)

    def getUnmarkedSessions():
        conn = courseDB.getConnection(dbName)
        sessions = courseDB.getUnmarkedSessions(conn)
        if(sessions==None):
            return jsonify(error="sessions not found")
        retSessions = []
        for session in sessions:
            retSessions.append({'sectionId': session.getSectionId(), 'courseId': session.getCourseId(),
                               'year': session.getYear(),'semester': session.getSemester(),'courseCode': session.getCourseCode(), 'courseTitle': session.getCourseTitle(),
                               'sessionId': session.getSessionId(),'date': session.getDate(),'startingTime':session.getStartingTime(),'marked':session.getMarked()})
        return jsonify(sessions=retSessions)

    def getTodaySummary():
        conn = courseDB.getConnection(dbName)
        summary = courseDB.getTodayAttendanceSummary(conn)
        if(summary==None):
            return jsonify(error="data not found")
        return jsonify(summary=summary)