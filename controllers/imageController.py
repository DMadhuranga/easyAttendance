import cv2
from classes.Recognizer import Recognizer
from controllers.studentController import studentController
from flask import request, jsonify
import time


def getFrameRate(cap):
    num_frames = 120
    start = time.time()
    for i in range(0, num_frames):
        ret, frame = cap.read()
    end = time.time()
    seconds = end-start
    return num_frames/seconds

class imageController:


    def saveImage(id):
        count = 0
        cap = cv2.VideoCapture(0)
        getFrameRate(cap)
        while(count<20 and cap.isOpened()):
            ret, frame = cap.read()
            if (ret):
                image, size = Recognizer.detect_face(frame)
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

    def markAttendance(sessionId):
        photoset = studentController.getStudentPictures(sessionId)
        print(photoset)
        cap = cv2.VideoCapture("videos/"+str(sessionId)+".avi")
        recognizer = Recognizer()
        recognizer.trainRecognizer(photoset)
        valid = True
        while(valid):
            valid,frame = cap.read()
            if valid:
                print(recognizer.predic(frame))