from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
from flask_cors import CORS  # Import CORS to enable cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Store images in static/uploads

# Load the model
model = tf.keras.models.load_model('best_model1.keras')

# Define your class labels
class_labels = ['Grassy Terrain', 'Marshy Terrain', 'Other', 'Rocky Terrain', 'Sandy Terrain']

@app.route('/')
def home():
    return "Terrain Recognition API is running."

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Get the URL of the uploaded image
    image_url = f"/static/uploads/{file.filename}"

    # Preprocess the image
    img = image.load_img(filepath, target_size=(229, 229))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Predict
    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions)]

    return jsonify({
        'prediction': predicted_class,
        'image_url': image_url  # Return the image URL
    })

if __name__ == '__main__':
    # Ensure that the static/uploads directory exists
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True)
