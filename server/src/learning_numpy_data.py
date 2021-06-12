from PIL import Image
import os, glob, shutil
import numpy as np
from sklearn import model_selection

IMAGE_SIZE = 50
save_dir = './src/images/'

def create_npy_data(gcp, file_name, classes):
    download_image_data(gcp, classes)

    X = []
    Y = []
    for index, classlabel in enumerate(classes):
        photos_dir = save_dir + classlabel 
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

    # gcsにアップロード    
    npy_file = './src/npy/' + file_name + '.npy'
    np.save(npy_file, xy)
    storage_file_path = 'npy/' + file_name + '.npy'
    blob_gcs = gcp['bucket'].blob(storage_file_path)
    blob_gcs.upload_from_filename(npy_file)

    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
        os.mkdir(save_dir)

def download_image_data(gcp, classes):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    for index, classlabel in enumerate(classes):
        prefix = 'images/' + classlabel + '/'
        for gcs_file in gcp['client'].list_blobs(gcp['bucket_name'], prefix=prefix):
            if not os.path.exists(save_dir + classlabel):
                os.mkdir(save_dir + classlabel)
            blob = gcp['bucket'].blob(gcs_file.name)
            local_file = save_dir + classlabel + '/' + gcs_file.name.split('/')[2]
            blob.download_to_filename(local_file)

def delete_npy_data(gcp, file_name):
    storage_file_path = 'npy/' + file_name + '.npy'
    blob_gcs = gcp['bucket'].blob(storage_file_path)
    blob_gcs.delete()
