#chatgptに考えてもらった
#アップロードするときのURLはhttps://example.com/が良さそう
import requests

url = 'https://example.com/'  # ウェブサイトのURLを指定
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
else:
    print("ウェブページを取得できませんでした。")


from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')

# 例: タイトルを取得
title = soup.title.string

links = soup.find_all('a')

for link in links:
    print(link.get('href'))

num_links = len(links)
num_paragraphs = len(soup.find_all('p'))

print(f"リンク数: {num_links}")
print(f"段落数: {num_paragraphs}")
