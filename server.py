from flask import Flask, request, render_template, jsonify, session
import webbrowser
import socket
from database.userDB import userDB
from classes.Tokens import Tokens
from controllers.userController import userController
from controllers.studentController import studentController
from controllers.courseController import courseController

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