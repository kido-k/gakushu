from flask import Flask, request
import flickr_download
import create_learning_data
import learning_cnn

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world!!"

@app.route('/get_images')
def get_images():
    search_name = request.args.get('search_name')
    max_get_number = request.args.get('max_get_number')
    flickr_download.get_images(search_name, max_get_number)
    return "OK"

@app.route('/learning')
def learning():
    file_name = 'dog-cat-bird'
    classes = ['dog', 'cat', 'bird']
    create_learning_data.main(file_name, classes)
    learning_cnn.main(file_name, classes)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)