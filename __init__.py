import keras.models
import tensorflow
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import utils
import glob

from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        processed_image = utils.process_image(path)
        classifier = tensorflow.keras.models.load_model("model.h5")

        prediction_vals = classifier.predict(processed_image)[0]
        rounded_values = []

        for val in prediction_vals:
            rounded_values.append(round(val * 10000)/100)

        emotion_names = ['anger', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
        print(utils.to_json(emotion_names, rounded_values))
        strona = render_template('index.html', filename=filename, anger=rounded_values[0], disgust=rounded_values[1],
        fear=rounded_values[2], happiness=rounded_values[3], neutral=rounded_values[4], sadness=rounded_values[5], surprise=rounded_values[6])
        return strona
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()
