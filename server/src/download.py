from dotenv import load_dotenv
from flickrapi import FlickrAPI
import urllib
import json
# from pprint import pprint
import os, time, sys

# .env ファイルをロードして環境変数へ反映
load_dotenv()

# APIキーの情報
key = os.getenv('FLICKR_API_KEY')
secret = os.getenv('FLICKR_SECRET_KEY')

wait_time = 1


def get_images(serch_name):
#保存フォルダの指定
    serch_name = serch_name
    savedir = "./src/images"
    json_file = "./src/imageList.json"

    flickr = FlickrAPI(key, secret, format='parsed-json')
    result = flickr.photos.search(
        text = serch_name,
        per_page = 20,
        media = 'photos',
        sort = 'relevance',
        safe_search = 1,
        extras = 'url_q, licence'
    )

    photos = result['photos']
    # 返り値を表示する
    # pprint(photos)

    json_data = {'result': []}

    for i, photo in enumerate(photos['photo']):
        url_q = photo['url_q']
        filepath = savedir + '/' + photo['id'] + '.jpg'
        json_data['result'].append(photo['id'] + '.jpg')
        if os.path.exists(filepath): continue
        data = urllib.request.urlopen(url_q).read()
        with open(filepath, mode="wb") as f:
            f.write(data)
        time.sleep(wait_time)
    
    with open(json_file, mode='wt', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)