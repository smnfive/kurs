from my_token import TOKEN_VK
from my_token import TOKEN_YA
import requests
from pprint import pprint


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
        params = {**self.params, 'owner_id': 264521131, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1}
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
        response = requests.put(href, data=url_photo_vk)
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

access_token = TOKEN_VK
token = TOKEN_YA
user_id = 264521131
vk = VK(access_token, user_id)
ya = YandexDisk(token)
pprint(vk.get_photo())
