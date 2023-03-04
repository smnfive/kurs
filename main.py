from my_token import TOKEN
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


access_token = TOKEN
user_id = 264521131
vk = VK(access_token, user_id)
pprint(vk.get_photo())
