# pixiv_dl
pixivのブックマークにある画像を自動でダウンロードできるスクレイピングツールです。<br>
必要なライブラリは標準ライブラリのtimeモジュールと、Requests のみです。<br>
個人的に趣味で作成したものなので、ご使用は自己責任でお願いします。

## 使用方法

### Cookieの指定
Chromeなどのブラウザで一度、自分のpixivアカウントにログインしておく。ブラウザ上で右クリックして「検証」→「NetWork」を開いた状態で[pixivサイト](https://www.pixiv.net/)に移動。表の「Name」が「 www.pixiv.net 」となっている行を選択し「Request Headers」の「cookie」の欄にある値をコピー。
それをpixiv_dl.py のcookieを指定している場所にペーストする。

### pixiv_dl.py の実行
```python pixiv_dl.py``` とすると非公開・公開ブックマークの選択、タグの指定の有無、イラスト取得件数を指定した後に画像がダウンロードされます。
