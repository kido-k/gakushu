json_file = "../front/src/assets/imageList.json"

json_data = {'result': []}
json_data['result'].append('hoge.jpg')

print(json_data)


with open(json_file, mode='wt', encoding='utf-8') as file:
    json.dump(json_data, savedir, ensure_ascii=False, indent=2)