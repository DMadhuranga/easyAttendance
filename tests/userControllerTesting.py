import unittest
import requests
import json

url = "http://localhost:5000"
token = ""

def sendPostRequest(url,payload):
    headers = {'content-type': 'application/json',"Token":token}
    return requests.post(url, data=json.dumps(payload), headers=headers)

def setToken(tokenValue):
    global token
    token = tokenValue

def sendGetRequest(url,payload):
    headers = {'content-type': 'application/json',"Token":token}
    return requests.get(url, payload, headers=headers)

class aLoginTestCase(unittest.TestCase):
    myurl = url+"/login/check"
    request = sendPostRequest(myurl,{"username":"admin","password":"superadmin"})

    def test_afor_response_code(self):
        self.assertEqual(self.request.status_code,200,"Incorrect, connection is set")

    def test_bfor_response_type(self):
        self.assertEqual(self.request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_cwith_valid_login_details(self):
        self.assertEqual("token" in self.request.json(),True,"Incorrect, login details are valid")
        setToken(self.request.json()["token"])

    def test_dwith_invalid_password(self):
        request = sendPostRequest(self.myurl, {"username": "admin", "password": "superain"})
        self.assertEqual(request.json(),0,"Incorrect, login details are invalid")

    def test_ewith_invalid_username(self):
        request = sendPostRequest(self.myurl, {"username": "adm12in", "password": "superain"})
        self.assertEqual(request.json(),0,"Incorrect, login details are invalid")

class getUserTestCase(unittest.TestCase):
    myurl = url+"/user/getUser/"

    def setUp(self):
        self.request = sendGetRequest(self.myurl + "1", "")

    def test_afor_response_code(self):
        self.assertEqual(self.request.status_code,200,"Incorrect, connection is set")

    def test_bfor_response_type(self):
        self.assertEqual(self.request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_cwith_valid_user_id(self):
        self.assertEqual("userName" in self.request.json(),True,"Incorrect, user details are valid")

    def test_dwith_invalid_user_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual("error" in request.json(), True, "Incorrect, user details are invalid")

class usersTestCase(unittest.TestCase):
    myurl = url+"/users"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_users(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("users" in request.json(),True,"Incorrect, output is users")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl, "")
        self.assertIsInstance(request.json()["users"],list)

    def test_e_for_user_json(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("userName" in request.json()["users"][0], True, "Incorrect, response should be json")

class getStudentTestCase(unittest.TestCase):
    myurl = url+"/student/getStudent/"

    def setUp(self):
        self.request = sendGetRequest(self.myurl + "1", "")

    def test_afor_response_code(self):
        self.assertEqual(self.request.status_code,200,"Incorrect, connection is set")

    def test_bfor_response_type(self):
        self.assertEqual(self.request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_cwith_valid_student_id(self):
        self.assertEqual("studentName" in self.request.json(),True,"Incorrect, student id is valid")

    def test_dwith_invalid_student_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual("error" in request.json(), True, "Incorrect, student id is invalid")

class getStudentByStudentIdTestCase(unittest.TestCase):
    myurl = url+"/student/getStudentByStudentId/"

    def setUp(self):
        self.request = sendGetRequest(self.myurl + "a001", "")

    def test_afor_response_code(self):
        self.assertEqual(self.request.status_code,200,"Incorrect, connection is set")

    def test_bfor_response_type(self):
        self.assertEqual(self.request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_cwith_valid_student_id(self):
        self.assertEqual("studentName" in self.request.json(),True,"Incorrect, student id is valid")

    def test_dwith_invalid_student_id(self):
        request = sendGetRequest(self.myurl+"a0c12","")
        self.assertEqual("error" in request.json(), True, "Incorrect, student id is invalid")

class getCourseTestCase(unittest.TestCase):
    myurl = url+"/course/getCourse/"

    def setUp(self):
        self.request = sendGetRequest(self.myurl + "1", "")

    def test_afor_response_code(self):
        self.assertEqual(self.request.status_code,200,"Incorrect, connection is set")

    def test_bfor_response_type(self):
        self.assertEqual(self.request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_cwith_valid_course_id(self):
        self.assertEqual("courseCode" in self.request.json(),True,"Incorrect, course id is valid")

    def test_dwith_invalid_course_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual("error" in request.json(), True, "Incorrect, course id is invalid")

class getStudentsTestCase(unittest.TestCase):
    myurl = url+"/students"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_students(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("students" in request.json(),True,"Incorrect, output is students")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl, "")
        self.assertIsInstance(request.json()["students"],list)

    def test_e_for_student_json(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("studentName" in request.json()["students"][0], True, "Incorrect, response should be json")

class getCoursesTestCase(unittest.TestCase):
    myurl = url+"/courses"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_courses(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("courses" in request.json(),True,"Incorrect, output is courses")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl, "")
        self.assertIsInstance(request.json()["courses"],list)

    def test_e_for_course_json(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("courseCode" in request.json()["courses"][0], True, "Incorrect, response should be json")

class getSectionsOfACourseTestCase(unittest.TestCase):
    myurl = url+"/sections/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_sections(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("sections" in request.json(),True,"Incorrect, output is sections")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertIsInstance(request.json()["sections"],list)

    def test_e_for_course_json(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("semester" in request.json()["sections"][0], True, "Incorrect, response should be json")

    def test_f_with_invalid_course_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual(len(request.json()["sections"]), 0, "Incorrect, course id is invalid")

class getSectionTestCase(unittest.TestCase):
    myurl = url+"/section/getSection/"

    def setUp(self):
        self.request = sendGetRequest(self.myurl + "1", "")

    def test_afor_response_code(self):
        self.assertEqual(self.request.status_code,200,"Incorrect, connection is set")

    def test_bfor_response_type(self):
        self.assertEqual(self.request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_cwith_valid_section_id(self):
        self.assertEqual("semester" in self.request.json(),True,"Incorrect, section id is valid")

    def test_dwith_invalid_section_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual("error" in request.json(), True, "Incorrect, section id is invalid")

class getSessionsOfASectionTestCase(unittest.TestCase):
    myurl = url+"/sessions/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_sessions(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("sessions" in request.json(),True,"Incorrect, output is sections")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertIsInstance(request.json()["sessions"],list)

    def test_e_for_session_json(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("semester" in request.json()["sessions"][0], True, "Incorrect, response should be json")

    def test_f_with_invalid_section_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual(len(request.json()["sessions"]), 0, "Incorrect, section id is invalid")

class getSessionsTestCase(unittest.TestCase):
    myurl = url+"/sessions"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_sessions(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("sessions" in request.json(),True,"Incorrect, output is sessions")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl, "")
        self.assertIsInstance(request.json()["sessions"],list)

    def test_e_for_session_json(self):
        request = sendGetRequest(self.myurl, "")
        self.assertEqual("date" in request.json()["sessions"][0], True, "Incorrect, response should be json")

class getSessionTestCase(unittest.TestCase):
    myurl = url+"/session/getSession/"

    def setUp(self):
        self.request = sendGetRequest(self.myurl + "7", "")

    def test_afor_response_code(self):
        self.assertEqual(self.request.status_code,200,"Incorrect, connection is set")

    def test_bfor_response_type(self):
        self.assertEqual(self.request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_cwith_valid_session_id(self):
        self.assertEqual("date" in self.request.json(),True,"Incorrect, session id is valid")

    def test_dwith_invalid_session_id(self):
        request = sendGetRequest(self.myurl+"3","")
        self.assertEqual("error" in request.json(), True, "Incorrect, session id is invalid")

class getAttendanceOfASessionTestCase(unittest.TestCase):
    myurl = url+"/attendances/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"10", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"10", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_attendances(self):
        request = sendGetRequest(self.myurl+"10", "")
        self.assertEqual("attendances" in request.json(),True,"Incorrect, output is attendances")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"10", "")
        self.assertIsInstance(request.json()["attendances"],list)

    def test_e_for_session_json(self):
        request = sendGetRequest(self.myurl+"10", "")
        self.assertEqual("attended" in request.json()["attendances"][0], True, "Incorrect, response should be json")

    def test_f_with_invalid_session_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual(len(request.json()["attendances"]), 0, "Incorrect, session id is invalid")

class getSectionStudentsTestCase(unittest.TestCase):
    myurl = url+"/enrolledStudents/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_students(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("students" in request.json(),True,"Incorrect, output is students")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertIsInstance(request.json()["students"],list)

    def test_e_for_student_json(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("studentName" in request.json()["students"][0], True, "Incorrect, response should be json")

    def test_f_with_invalid_section_id(self):
        request = sendGetRequest(self.myurl+"0","")
        self.assertEqual(len(request.json()["students"]), 0, "Incorrect, section id is invalid")

class getUnEnrolledStudentsTestCase(unittest.TestCase):
    myurl = url+"/notEnrolledStudents/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_students(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("students" in request.json(),True,"Incorrect, output is students")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertIsInstance(request.json()["students"],list)

    def test_e_for_student_json(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("studentName" in request.json()["students"][0], True, "Incorrect, response should be json")

class getEnrolledSectionsTestCase(unittest.TestCase):
    myurl = url+"/getEnrolledSections/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_sections(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("sections" in request.json(),True,"Incorrect, output is sections")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertIsInstance(request.json()["sections"],list)

    def test_e_for_section_json(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("sectionId" in request.json()["sections"][0], True, "Incorrect, response should be json")

class getSessionAttendanceSummaryTestCase(unittest.TestCase):
    myurl = url+"/section/getSessionAttendanceSummary/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_sessions(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("sessions" in request.json(),True,"Incorrect, output is sessions")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertIsInstance(request.json()["sessions"],list)

    def test_e_for_session_json(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("numberOfAttendance" in request.json()["sessions"][0], True, "Incorrect, response should be json")

class getStudentAttendanceSummaryTestCase(unittest.TestCase):
    myurl = url+"/section/getStudentAttendanceSummary/"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_sessions(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("students" in request.json(),True,"Incorrect, output is sessions")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        students = request.json()["students"]
        self.assertIsInstance(students,dict)

    def test_e_for_session_json(self):
        request = sendGetRequest(self.myurl+"2", "")
        students = request.json()["students"]
        self.assertEqual("presentDays" in students[list(students.keys())[0]], True, "Incorrect, response should be json")

class getUnmarkedSessionsTestCase(unittest.TestCase):
    myurl = url+"/sessions/unmarked"

    def test_a_for_response_code(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_sessions(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertEqual("sessions" in request.json(),True,"Incorrect, output is sessions")

    def test_d_for_list(self):
        request = sendGetRequest(self.myurl+"2", "")
        self.assertIsInstance(request.json()["sessions"],list)

class validPasswordTestCase(unittest.TestCase):
    myurl = url+"/user/validPassword"

    def test_a_for_response_code(self):
        request = sendPostRequest(self.myurl,{"userId":"admin","password":"superadmin"})
        self.assertEqual(request.status_code,200,"Incorrect, connection is set")

    def test_b_for_response_type(self):
        request = sendPostRequest(self.myurl,{"userId":"admin","password":"superadmin"})
        self.assertEqual(request.headers.get('content-type'),"application/json","Incorect, response should be json")

    def test_c_for_valid_user_details(self):
        request = sendPostRequest(self.myurl,{"userId":"1","password":"superadmin"})
        self.assertEqual("success" in request.json(),True,"Incorrect, output is sessions")

    def test_d_for_invalid_password(self):
        request = sendPostRequest(self.myurl, {"userId": "1", "password": "supe12radmin"})
        self.assertEqual("error" in request.json(), True, "Incorrect, response should be json")

    def test_e_for_invalid_userId_and_password(self):
        request = sendPostRequest(self.myurl, {"userId": "0", "password": "super12dmin"})
        self.assertEqual("error" in request.json(), True, "Incorrect, response should be json")