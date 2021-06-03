from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
import sys
import tensorflow as tf
import numpy as np
from PIL import Image

image_size = 50

def build_model(file_name, classes):
    model = Sequential()
    model.add(Conv2D(32,(3,3), padding='same',input_shape=(50,50,3)))
    model.add(Activation('relu'))
    model.add(Conv2D(32,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64,(3,3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    opt = tf.keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)

    model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])

    # モデルのロード
    model = load_model('./src/model/' + file_name + '.h5')

    return model

def main(predict_image_file, file_name, classes):
    image = Image.open(predict_image_file)
    image = image.convert('RGB')
    image = image.resize((image_size, image_size))
    data = np.asarray(image)/255
    X = []
    X.append(data)
    X = np.array(X)
    model = build_model(file_name, classes)

    result = model.predict([X])[0]
    print(result)
    predicted = result.argmax()
    percentage = int(result[predicted] * 100)
    return "{0} ({1} %)".format(classes[predicted], percentage)

if __name__ == "__main__":
    main()
