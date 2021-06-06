from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.applications.vgg16 import preprocess_input
from tensorflow.python.keras.applications.vgg16 import decode_predictions
from tensorflow.python.keras.preprocessing.image import img_to_array
from tensorflow.python.keras.preprocessing.image import load_img

import firebase_admin
from firebase_admin import credentials, db, storage

import urllib.request
import io, json, base64
import numpy as np
from PIL import Image

image_size = 224
my_round_int = lambda x: int((x * 200 + 1) // 2)

def main(predict_image_file, model_name):
    image_data = urllib.request.urlopen(predict_image_file).read()

    filename = './src/sample/temp.jpg'
    with open(filename, 'wb') as f:
            f.write(image_data)
    
    img_dog = load_img(filename, target_size=(224, 224))
    arr_dog = img_to_array(img_dog)
    arr_dog = preprocess_input(arr_dog)
    arr_input = np.stack([arr_dog])

    model = VGG16()
    probs = model.predict(arr_input)

    predictions = decode_predictions(probs)
    prediction = predictions[0]
    result = None
    detail = {}
    for i, predict in enumerate(prediction):
        print('my_round_int(predict[2])')
        print(predict[2])
        print(my_round_int(predict[2]))
        if i == 0: 
            result = "{0} ({1} %)".format(predict[1], my_round_int(predict[2]))
        if i >= 9: break
        detail[predict[1]] = my_round_int(predict[2])
    results_ref = db.reference('/results/learning/' + model_name + '/')
    results_ref.child('predict').update({
        'imageUrl': predict_image_file,
        'result': result,
        'predictDetail': detail
    })
    print('result', result)
    return  result

if __name__ == "__main__":
    main()
