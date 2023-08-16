import numpy as np
import os
import face_recognition as fr
from keras.models import load_model
from django.db import models


model_age = load_model('face_detector/model/agegender.h5')
model_emotion = load_model('face_detector/model/emotion.h5')


def get_age(distr):
    if distr >= 1 and distr <= 10:
        return "9-18"
    if distr >= 11 and distr <= 30:
        return "19-25"
    if distr >= 31 and distr <= 35:
        return "26-37"
    if distr >= 36 and distr <= 40:
        return "38-49"
    if distr >= 60:
        return "60 +"
    return 'Unknown'
    # age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
    #             '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

    # maxindex = int(np.argmax(distr))
    # return age_list[maxindex]


def get_gender(prob):
    if prob > 0.5:
        return "Male"
    else:
        return "Female"


def get_emotion(hrr):
    emotion_dict = {0: "Angry", 1: "Happy", 2: "Disgust",
                    3: "Surprise", 4: "Sad", 5: "Fear", 6: "Neutral"
                    }

    maxindex = int(np.argmax(hrr))
    return emotion_dict[maxindex]


def known_names():
    known_face_names = []
    for face in os.listdir('images'):

        file_name = face
        base_name = os.path.splitext(file_name)[0]

        known_face_names.append(base_name.capitalize())

    return known_face_names


def known_encodings():
    known_face_encodings = []
    for face in os.listdir('images'):
        face_image = fr.load_image_file(f'images/{face}')
        face_encode = fr.face_encodings(face_image)[0]

        known_face_encodings.append(face_encode)

    return known_face_encodings


def face_locations(frame):
    face_locations = []
    face_location = fr.face_locations(frame)
    face_locations.append(face_location)

    return face_locations


def encode_detected_face(frame):
    face_encodings = []

    face_location = fr.face_locations(frame)
    face_encoding = fr.face_encodings(frame, face_location)

    face_encodings.append(face_encoding)

    return face_encodings


def compare_encoded_faces(known_encoded, detected_encoded, known_names):
    recognized_names = []
    for encoding in detected_encoded:
        matches = fr.compare_faces(known_encoded, encoding)
        face_distance = fr.face_distance(known_encoded, encoding)
        name = 'Unknown'

        best_match = np.argmin(face_distance)
        if matches[best_match]:
            name = known_names[best_match]

        recognized_names.append(name)

    return recognized_names


class FaceData(models.Model):
    top = models.IntegerField()
    right = models.IntegerField()
    bottom = models.IntegerField()
    left = models.IntegerField()
    emotion = models.CharField(max_length=50)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
