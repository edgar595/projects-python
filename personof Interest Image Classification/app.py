from flask import Flask, request, render_template, jsonify
import cv2
import joblib
import numpy as np
import os
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load the trained model
model = joblib.load('saved_model.pkl')

face_cascade = cv2.CascadeClassifier('model/opencv/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('model/opencv/haarcascade_eye.xml')

import pywt

def w2d(img, mode='haar', level=1):
    imArray = img
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    imArray = np.float32(imArray)
    imArray /= 255
    coeffs = pywt.wavedec2(imArray, mode, level=level)
    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0
    imArray_H = pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H = np.uint8(imArray_H)
    return imArray_H

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None
    (x, y, w, h) = faces[0]
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    if len(eyes) < 2:
        return None
    scalled_raw_img = cv2.resize(roi_color, (32, 32))
    img_har = w2d(roi_color, 'db1', 5)
    scalled_img_har = cv2.resize(img_har, (32, 32))
    combined_img = np.vstack((scalled_raw_img.reshape(32*32*3, 1), scalled_img_har.reshape(32*32, 1)))
    return combined_img.reshape(1, 4096).astype(float)

def image_to_base64(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (200, 200))
    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        input_image_features = preprocess_image(filepath)
        if input_image_features is not None:
            prediction = model.predict(input_image_features)[0]
            class_dict = {0: 'fusco', 1: 'harold', 2: 'john', 3: 'root', 4: 'shaw'}
            predicted_class = class_dict[prediction]
            image_base64 = image_to_base64(filepath)
            id_info = generate_id_info(predicted_class)
            return jsonify({'image_base64': image_base64, 'id_info': id_info})
        return jsonify({'error': 'No face with two eyes detected in the image.'}), 400
    return jsonify({'error': 'File upload failed.'}), 400

def generate_id_info(name):
    id_data = {
        'fusco': {'Name': 'Fusco', 'Occupation': 'NYPD', 'Role': 'Homicide Task force'},
        'harold': {'Name': 'Harold', 'Occupation': 'Admin', 'Role': 'Build Machine'},
        'john': {'Name': 'John', 'Occupation': 'Former CIA', 'Role': 'Homicide Task force'},
        'root': {'Name': 'Root', 'Occupation': 'Hacker', 'Role': 'Machine Handler'},
        'shaw': {'Name': 'Shaw', 'Occupation': 'Control handler', 'Role': 'Nothern Lights'}
    }
    id_info = id_data.get(name, {})
    id_html = f"""
    <div class="id-card">
        <h2>Predicted user</h2>
        <div class="info"><span>Name:</span> {id_info['Name']}</div>
        <div class="info"><span>Occupation:</span> {id_info['Occupation']}</div>
        <div class="info"><span>Role:</span> {id_info['Role']}</div>
    </div>
    """
    return id_html

if __name__ == '__main__':
    app.run(debug=True)
