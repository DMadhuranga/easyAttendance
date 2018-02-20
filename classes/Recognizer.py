import numpy as np
import cv2
import time


def detect_facePublic(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if (len(faces) != 1):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y + w, x:x + h], faces[0]

class Recognizer:

    faceRecognizer = ""

    def detect_face(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        if (len(faces) !=1):
            return None, None
        (x, y, w, h) = faces[0]
        return img[y:y + w, x:x + h], faces[0]

    def detect_face1(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        if (len(faces) !=1):
            return None, None
        (x, y, w, h) = faces[0]
        return gray[y:y + w, x:x + h], faces[0]

    def prepare_training_data(self,imageSet):
        faces = []
        labels = []
        for studentID in imageSet.keys():
            for image_name in imageSet[studentID]:
                image_path = "images/" + image_name
                image = cv2.imread(image_path)
                face, rect = detect_facePublic(image)
                if face is not None:
                    faces.append(face)
                    labels.append(studentID)
        return faces, labels

    def trainRecognizer(self,imageSet):
        self.faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
        faces, labels = self.prepare_training_data(imageSet)
        self.faceRecognizer.train(faces, np.array(labels))

    def predic(self,testImage):
        img = testImage.copy()
        face, rect = detect_facePublic(img)
        if face is not None:
            label = self.faceRecognizer.predict(face)
            return label
        return None