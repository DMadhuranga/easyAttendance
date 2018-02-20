import face_recognition
import cv2

class FaceRecognition:
    def detect_face(img):
        rgb_frame = img[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        if (len(faces) !=1):
            return None, None
        (x, y, w, h) = faces[0]
        return gray[y:y + w, x:x + h], faces[0]