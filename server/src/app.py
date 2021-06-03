from flask import Flask, request
from flask_cors import CORS, cross_origin
import flickr_download
import create_learning_data
import learning_cnn
import predict

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['POST'])
def hello():
    return "Hello world!!"

@app.route('/get_images', methods=['POST'])
def get_images():
    post_data = request.json
    search_name = post_data['search_name']
    max_get_number = post_data['max_get_number']
    flickr_download.get_images(search_name, max_get_number)
    return "OK"

@app.route('/learning', methods=['POST'])
@cross_origin(supports_credentials=True)
def learning():
    post_data = request.json
    file_name = post_data['file_name']
    classes = post_data['classes']
    create_learning_data.main(file_name, classes)
    learning_cnn.main(file_name, classes)
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