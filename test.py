import requests
from bs4 import BeautifulSoup
import re

# すべての収集済みURLを格納するセット
url_list = []

# 抽出したテキストを格納するリスト
keyword_list = []

#キーワードを抽出する処理
def get_keyword(text):
    # 正規表現を使用して"TEST{xxxx}"のパターンを抽出
    matches = re.findall(r'TEST\{[^\}]*\}', text)
    keyword_list.extend(matches)
    return

# 指定したURLからリンクを収集、再帰的に処理する関数
#関数名を後で変えたい
def get_urls(url):

    # URLを収集
    url_list.append(url)

    # ページのコンテンツを取得
    response = requests.get(url)
    page_content = response.text

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(page_content, 'html.parser')

    # すべてのリンク（<a>要素）を取得
    links = soup.find_all('a')

    # テキストを抽出
    text = soup.get_text()

    #【要修正】（再帰的に、そのページのすべてのキーワードを収集するようにする）
    #keywordを抽出する関数
    get_keyword(text)

    for link in links:
        #aタグのhref属性（URL部分）を取得
        href = link.get('href')
        if href:
            # 【要修正】絶対URLに変換（URLが"http"から始まっていない場合）
            if not href.startswith('http'):
                href = url + href
            # 収集済みのURLでない場合に再帰的に処理
            if href not in url_list:
                get_urls(href)

#【要修正】スタートURLを指定（将来的には利用者が入力できるように）
start_url = 'http://127.0.0.1:5500/testsite/index.html'

# URLを収集
get_urls(start_url)

# 収集済みのURLを表示
print("URLs:")
for url in url_list:
    print(url)

# 抽出したテキストを表示
print("\nKeyWord:")
for keyword in keyword_list:
    print(keyword)
