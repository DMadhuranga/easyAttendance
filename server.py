from flask import Flask, request, render_template, jsonify, session
import webbrowser
import socket
from database.userDB import userDB
from database.courseDB import courseDB
from classes.Tokens import Tokens
from controllers.userController import userController
from controllers.studentController import studentController
from controllers.courseController import courseController
from controllers.imageController import imageController

app = Flask(__name__)
tokens = Tokens()
portId = 0

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
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getSession(sessionId)

@app.route('/attendances/<sessionId>')
def getAttendance(sessionId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return courseController.getAttendance(sessionId)

@app.route('/images/<studentId>',methods=['post'])
def takeMyPic(studentId):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return imageController.saveImage(studentId)

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
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return imageController.markAttendance(sessionId)

@app.route('/getEnrolledSections/<id>')
def getEnrolledSection(id):
    if (authenticationFail(request) or adminAuthenticationFail(request)):
        return jsonify(error="Invalid request or user")
    return studentController.getEnrolledSections(id)

#run_server__________________________________________________________________________________________________________

if __name__ == '__main__':
    app.secret_key = "123"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    portId = port
    webbrowser.open("http://localhost:" + str(port), new=0, autoraise=True)
    app.run(port=port)