from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection

IMAGE_SIZE = 50

def main(category, classes):
    X = []
    Y = []
    for index, classlabel in enumerate(classes):
        photos_dir = './src/images/' + classlabel 
        files = glob.glob(photos_dir + "/*.jpg")
        for i, file in enumerate(files):
            if i >= 200: break
            image = Image.open(file)
            image = image.convert('RGB')
            image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
            data = np.asarray(image)
            X.append(data)
            Y.append(index)

    X = np.array(X)
    Y = np.array(Y)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
    xy = (X_train, X_test, y_train, y_test )
    np.save('./src/npy/' + category + '.npy', xy)


