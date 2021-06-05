import firebase_admin
from firebase_admin import credentials, db, storage

from dotenv import load_dotenv
from flickrapi import FlickrAPI
import urllib
from urllib.request import urlretrieve
import os, time, sys, shutil

# .env ファイルをロードして環境変数へ反映
load_dotenv()

# flickr APIの設定
key = os.getenv('FLICKR_API_KEY')
secret = os.getenv('FLICKR_SECRET_KEY')
wait_time = 1

# bucket = storage.bucket()

def get_images(search_name, max_get_number):
    # firebaseのステータスを処理中に変更
    results_ref = db.reference('/results/images/')
    results_ref.child(search_name).set({
        'getImageStatus': 'progress',
        'maxGetNumber': max_get_number,
        'getImageNumber': 0,
    })

    #保存フォルダの指定
    # savedir = "./src/images"
    savedir = "./src/images/" + search_name

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

    for i, photo in enumerate(photos['photo']):
        # 画像が取得済みかどうかチェックし、なければfirebaseに登録
        # image_data = images_ref.get()
        # if image_data != None and image_data.get(photo['id']) != None: continue
        # storage_path = search_name + '/' + photo['id'] + '.jpg'
        if not os.path.exists(savedir):
            os.mkdir(savedir)

        # flickrからデータをダウンロード
        url_q = photo['url_q']
        images_ref.child(photo['id']).set({
            'path': url_q,
            'learn_image': True
        })
        filepath = savedir + '/' + photo['id'] + '.jpg'
        if os.path.exists(filepath): continue

        data = urllib.request.urlopen(url_q).read()
        urlretrieve(url_q, filepath)
        with open(filepath, mode="wb") as f:
            f.write(data)

        # firebase storageにアップロード
        # content_type = 'image/jpg'
        # blob = bucket.blob(storage_path)
        # with open(filepath, 'rb') as f:
        #     blob.upload_from_file(f, content_type=content_type)
        # time.sleep(wait_time)

    # localに落とした画像ファイルを削除
    # shutil.rmtree(savedir)
    # os.mkdir(savedir)

    # firebaseのステータスを更新
    results_ref.child(search_name).set({
        'getImageStatus': 'finish',
        'maxGetNumber': max_get_number,
        'getImageNumber': len(photos['photo'])
    })


def delete_images(image_name):
    delete_dir = "./src/images/" + image_name    
    if os.path.exists(delete_dir):
        shutil.rmtree(delete_dir)