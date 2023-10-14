import requests
from bs4 import BeautifulSoup
import re

# すべての収集済みURLを格納するセット
collected_urls = set()

# 抽出したテキストを格納するリスト
extracted_texts = []

# 指定したURLからリンクを収集し、テキストを抽出し、再帰的に処理する関数
def collect_urls_and_extract_text(url, depth=1, max_depth=3):
    if depth > max_depth:
        return

    # URLを収集
    collected_urls.add(url)

    # ページのコンテンツを取得
    response = requests.get(url)
    page_content = response.text

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(page_content, 'html.parser')

    # すべてのリンク（<a>要素）を取得
    links = soup.find_all('a')

    for link in links:
        href = link.get('href')
        if href:
            # 絶対URLに変換
            if not href.startswith('http'):
                href = url + href
            # 収集済みのURLでない場合に再帰的に処理
            if href not in collected_urls:
                collect_urls_and_extract_text(href, depth + 1)

    # テキストを抽出
    text = soup.get_text()
    # 正規表現を使用して"TEST{xxxx}"のパターンを抽出
    matches = re.findall(r'TEST\{[^\}]*\}', text)
    extracted_texts.extend(matches)

# スタートURLを指定
start_url = 'http://127.0.0.1:5500/testsite/index.html'

# URLを収集し、テキストを抽出
collect_urls_and_extract_text(start_url)

# 収集済みのURLを表示
print("Collected URLs:")
for url in collected_urls:
    print(url)

# 抽出したテキストを表示
print("\nExtracted Texts:")
for text in extracted_texts:
    print(text)
