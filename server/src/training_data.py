import firebase_admin
from firebase_admin import credentials, db, storage

from dotenv import load_dotenv
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import os, time, sys, shutil, urllib

# .env ファイルをロードして環境変数へ反映
load_dotenv()

# flickr APIの設定
key = os.getenv('FLICKR_API_KEY')
secret = os.getenv('FLICKR_SECRET_KEY')
wait_time = 1.5

def get_images(gcp, search_name, max_get_number):
    # firebaseのステータスを処理中に変更
    results_ref = db.reference('/results/images/')
    results_ref.child(search_name).set({
        'getImageStatus': 'progress',
        'maxGetNumber': max_get_number,
        'getImageNumber': 0,
    })

    # 一時保存用のフォルダの指定
    savedir = "./src/temp/"

    flickr = FlickrAPI(key, secret, format='parsed-json')
    result = flickr.photos.search(
        text = search_name,
        per_page = max_get_number,
        media = 'photos',
        sort = 'relevance',
        safe_search = 1,
        extras = 'url_q, licence'
    )
    photos = result['photos']
    images_ref = db.reference('/images/' + search_name)

    if not os.path.exists(savedir):
        os.mkdir(savedir)

    for i, photo in enumerate(photos['photo']):
        # 画像が取得済みかどうかチェックし、なければfirebaseに登録
        image_data = images_ref.get()
        if image_data != None and image_data.get(photo['id']) != None: continue

        # flickrからデータをダウンロード
        url_q = photo['url_q']
        images_ref.child(photo['id']).set({
            'path': url_q,
            'learn_image': True
        })
        filepath = savedir + photo['id'] + '.jpg'

        data = urllib.request.urlopen(url_q).read()
        urlretrieve(url_q, filepath)
        with open(filepath, mode="wb") as f:
            f.write(data)

        # gcsにアップロード
        storage_file_path = 'images/' + search_name + '/' + photo['id'] + '.jpg'
        blob_gcs = gcp['bucket'].blob(storage_file_path)
        blob_gcs.upload_from_filename(filepath)
        time.sleep(wait_time)

    # localに落とした画像ファイルを削除
    shutil.rmtree(savedir)
    os.mkdir(savedir)

    # firebaseのステータスを更新
    results_ref.child(search_name).set({
        'getImageStatus': 'finish',
        'maxGetNumber': max_get_number,
        'getImageNumber': len(photos['photo'])
    })


def delete_images(gcp, image_name):
    prefix = 'images/' + image_name + '/'
    for gcs_file in gcp['client'].list_blobs(gcp['bucket_name'], prefix=prefix):
        blob = gcp['bucket'].blob(gcs_file.name)
        blob.delete()
    return