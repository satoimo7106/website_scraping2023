import requests

url = 'https://scraping-training.vercel.app/site?postCount=30&title=%E3%81%93%E3%82%8C%E3%81%AF{no}%E3%81%AE%E8%A8%98%E4%BA%8B%E3%81%A7%E3%81%99&dateFormat=YYYY-MM-DD&isTime=true&timeFormat=&isImage=true&interval=360&isAgo=true&countPerPage=10&page=1&robots=true&'  # ウェブサイトのURLを指定
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
