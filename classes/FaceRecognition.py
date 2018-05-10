import face_recognition
import cv2

import numpy as np
import cv2
import time


def detect_facePublic(img):
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    if (len(face_locations) != 1):
        return None, None
    (top, right, bottom, left) = face_locations[0]
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4
    return img[top:bottom, left:right], face_locations[0]

class FaceRecognizer:

    # this class is an adapter class
    # connects the system and face_recognition library

    known_faces = []
    face_names = []

    def detect_face(img):
        # detects faces in a given image

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if (len(face_locations) != 1):
            return None, None
        (top, right, bottom, left) = face_locations[0]
        top*=4
        right *= 4
        bottom *= 4
        left *= 4
        return img[top:bottom, left:right], face_locations[0]

    def detect_face1(img):
        # test method

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        if (len(faces) !=1):
            return None, None
        (x, y, w, h) = faces[0]
        return gray[y:y + w, x:x + h], faces[0]

    def prepare_training_data(self,imageSet):
        # prepare data need to fetch for the trainer (two lists. one with face encodings another with identifiers)

        cnt = 0
        for studentID in imageSet.keys():
            for image_name in imageSet[studentID]:
                image_path = "images/" + image_name
                try:
                    temp_rec = face_recognition.face_encodings(face_recognition.load_image_file(image_path))
                    if len(temp_rec) > 0:
                        self.known_faces.append(temp_rec[0])
                        self.face_names.append(studentID)
                except Exception:
                    pass

    def predic(self,img):
        # find whether a known student is in the given image, if exist return set of identifiers of the students

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        if (len(face_locations) != 1):
            return None, img
        names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_faces, face_encoding, tolerance=0.45)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.face_names[first_match_index]
                names.append(name)
                print(name)
        for (top, right, bottom, left), name in zip(face_locations, names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return list(set(names)),img