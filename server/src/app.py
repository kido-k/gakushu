from flask import Flask, request
from flask_cors import CORS, cross_origin
import os

import firebase_admin
from firebase_admin import credentials, db, storage

import training_data
import learning_numpy_data
import learning_model
import predict

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

# firebaseの初期設定
credential = credentials.Certificate("./src/firebase-adminsdk.json")
firebase_database_url = os.getenv('FIREBASE_DATABASE_URL')
firebase_bucket = os.getenv('FIREBASE_BUCKET')
firebase_admin.initialize_app(credential, {
    'databaseURL': firebase_database_url,
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    },
    'storageBucket': firebase_bucket
})

@app.route('/', methods=['POST'])
def hello():
    return "Hello world!!"

@app.route('/get_images', methods=['POST'])
def get_images():
    post_data = request.json
    search_name = post_data['search_name']
    max_get_number = post_data['max_get_number']
    training_data.get_images(search_name, max_get_number)
    return "OK"

@app.route('/delete_images', methods=['POST'])
def delete_images():
    post_data = request.json
    image_name = post_data['image_name']
    training_data.delete_images(image_name)
    return "OK"

@app.route('/create_learning_model', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_learning_model():
    post_data = request.json
    file_name = post_data['file_name']
    classes = post_data['classes']
    learning_numpy_data.create_npy_data(file_name, classes)
    learning_model.main(file_name, classes)
    return "OK"

@app.route('/delete_learning_model', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_learning_model():
    post_data = request.json
    model_name = post_data['model_name']
    learning_numpy_data.delete_npy_data(model_name)
    learning_model.delete_learning_model(model_name)
    return "OK"

@app.route('/predict', methods=['POST'])
def predict_image():
    post_data = request.json
    predict_image_file = post_data['predict_image_file']
    model_name = post_data['model_name']
    classes = post_data['classes']
    result = predict.main(predict_image_file, model_name, classes)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)