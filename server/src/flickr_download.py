import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage

from dotenv import load_dotenv
from flickrapi import FlickrAPI
import urllib
import os, time, sys, shutil

# .env ファイルをロードして環境変数へ反映
load_dotenv()

# flickr APIの設定
key = os.getenv('FLICKR_API_KEY')
secret = os.getenv('FLICKR_SECRET_KEY')
wait_time = 1

# firebaseの設定
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
bucket = storage.bucket()

def get_images(search_name):
    #保存フォルダの指定
    savedir = "./src/images"

    flickr = FlickrAPI(key, secret, format='parsed-json')
    result = flickr.photos.search(
        text = search_name,
        per_page = 20,
        media = 'photos',
        sort = 'relevance',
        safe_search = 1,
        extras = 'url_q, licence'
    )
    photos = result['photos']
    images_ref = db.reference('/images/' + search_name)

    for i, photo in enumerate(photos['photo']):
        # 画像が取得済みかどうかチェックし、なければfirebaseに登録
        image_data = images_ref.get()
        if image_data.get(photo['id']) != None: continue
        images_ref.child(photo['id']).set({
            'path': photo['id'] + '.jpg',
        })

        # flickrからデータをダウンロード
        url_q = photo['url_q']
        data = urllib.request.urlopen(url_q).read()
        filepath = savedir + '/' + photo['id'] + '.jpg'
        with open(filepath, mode="wb") as f:
            f.write(data)

        # firebase storageにアップロード
        content_type = 'image/jpg'
        storage_path = search_name + '/' + photo['id'] + '.jpg'
        blob = bucket.blob(storage_path)
        with open(filepath, 'rb') as f:
            blob.upload_from_file(f, content_type=content_type)
        time.sleep(wait_time)

    # localに落とした画像ファイルを削除
    shutil.rmtree(savedir)
    os.mkdir(savedir)