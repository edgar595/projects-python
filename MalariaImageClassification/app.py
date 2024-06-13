from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

# Define the folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your trained model
model = "malaria_model.h5"

# Load the model
model = tf.keras.models.load_model(model)

# Function to preprocess the image
def preprocess_image(image_path, target_size):
    img = Image.open(image_path)
    img = img.resize(target_size)
    img = np.array(img) / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to make predictions
def predict_uploaded_image(image_path, target_size):
    img = preprocess_image(image_path, target_size)
    prediction = model.predict(img)
    return prediction[0][0]  


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Perform prediction
            prediction = predict_uploaded_image(file_path, (200, 200))
            # Render the index.html template again with the filename of the uploaded image and prediction
            return render_template('index.html', filename=filename, prediction=prediction)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
