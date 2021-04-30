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

output_folder = r'D:\pixiv_test'

def accessBookmark(sheets):
    p = 1
    all_page = 1
    all_illusts = []
    i = 0
    flag = False
    while p <= all_page:
        time.sleep(1)
        session = requests.Session()
        res = session.get(f'{pixiv_domain}bookmark.php?rest=show&type=illust_all&p={p}', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        count_badge = int(soup.select_one('.column-label').span.get_text().replace('件', ''))
        if sheets == 'all': sheets = count_badge
        sheets = int(sheets)
        all_page = count_badge // 20 + 1
        
        item_list = soup.select('#wrapper > div.layout-a > div.layout-column-2 > div._unit.manage-unit > form > div.display_editable_works > ul > li')
        for item in item_list:
            all_illusts += [{
                'illust_id': item.find(class_='ui-scroll-view')['data-id'],
                'single' : not item.find(class_='page-count')
            }]
            i += 1
            if i >= sheets :
                flag = True
                break
        if flag : break
        p += 1
    return all_illusts[::-1]

def getUrls(illusts):
    urls = []
    for i, illust in enumerate(illusts):
        time.sleep(1)
        print(f'\r{len(illusts)}中{i+1}件目の画像URLを取得中', end='')
        if illust['single']:
            session = requests.Session()
            res = session.get(f"{pixiv_domain}artworks/{illust['illust_id']}", headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            json_data = soup.select_one('#meta-preload-data')['content']
            data = json.loads(json_data)
            urls += [data['illust'][illust['illust_id']]['urls']['original']]
        else:
            session = requests.Session()
            res = session.get(f"{pixiv_domain}ajax/illust/{illust['illust_id']}/pages?lang=ja", headers=headers)
            data = res.json()['body']
            urls += [d['urls']['original'] for d in data]
    return urls

def downloadImage(urls):
    for i, url in enumerate(urls):
        time.sleep(1)
        session = requests.Session()
        res = session.get(url, headers={"referer": pixiv_domain})
        if res.status_code == 200:  
            file_name = url.split('/')[-1]
            with open(f'{output_folder}/{file_name}', 'wb') as fout:
                fout.write(res.content)
        else:
            print(f'404error at {url}')
        print(f'\r{len(urls)}件中{i+1}件 画像ダウンロード完了', end='')

if __name__ == '__main__':
    sheets = input('画像取得件数を入力してください。（すべてダウンロードする場合は「all」と入力）\n')
    illsts = accessBookmark(sheets)
    urls = getUrls(illsts)
    downloadImage(urls)