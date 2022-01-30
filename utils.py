import cv2
import os
import flask
import numpy


def process_image(file_path):
    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        cropped_image = gray_image[y:y + h, x:x + w]
    else:
        cropped_image = gray_image
    final_image = cv2.resize(cropped_image, [48, 48])
    final_image = numpy.expand_dims(final_image, axis=0)
    return final_image


def save_file(app, file):
    filename = file.filename
    upload_folder = app.config['UPLOAD_FOLDER']

    if not os.path.isdir(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path


def to_json(emotion_names, prediction_vals):
    out = ""
    for i in range(7):
        out += '"' + emotion_names[i] + '": ' + str(prediction_vals[i])
        if (i != 6):
            out += ", "
    return "{" + out + "}"

