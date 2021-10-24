import requests
import time

pixiv_domain = 'https://www.pixiv.net/'
cookie = 'pixivにアクセスした際のcookieをコピーしてください。'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "cookie": cookie
}

#ファイルのダウンロード先を指定
output_folder = '.'

def accessBookmark(sheets, tag="", rest="1"):
    p = 1
    all_page = 1
    all_works = []
    i = 0
    flag = False
    res = requests.get(f'{pixiv_domain}ajax/user/extra?lang=ja', headers=headers)
    if res.json()['error'] : print("cookieが無効です"); return []
    userId = res.headers['X-UserId']
    rest = 'hide' if rest == "2" else 'show'
    while p <= all_page:
        time.sleep(1)
        offset = 100*(p-1)
        res = requests.get(f'{pixiv_domain}ajax/user/{userId}/illusts/bookmarks?tag={tag}&offset={offset}&limit=100&rest={rest}&lang=ja', headers=headers)
        data = res.json()

        total = data['body']['total']
        if not total : print('指定されたイラストは見つかりませんでした。')
        sheets = total if sheets == 'all' else int(sheets)
        sheets = sheets if sheets < total else total
        all_page = total // 100 + 1

        for work in data['body']['works']:
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
        print(f'\r{len(works)}件中{i+1}件目の画像URLを取得中', end='')
        session = requests.Session()
        res = session.get(f"{pixiv_domain}ajax/illust/{illust_id}/pages?lang=ja", headers=headers)
        data = res.json()['body']
        urls += [d['urls']['original'] for d in data]
    return urls

def downloadImage(urls):
    for i, url in enumerate(urls):
        time.sleep(1)
        res = requests.get(url, headers={"referer": pixiv_domain})
        if res.status_code == 200:  
            file_name = url.split('/')[-1]
            with open(f'{output_folder}/{file_name}', 'wb') as fout:
                fout.write(res.content)
        else:
            print(f'404error at {url}')
        print(f'\r{len(urls)}件中{i+1}件 画像ダウンロード完了', end='')

if __name__ == '__main__':
    rest = input('ブックマークの公開・非公開を選択\n1: 公開\n2: 非公開\n')
    tag = input('タグ名：') if input('タグを指定しますか?\n1: はい\n2: いいえ\n') == '1' else ''
    sheets = input('イラスト取得件数を入力してください。（すべてダウンロードする場合は「all」と入力）\n')
    works = accessBookmark(sheets, tag, rest)
    urls = getUrls(works)
    downloadImage(urls)
