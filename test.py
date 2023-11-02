import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import tkinter as tk
from tkinter import Scrollbar, Text



#とりあえずのエラー処理
# try:


#--------GUI-------------

#Tkinterウィンドウの作成
window = tk.Tk()
window.title("自動巡回ツール")

#ラベルと入力欄の作成
label1 = tk.Label(window, text="対象サイトのURLを入力してください（例：https://example.com/)")
label1.pack()

entry1 = tk.Entry(window)
entry1.pack()

label2 = tk.Label(window, text="対象のドメインを入力してください（例：example.com)")
label2.pack()

entry2 = tk.Entry(window)
entry2.pack()

#実行結果を表示するテキストウィジェット
text_widget = Text(window, wrap=tk.WORD)
text_widget.pack(expand=True, fill="both")

# #テキストウィジェットにスクロールバーを追加
# scrollbar = Scrollbar(window, command=text_widget.yview)
# scrollbar.pack(side="right", fill="y")
# text_widget.config(yscrollcommand=scrollbar.set)


#URLを格納するリスト
url_list = []

#パラメータを格納するリスト
parameter_list=[]

#ページタイトルを格納するリスト
title_list=[]

#抽出したキーワード(MBSD{xxxx})を格納するリスト
keyword_list = []

def website_scraping(start_url,target_domain):


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
            if href and href not in url_list and target_domain in href:
                # 収集済みのURLでない場合に再帰的に処理
                get_urls(href)

    #各リストの内容をクリア
    url_list.clear()
    parameter_list.clear()
    title_list.clear()
    keyword_list.clear()
    
    #URLを収集
    if target_domain in start_url:
        get_urls(start_url)

    text_widget.delete(1.0, tk.END)
    #収集済みのURLを表示
    text_widget.insert(tk.END, "\nURL|パラメータ|ページタイトル\n")
    for url,parameter,title in zip(url_list,parameter_list,title_list):
        text_widget.insert(tk.END, f"{url}|{parameter}|{title}\n")

    #キーワードリストを表示
    text_widget.insert(tk.END, "\nKeyword\n")
    for k in keyword_list:
        text_widget.insert(tk.END, f"{k}\n")


#ボタンの作成
scraping_button = tk.Button(window, text="実行", command=lambda:website_scraping(str(entry1.get()),str(entry2.get())))
scraping_button.pack()

#ウィンドウのメインループ
window.mainloop()

# #何かしらのエラーが発生したらエラー表示
# except Exception:
#     print("エラーが発生しました")
#     input("Enterを押すと終了します")



