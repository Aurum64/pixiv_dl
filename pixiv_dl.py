import requests
from bs4 import BeautifulSoup
import time
import json
import os


pixiv_domain = 'https://www.pixiv.net/'
import authentication
cookie = 'pixivにアクセスした際のcookieをコピーしてください。'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "cookie": cookie
}

#ファイルのダウンロード先を指定
output_folder = '.'


def accessBookmark(sheets):
    p = 1
    all_page = 1
    all_works = []
    i = 0
    flag = False
    res = requests.get(f'{pixiv_domain}ajax/user/extra?lang=ja', headers=headers)
    userId = res.headers['X-UserId']
    
    while p <= all_page:
        time.sleep(1)
        offset = 100*(p-1)
        res = requests.get(f'{pixiv_domain}ajax/user/{userId}/illusts/bookmarks?tag=&offset={offset}&limit=100&rest=show&lang=ja', headers=headers)
        data = res.json()

        total = data['body']['total']
        sheets = total if sheets == 'all' else int(sheets)
        sheets = sheets if sheets < total else total
        all_page = total // 100 + 1

        works = data['body']['works']
        for work in works:
            all_works += [work['id']]
            i += 1
            if i >= sheets :
                flag = True
                break
        if flag : break
        p += 1
    return all_works[::-1]

def getUrls(works):
    urls = []
    for i, illust_id in enumerate(works):
        time.sleep(1)
        print(f'\r{len(works)}中{i+1}件目の画像URLを取得中', end='')
        session = requests.Session()
        res = session.get(f"{pixiv_domain}ajax/illust/{illust_id}/pages?lang=ja", headers=headers)
        data = res.json()['body']
        urls += [d['urls']['original'] for d in data]
    return urls

if __name__ == '__main__':
    sheets = input('イラスト取得件数を入力してください。（すべてダウンロードする場合は「all」と入力）\n')
    works = accessBookmark(sheets)
    urls = getUrls(works)
    downloadImage(urls)
