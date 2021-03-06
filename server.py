from flask import Flask, request, render_template, jsonify, session,Response
import webbrowser
import socket
import datetime
from database.userDB import userDB
from database.courseDB import courseDB
from classes.Tokens import Tokens
from controllers.userController import userController
from controllers.studentController import studentController
from controllers.courseController import courseController
from controllers.imageController import imageController
from tkinter import *
import cv2

app = Flask(__name__)
tokens = Tokens()
portId = 0
imageProcesing = False

#common_functions
def authenticationFail(request):
    return not tokens.isLogged(request.headers)

def adminAuthenticationFail(request):
    return not tokens.isAdmin(request.headers)

def sessionLogged():
    if(('token' in session) and tokens.isValidToken(session['token'])):
        return True
    return False

def sessionAdmin():
    if(('token' in session) and tokens.isValidAdminToken(session['token'])):
        return True
    return False

def imageProcesingStart():
    imageProcesing = True

def imageProcesingStop():
    imageProcesing = False

def isImageProcessing():
    return imageProcesing

#page_requests

@app.route('/')
def index():
    if(sessionLogged()):
        return render_template("home.html",user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/home')
def getHomePage():
    if (sessionLogged()):
        return render_template("home.html",user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/profile')
def getProfilePage():
    if (sessionLogged()):
        return render_template("profile.html",user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/logout')
def logout():
    if('token' in session):
        tokens.removeToken(int(session['token']))
        session.pop(session['token'],None)
    return render_template("index.html")

@app.route('/page_addStudent')
def getAddStudentPage():
    if (sessionLogged() and sessionAdmin()):
        return render_template("addStudent.html", user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_addCourse')
def getAddCoursePage():
    if (sessionLogged() and sessionAdmin()):
        return render_template("addCourse.html", user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewStudent')
def getViewStudentPage():
    id = request.args.get('id')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("viewStudent.html",id=id, user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewCourse')
def getViewCoursePage():
    id = request.args.get('courseId')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("viewCourse.html",courseId=id, user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_students')
def getStudentsPage():
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("students.html",user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_courses')
def getCoursesPage():
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("courses.html",user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_addSection')
def getAddSectionPage():
    id = request.args.get('courseId')
    if ((sessionLogged() and id) and sessionAdmin()):
        course = courseDB.getCourse(courseDB.getConnection('database/example.db'),id)
        if(course!=None):
            return render_template("addSection.html",user=tokens.getUserDetails(session['token']),course={'courseId':course.getCourseId(),'courseCode':course.getCourseCode(),'courseTitle':course.getCourseTitle()})
        return render_template("sections.html", user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("sections.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewSection')
def getViewSectionPage():
    id = request.args.get('sectionId')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("viewSection.html",sectionId=id, user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_addSession')
def getAddSessionPage():
    id = request.args.get('sectionId')
    if ((sessionLogged() and id) and sessionAdmin()):
        section = courseDB.getSection(courseDB.getConnection('database/example.db'),id)
        if(section!=None):
            return render_template("addSession.html",user=tokens.getUserDetails(session['token']),section={'sectionId':section.getSectionId(),'courseId':section.getCourseId(),'courseCode':section.getCourseCode(),'courseTitle':section.getCourseTitle(),'year':section.getYear(),'semester':section.getSemester()})
        return render_template("sessions.html", user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("sessions.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewSession')
def getViewSessionPage():
    id = request.args.get('sessionId')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("viewSession.html",sessionId=id, user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_sessions')
def getSessionsPage():
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("sessions.html",user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_testCam')
def testPage():
    if (sessionLogged() and sessionAdmin()):
        return render_template("testCam.html", user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_enrollStudent')
def getEnrollPage():
    id = request.args.get('sectionId')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("enrollStudents.html", sectionId=id, user=tokens.getUserDetails(session['token']))
    elif (sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewStudentAttendanceSummary')
def pageViewStudentAttendanceSummary():
    id = request.args.get('sectionId')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("viewStudentAttendance.html", sectionId=id, user=tokens.getUserDetails(session['token']))
    elif (sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewSessionAttendanceSummary')
def pageViewSessionAttendanceSummary():
    id = request.args.get('sectionId')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("viewSessionAttendance.html", sectionId=id, user=tokens.getUserDetails(session['token']))
    elif (sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_addUser')
def getAddUserPage():
    if (sessionLogged() and sessionAdmin()):
        return render_template("addUser.html", user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_users')
def getUsersPage():
    if (sessionLogged() and sessionAdmin()):
        return render_template("users.html", user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewUser')
def getViewUserPage():
    id = request.args.get('userId')
    if ((sessionLogged() and id) and sessionAdmin()):
        return render_template("viewUser.html",id=id, user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_attendance')
def getMarkAttendancePage():
    if (sessionLogged()):
        return render_template("markAttendance.html",user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")

@app.route('/page_viewRestrictedSession')
def getViewRestSessionPage():
    id = request.args.get('sessionId')
    if (sessionLogged() and id):
        return render_template("viewRestrictedSession.html",sessionId=id, user=tokens.getUserDetails(session['token']))
    elif(sessionLogged()):
        return render_template("home.html", user=tokens.getUserDetails(session['token']))
    return render_template("index.html")


#other_requests_____________________________________________________________________________________________________

@app.route('/login/check', methods=["POST"])
def checkLogin():
    if(request.is_json):
        data = request.get_json()
        if(('username' in data) and ('password' in data)):
            username = data['username']
            password = data['password']
            conn = userDB.getConnection('database/example.db')
            login = userDB.checkLogin(conn,username,password)
            if(login==None):
                return "-1"
            elif(login==False):
                return "0"
            token = str(tokens.addToken(login))
            session['token'] = token
            print(username+" logged, token : "+str(token))
            return jsonify(token=token)
    return "-2"

@app.route('/user/addStaff',methods=["POST"])
def createStaff():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return userController.addStaff(request)

@app.route('/user/getUser/<id>')
def getUser(id):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return userController.getUser(id)

@app.route('/user/getMe')
def getMe():
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return

@app.route('/user/addUser',methods=["POST"])
def addUser():
    if (authenticationFail(request)  or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return userController.addUser(request)

@app.route('/users')
def getAllUsers():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return userController.getAllUsers()

@app.route('/student/addStudent',methods=["POST"])
def addStudent():
    if (authenticationFail(request)  or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return studentController.addStudent(request)

@app.route('/student/getStudent/<id>')
def getStudent(id):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return studentController.getStudent(id)

@app.route('/student/getStudentByStudentId/<studentId>')
def getStudentById(studentId):
    if (authenticationFail(request)  or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return studentController.getStudentByStudentId(studentId)

@app.route('/course/addCourse',methods=["POST"])
def addCourse():
    if (authenticationFail(request)  or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.addCourse(request)

@app.route('/course/getCourse/<id>')
def getCourse(id):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getCourse(id)

@app.route('/students')
def getStudents():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return studentController.getStudents()

@app.route('/courses')
def getCourses():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getCourses()

@app.route('/sections/<courseId>')
def getSections(courseId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getSections(courseId)

@app.route('/section/addSection',methods=['POST'])
def addSections():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.addSection(request)

@app.route('/section/getSection/<sectionId>')
def getSection(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getSection(sectionId)

@app.route('/sessions/<sectionId>')
def getSessions(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getSessions(sectionId)

@app.route('/sessions')
def getAllSessions():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getAllSessions()

@app.route('/session/addSession',methods=['POST'])
def addSession():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.addSession(request)

@app.route('/session/getSession/<sessionId>')
def getSesseion(sessionId):
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getSession(sessionId)

@app.route('/attendances/<sessionId>')
def getAttendance(sessionId):
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getAttendance(sessionId)

@app.route('/images/<studentId>',methods=['post'])
def takeMyPic(studentId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    if isImageProcessing():
        return jsonify(error="Image processing going on. Please try again later.")
    imageProcesingStart()
    returnObject = imageController.saveImage(studentId)
    imageProcesingStop()
    return returnObject

@app.route('/images/remove/<studentId>')
def removeMyPic(studentId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    if isImageProcessing():
        return jsonify(error="Image processing going on. Please try again later.")
    imageProcesingStart()
    returnObject = studentController.removeStudentImages(studentId)
    imageProcesingStop()
    return returnObject

@app.route('/sectionStudents/<sectionId>')
def getSectionStudents(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getEnrolledStudents(sectionId)

@app.route('/enrolledStudents/<sectionId>')
def getenrolledStudents(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getEnrolledStudents(sectionId)

@app.route('/notEnrolledStudents/<sectionId>')
def getNotEnrolledStudents(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getNotEnrolledStudents(sectionId)

@app.route('/section/enrollStudent',methods=['POST'])
def addStudentToSection():
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.addStudentToSection(request)

@app.route('/markAttendances/<sessionId>')
def markStudentAttendance(sessionId):
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    if isImageProcessing():
        return jsonify(error="Image processing going on. Please try again later.")
    imageProcesingStart()
    returnObject = imageController.markAttendance(sessionId)
    imageProcesingStop()
    return returnObject

@app.route('/getEnrolledSections/<id>')
def getEnrolledSection(id):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return studentController.getEnrolledSections(id)

@app.route('/getSectionAttendance/<sectionId>')
def getSectionAttendance(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getSectionAttendanceSummary(sectionId)

@app.route('/section/getStudentAttendanceSummary/<sectionId>')
def getSectionStudentAttendance(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getStudentAttendanceSummaryJSON(sectionId)

@app.route('/section/getSessionAttendanceSummary/<sectionId>')
def getSectionSessionAttendance(sectionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getSessionAttendanceSummaryJSON(sectionId)

@app.route('/markAttendancesRealTime/<sessionId>',methods=['POST'])
def markStudentAttendanceRealTime(sessionId):
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    if isImageProcessing():
        return jsonify(error="Image processing going on. Please try again later.")
    imageProcesingStart()
    returnObject = imageController.markAttendanceRealTime(request,sessionId)
    imageProcesingStop()
    return returnObject

@app.route('/markAttendancesAfterSaving/<sessionId>',methods=['POST'])
def markAttendancesAfterSaving(sessionId):
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    if isImageProcessing():
        return jsonify(error="Image processing going on. Please try again later.")
    imageProcesingStart()
    returnObject = imageController.markAttendanceAfterSaving(request,sessionId)
    imageProcesingStop()
    return returnObject

@app.route('/user/validPassword',methods=["POST"])
def checkPasswordValidity():
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return userController.checkValidPassword(request)

@app.route('/user/changePassword',methods=["POST"])
def changePasswordValidity():
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return userController.changePassword(request)

@app.route('/sessions/unmarked')
def getUnmarkedSessions():
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getUnmarkedSessions()

@app.route('/clean')
def cleanServer():
    tokens.cleanTokens()
    return jsonify(success="cleared")

@app.route('/home/getTodayCharts')
def getTodayAttendanceSummary():
    if (authenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getTodaySummary()

@app.route('/video')
def getTestPage():
    return render_template("testCam.html")

def gen():
    cap = cv2.VideoCapture(0)
    valid, frame = cap.read()
    while(valid):
        valid, frame = cap.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

#run_server__________________________________________________________________________________________________________

def runserver(port):
    window = Tk()
    window.title("Welcome to LikeGeeks app")
    window.geometry('350x200')
    lbl = Label(window, text="Hello")
    lbl.grid(column=0, row=0)
    def clicked():
        app.secret_key = "123"
        app.run(port=port)
        #webbrowser.open("http://localhost:" + str(portId), new=0, autoraise=True)
    btn = Button(window, text="Click Me", command=clicked)
    btn.grid(column=1, row=0)
    window.mainloop()

#runserver(5000)

if __name__ == '__main__':
    app.secret_key = "123"
    """sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    portId = port
    sock.close()
    portId = port"""
    port  = 5000
    webbrowser.open("http://localhost:" + str(port), new=0, autoraise=True)
    app.run(port=port)