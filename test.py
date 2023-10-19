import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
# import html5lib

#とりあえずのエラー処理
try:

    # URLを格納するリスト
    url_list = []

    #パラメータを格納するリスト
    parameter_list=[]

    #ページタイトルを格納するリスト
    title_list=[]

    # 抽出したキーワード(MBSD{xxxx})を格納するリスト
    keyword_list = []

    #スタートURLを指定（将来的には利用者が入力できるように）
    print("対象サイトのURLを入力してください（例：https://example.com/)")
    start_url=input() #入力する場合（CUI)

    #対象のドメインを指定
    print("対象のドメインを入力してください（例：example.com)")
    target_domain=input() #入力する場合（CUI)

    #URLからリンクを収集、再帰的に処理する関数
    def get_urls(url):

        # URLをurl_listに追加
        url_list.append(url)
        
        # ページのコンテンツを取得
        response = requests.get(url)

        # BeautifulSoupを使用してHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # すべてのリンク（<a>要素）を取得
        links = soup.find_all('a')

        # テキストを抽出
        website_text = soup.get_text()

        #URLからパラメータ（q="xxxx")を取得
        parameter=urllib.parse.urlparse(url).query
        #パラメータが取得できた場合、パラメータリストに追加
        if parameter:
            parameter_list.append(parameter)
        #【要検討】取得できなかった場合、パラメータリストに"なし"を追加
        else:
            parameter_list.append("なし")

        #ページタイトルを取得
        #ページタイトルが取得できた場合、ページタイトルリストに追加
        if soup.title:
            title_list.append(soup.title.string)
        #取得できなかった場合、ページタイトルリストに"なし"を追加
        else:
            title_list.append("なし")


        #キーワードを抽出する
        # 正規表現を使用して"MBSD{xxxx}"を抽出して一致したものをすべてリストに格納
        keyword=re.findall(r'MBSD\{[^\}]*\}', website_text)

        for k in keyword:
            #キーワードリストに含まれていない場合に追加
            if k not in keyword_list:
                keyword_list.append(k)


        for link in links:
            #aタグのhref属性（URL部分）を取得
            href = link.get('href')
            if href and href not in url_list:
                # 収集済みのURLでない場合に再帰的に処理
                get_urls(href)


    #URLを収集
    # if target_domain in start_url:
    get_urls(start_url)

    #収集済みのURLを表示
    print("\nURL|パラメータ|ページタイトル")
    for url,parameter,title in zip(url_list,parameter_list,title_list):
        print(url,parameter,title)

    #キーワードリストを表示
    print("\nKeyWord:")
    for k in keyword_list:
        print(k)
        
#何かしらのエラーが発生したらエラー表示
except Exception: 
    print("エラーが発生しました")
