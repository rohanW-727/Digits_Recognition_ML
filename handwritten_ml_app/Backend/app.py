from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Absolute path to the model file on your desktop
model_path = '/Users/rohanwadhwa/Desktop/mnist_model.keras'

#Load Tensorflow model
model = tf.keras.models.load_model(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image = np.array(data['image'], dtype=np.float32)
    image = image.reshape((1, 28, 28, 1)) / 255.0  # Reshape and normalize
    prediction = model.predict(image)
    predicted_digit = np.argmax(prediction)
    return jsonify({'digit': int(predicted_digit)})
    



if __name__ == "__main__":
    app.run(port=5000)