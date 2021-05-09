import requests

with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()
with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_vk, version):
        self.token_vk = token_vk
        self.version = version
        self.params = {
            'access_token': self.token_vk,
            'v': self.version
        }

    def get_photos(self, vk_album, owner_id, count=200):
        photos_url = self.url + 'photos.get'
        photos_params = {'owner_id': owner_id,
                         'album_id': vk_album,
                         'extended': 1,
                         'photo_sizes': 1,
                         'count': count}
        response = requests.get(photos_url, params={**self.params, **photos_params})
        return response.json()['response']['items']

class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token_ya: str):
        self.token_ya = token_ya

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token_ya)
        }

    def folder(self, yandex_path):
        create_url = self.url + 'resources/'
        create_params = {'path': yandex_path}
        requests.put(create_url, headers=self.get_headers(), params=create_params)

    def upload_from_url(self, yandex_path: str, photo_url: str):
        upload_url = self.url + 'resources/upload'
        upload_params = {'path': yandex_path, 'url': photo_url}
        requests.post(upload_url, headers=self.get_headers(), params=upload_params)

def copy_photo_ya(uploader, vk_VkUser, album_name, user_id, count=200):
    print('Загружается...')
    uploader.folder(f'{album_name}/')
    photos = vk_VkUser.get_photos(album_name.lower(), user_id, count)
    count_list = []
    for photo in photos:
        namber_count = photo["likes"]["count"]
        if namber_count in count_list:
            photo_path = f'{album_name}/{str(photo["likes"]["count"])}_{photo["date"]}.jpg'
            uploader.upload_from_url(photo_path, photo['sizes'][-1]['url'])
            count_list.append(namber_count)
        else:
            photo_path = f'{album_name}/{str(photo["likes"]["count"])}.jpg'
            uploader.upload_from_url(photo_path, photo['sizes'][-1]['url'])
            count_list.append(namber_count)
    print('Загрузка завершена')

if __name__ == '__main__':
    album_name = 'Profile'
    user_id = 552934290
    vk_VkUser = VkUser(token_vk, '5.130')
    ya_uploader = YaUploader(token_ya)
    copy_photo_ya(ya_uploader, vk_VkUser, album_name, user_id)