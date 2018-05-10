import cv2
from classes.Recognizer import Recognizer
from classes.FaceRecognition import FaceRecognizer
from controllers.studentController import studentController
from controllers.courseController import courseController
from flask import request, jsonify
import time
from os import listdir
from os.path import isfile, join


def getFrameRate(cap):
    # this methods calculate frame rate of a video feed

    num_frames = 120
    start = time.time()
    for i in range(0, num_frames):
        ret, frame = cap.read()
    end = time.time()
    seconds = end-start
    return num_frames/seconds

dbName = 'database/example.db'

class imageController:

    # this class handles all the requests related to image processing

    """def saveImage(id):
        count = 0
        cap = cv2.VideoCapture(0)
        getFrameRate(cap)
        while(count<20 and cap.isOpened()):
            ret, frame = cap.read()
            if (ret):
                image, size = FaceRecognizer.detect_face(frame)
                if not image is None:
                    name = studentController.saveStudentImage(id)
                    cv2.imwrite("images/"+name, image)
                    count += 1
                cv2.imshow('image', frame)
                cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()
        return jsonify(success="Done")"""

    """def saveImage(id):
            mypath = "TestImages"
            onlyfiles = ["TestImages/" + f for f in listdir(mypath) if isfile(join(mypath, f))]
            count = 0
            while(count<5 and len(onlyfiles)>0):
                ret = True
                frame = cv2.imread(onlyfiles.pop())
                if (ret):
                    image, size = FaceRecognizer.detect_face(frame)
                    if not image is None:
                        name = studentController.saveStudentImage(id)
                        cv2.imwrite("images/"+name, image)
                        count += 1
                    cv2.imshow('image', frame)
                    cv2.waitKey(1)
            cv2.destroyAllWindows()
            return jsonify(success="Done")"""

    def saveImage(id):
        # this methods captures images of a student and save his face in the database

        count = 0
        cap = cv2.VideoCapture(0)
        while(count<3 and cap.isOpened()):
            ret, frame = cap.read()
            if (ret):
                image, size = FaceRecognizer.detect_face(frame)
                if not image is None:
                    name = studentController.saveStudentImage(id)
                    cv2.imwrite("images/"+name, image)
                    count += 1
                cv2.imshow('image', frame)
                cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()
        return jsonify(success="Done")

    def saveVideo(sessionId,length):
        # test methods not relevant

        noOfFrama = 0
        cap = cv2.VideoCapture(0)
        fps = getFrameRate(cap)
        totalFrame = length*fps
        print(totalFrame)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter("videos/"+str(sessionId)+'.avi', fourcc, fps, (frame_width, frame_height))
        while(noOfFrama<totalFrame and cap.isOpened()):
            ret, frame = cap.read()
            if (ret):
                frame = cv2.flip(frame,1)
                noOfFrama += 1
                out.write(frame)
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()
        #return jsonify(success="Done")

    """def markAttendance(sessionId):
        photoset = studentController.getStudentPictures(sessionId)
        print(photoset)
        cap = cv2.VideoCapture("videos/"+str(sessionId)+".avi")
        recognizer = Recognizer()
        recognizer.trainRecognizer(photoset)
        valid = True
        while(valid):
            valid,frame = cap.read()
            if valid:
                print(recognizer.predic(frame))"""

    def markAttendance(sessionId):
        # test methods not relevant

            photoset = studentController.getStudentPictures(sessionId)
            if(len(photoset.values())==0):
                return jsonify(error="Invalid request")
            cap = cv2.VideoCapture("videos/"+str(sessionId)+".avi")
            recognizer = FaceRecognizer()
            print("Start training")
            recognizer.prepare_training_data(photoset)
            print("Finish training")
            valid = True
            process = True
            allNames = []
            while(valid):
                valid,frame = cap.read()
                if valid and process:
                    names, img = recognizer.predic(frame)
                    if not names is None:
                        allNames = allNames+names
                    cv2.imshow('Video', img)
                    cv2.waitKey(1)
                process = not process
            if(len(allNames)>0):
                courseController.markAttendanceToDB(sessionId,list(set(allNames)))
            cv2.destroyAllWindows()
            return jsonify(success="Student Attendance Marked")

    def markAttendanceRealTime(request,sessionId):
        # captures video and mark attendance realtime

        if (request.is_json):
            data = request.get_json()
            if 'recordingTime' in data:
                recordingTime = data['recordingTime']
                if isinstance(recordingTime,int) and recordingTime>0:
                    photoset = studentController.getStudentPictures(sessionId)
                    if(len(photoset.values())==0):
                        return jsonify(error="Invalid request")
                    cap = cv2.VideoCapture(0)
                    fps = getFrameRate(cap)
                    frame_width = int(cap.get(3))
                    frame_height = int(cap.get(4))
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter("videos/" + str(sessionId) + '.avi', fourcc, fps, (frame_width, frame_height))
                    recognizer = FaceRecognizer()
                    print("Start Loading")
                    recognizer.prepare_training_data(photoset)
                    print("Finish Loading")
                    valid = True
                    process = 0
                    allNames = []
                    startTime = time.time()
                    while(valid and (time.time()-startTime)<recordingTime):
                        valid,frame = cap.read()
                        if valid and process%5==0:
                            names, img = recognizer.predic(frame)
                            if not names is None:
                                allNames = allNames+names
                            out.write(frame)
                            cv2.imshow('Video', img)
                            cv2.waitKey(1)
                        process += 1
                    if(len(allNames)>0):
                        courseController.markAttendanceToDB(sessionId,list(set(allNames)))
                    cv2.destroyAllWindows()
                    return jsonify(success="Student Attendance Marked")
        return jsonify(error="Invalid request")

    def markAttendanceAfterSaving(request,sessionId):
        # first save the video then mark attendance

        if (request.is_json):
            data = request.get_json()
            if 'recordingTime' in data:
                recordingTime = data['recordingTime']
                if isinstance(recordingTime,int) and recordingTime>0:
                    photoset = studentController.getStudentPictures(sessionId)
                    if(len(photoset.values())==0):
                        return jsonify(error="Invalid request")
                    cap = cv2.VideoCapture(0)
                    fps = getFrameRate(cap)
                    frame_width = int(cap.get(3))
                    frame_height = int(cap.get(4))
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter("videos/" + str(sessionId) + '.avi', fourcc, fps, (frame_width, frame_height))
                    startTime = time.time()
                    valid = True
                    while (valid and (time.time() - startTime) < recordingTime):
                        valid, frame = cap.read()
                        cv2.imshow('Video', frame)
                        cv2.waitKey(1)
                        out.write(frame)
                    cap.release()
                    cv2.destroyAllWindows()
                    cap = cv2.VideoCapture("videos/"+str(sessionId)+".avi")
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter("videos/" + str(sessionId) + '_processed.avi', fourcc, fps, (frame_width, frame_height))
                    recognizer = FaceRecognizer()
                    print("Start Loading")
                    recognizer.prepare_training_data(photoset)
                    print("Finish Loading")
                    process = 0
                    allNames = []
                    valid = True
                    while(valid):
                        valid,frame = cap.read()
                        if valid and process%3==0:
                            names, img = recognizer.predic(frame)
                            if not names is None:
                                allNames = allNames+names
                            out.write(frame)
                            cv2.imshow('Video', img)
                            cv2.waitKey(1)
                        process += 1
                    if(len(allNames)>0):
                        courseController.markAttendanceToDB(sessionId,list(set(allNames)))
                    cv2.destroyAllWindows()
                    return jsonify(success="Student Attendance Marked")
        return jsonify(error="Invalid request")