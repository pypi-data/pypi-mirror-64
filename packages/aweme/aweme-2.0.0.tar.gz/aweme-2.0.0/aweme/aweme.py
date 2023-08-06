#!/usr/bin/env python3


import os
from concurrent.futures import ThreadPoolExecutor
import fire
import requests


DOWNLOAD_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36'
}

API_BASE = 'https://douyin.asyncfunc.com'
s = requests.Session()


class Aweme:
    """douyin cli
    """

    def __init__(self):
        pass

    def user(self, uid):
        """user info

        :param uid: douyin user uid
        :return:
        """
        res = s.get(f'{API_BASE}/api/user/{uid}')
        return res.json()

    def video(self, aweme_id):
        """video detail

        :param aweme_id: douyin video id
        :return:
        """
        res = s.get(f'{API_BASE}/api/video/{aweme_id}')
        return res.json()

    def user_video(self, uid, max_cursor=0):
        """user video list

        :param uid: douyin user uid
        :return:
        """
        res = s.get(f'{API_BASE}/api/user/{uid}/video?max_cursor={max_cursor}')
        return res.json()

    def search(self, keyword):
        """user search

        :param keyword: user nickname or uid..
        :return:
        """
        res = s.get(f'{API_BASE}/api/search_user?keyword={keyword}')
        return res.json()

    def download_video(self, aweme_id, download_dir='download'):
        """download video

        :param aweme_id: video id
        :param download_dir: download dir
        :return:
        """
        data = self.video(aweme_id)['aweme_detail']
        uid = data['author']['uid']
        video_url = data['video']['play_addr']['url_list'][0]

        save_path = os.path.join(download_dir, uid)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, f'{aweme_id}.mp4')
        if os.path.exists(file_path):
            print(f'file {uid}/{aweme_id} exists')
        else:
            r = requests.get(video_url, stream=True, headers=DOWNLOAD_HEADERS)
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                print(f'download {uid}/{aweme_id} success')
            else:
                print(f'download {uid}/{aweme_id} err: {r.status_code}')

    def download_user_videos(self, uid, download_dir='download'):
        """download user videos

        :param uid:
        :param download_dir:
        :return:
        """
        max_cursor = 0
        with ThreadPoolExecutor() as executor:
            while True:
                # print(max_cursor)
                data = self.user_video(uid, max_cursor=max_cursor)
                has_more = data.get('has_more')
                max_cursor = data.get('max_cursor')
                aweme_list = data.get('aweme_list')

                if not (has_more or aweme_list):
                    # print(data)
                    break

                save_path = os.path.join(download_dir, str(uid))
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                for video in aweme_list:
                    uid = video['author']['uid']
                    aweme_id = video['aweme_id']
                    video_url = video['video']['play_addr']['url_list'][0]
                    file_path = os.path.join(save_path, f'{aweme_id}.mp4')

                    if os.path.exists(file_path):
                        print(f'file {uid}/{aweme_id} exists')
                    else:
                        executor.submit(self._download, video_url, file_path, uid, aweme_id)

    def _download(self, video_url, file_path, uid, aweme_id):
        # print(f'start download {uid}/{aweme_id} success')
        r = requests.get(video_url, stream=True, headers=DOWNLOAD_HEADERS)
        if r.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f'download {uid}/{aweme_id} success')
        else:
            print(f'download {uid}/{aweme_id} err: {r.status_code}')


def main():
    fire.Fire(Aweme)


if __name__ == '__main__':
    fire.Fire(Aweme)
