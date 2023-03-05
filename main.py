import json

from my_token import TOKEN_VK
from my_token import TOKEN_YA
import requests
from pprint import pprint
import json as js
import urllib

class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photo(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {**self.params, 'owner_id': self.id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1}
        response = requests.get(url, params=params)
        return response.json()


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def make_upload_link(self, name_your_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": name_your_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()['href']

    def upload(self, name_your_path, url_photo_vk):
        href = self.make_upload_link(name_your_path=name_your_path)
        params = {'path': name_your_path, 'url': url_photo_vk}
        response = requests.post(url=href, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def create_folder(self, name_your_path):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': name_your_path}
        response = requests.put(files_url, headers=headers, params=params)
        return response.json()



access_token = TOKEN_VK
token = TOKEN_YA
user_id = 264521131
vk = VK(access_token, user_id)
ya = YandexDisk(token)
max_photo_count = vk.get_photo()['response']['count']
max_photo = vk.get_photo()['response']['items']
new = []
URL = []

# my_dic = {new[i]: new[i+1] for i in range(0, len(new), 2)}
# json_ob = json.dumps(my_dic, indent=4)
# print(type(vk.get_photo())

for i in max_photo:
    for j in i['sizes']:
        if j['type'] == 'z':
            new.append({i['likes']['count']: j['url']})
            URL.append(j['url'])
a = URL[0]
folder_for_photos = ya.create_folder('downloaded_photos')
ya.upload(folder_for_photos, a)