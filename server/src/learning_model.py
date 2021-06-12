from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.keras.utils import to_categorical

import firebase_admin
from firebase_admin import credentials, db, storage

import tensorflow as tf
import numpy as np
import os, shutil

from google.cloud import storage as gcs
from google.oauth2 import service_account

project_id = os.getenv('PROJECT_ID')
key_path = os.getenv('GOOGLE_CREDENTIALS')
credential = service_account.Credentials.from_service_account_file(key_path)
client = gcs.Client(project_id, credentials=credential)
bucket_name = os.getenv('BUCKET_NAME')
bucket = client.get_bucket(bucket_name)

image_size = 50

def main(file_name, classes):
    # firebaseのステータスを処理中に変更
    results_ref = db.reference('/results/learning/')
    results_ref.child(file_name).update({
        'learningStatus': 'progress'
    })

    X_train, X_test, y_train, y_test = np.load('./src/npy/' + file_name + '.npy', allow_pickle=True)
    X_train = X_train.astype('float') / 256
    X_test = X_test.astype('float') / 256
    y_train = to_categorical(y_train, len(classes))
    y_test = to_categorical(y_test, len(classes))

    model = model_train(file_name, classes, X_train, y_train)
    model_eval(model, X_test, y_test)

    results_ref.child(file_name).update({
        'learningStatus': 'finish'
    })

    os.remove('./src/npy/' + file_name + '.npy')
    os.remove('./src/model/' + file_name + '.h5')

def model_train(file_name, classes, X, y):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(classes)))
    model.add(Activation('softmax'))

    opt = tf.keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)

    model.compile(
        loss='categorical_crossentropy',
        optimizer=opt,
        metrics=['accuracy']
    )

    model.fit(X, y, batch_size=32, epochs=100)
    model.save('./src/model/' + file_name + '.h5')

    # gcsにアップロード
    storage_file_path = 'model/' + file_name + '.h5'
    blob_gcs = bucket.blob(storage_file_path)
    model_file = './src/model/' + file_name + '.h5'
    blob_gcs.upload_from_filename(model_file)

    return model

def model_eval(model, X, y):
    scores = model.evaluate(X, y, verbose=1)
    print('Test Loss: ', scores[0])
    print('Test Accuracy: ', scores[1])

def delete_learning_model(file_name):
    storage_file_path = 'model/' + file_name + '.h5'
    blob_gcs = bucket.blob(storage_file_path)
    blob_gcs.delete()

    storage_file_path = 'npy/' + file_name + '.npy'
    blob_gcs = bucket.blob(storage_file_path)
    blob_gcs.delete()


if __name__ == '__main__':
    main()
