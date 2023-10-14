#chatgptに考えてもらった
#アップロードするときのURLはhttps://example.com/が良さそう（実行時はテスト用のサイトに書き換えること）
import requests

url = 'http://127.0.0.1:5500/testsite/index.html'  # ウェブサイトのURLを指定
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
else:
    print("ウェブページを取得できませんでした。")


from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')

# 例: タイトルを取得
title = soup.title.string

# すべてのリンク（<a>要素）を取得
links = soup.find_all('a')


# 各リンクのURLを表示
for link in links:
    print(link.get('href'))

num_links = len(links)

print("リンク数:"+ str(num_links))


#スタートのページのリンクを全部取得
# まだ行ったことがないリンクだったら（繰り返し）
    # 取得したリンク先に移動
    # そのページのリンクを全部取得
