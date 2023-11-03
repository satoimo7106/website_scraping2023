import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import tkinter as tk
from tkinter import Scrollbar, Text
from tkinter import ttk


#とりあえずのエラー処理
# try:


#--------GUI-------------
def on_window_resize(event):
    # ウィンドウの幅と高さを取得
    window_width = event.width
    window_height = event.height

    # 表の幅と高さを調整
    tree_width = window_width - 20  # 余白を設定
    tree.column("URL", width=tree_width // 3)
    tree.column("パラメータ", width=tree_width // 3)
    tree.column("ページタイトル", width=tree_width // 3)

    # 入力欄の幅を調整
    input_width = window_width - 40  # 余白を設定
    entry1.config(width=input_width)
    entry2.config(width=input_width)
    
    # Treeviewの高さを調整
    treeview_height = window_height - 100  # 余白を設定
    tree["height"] = treeview_height


#Tkinterウィンドウの作成
root = tk.Tk()
root.title("自動巡回ツール")
root.geometry('400x300')
root.bind("<Configure>", on_window_resize)

#URLとドメインの入力欄
label1 = tk.Label(root, text="対象サイトのURLを入力してください（例：https://example.com/)")
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="対象のドメインを入力してください（例：example.com)")
label2.pack()

entry2 = tk.Entry(root)
entry2.pack()


# 列の識別名を指定
column = ('URL', 'パラメータ', 'ページタイトル')

# Treeviewの生成
tree = ttk.Treeview(root, columns=column)
# 列の設定
tree.column('#0',width=0, stretch='no')
tree.column('URL', anchor='w', width=80)
tree.column('パラメータ',anchor='w', width=100)
tree.column('ページタイトル', anchor='w', width=80)
# 列の見出し設定
tree.heading('#0',text='')
tree.heading('URL', text='URL',anchor='w')
tree.heading('パラメータ', text='パラメータ', anchor='w')
tree.heading('ページタイトル',text='ページタイトル', anchor='w')

# #実行結果を表示するテキストウィジェット
# text_widget = Text(root, wrap=tk.WORD)
# text_widget.pack(expand=True, fill="both")

# #テキストウィジェットにスクロールバーを追加
# scrollbar = Scrollbar(root, command=text_widget.yview)
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

    # text_widget.delete(1.0, tk.END)
    # #収集済みのURLを表示
    # text_widget.insert(tk.END, "\nURL|パラメータ|ページタイトル\n")
    # for url,parameter,title in zip(url_list,parameter_list,title_list):
    #     text_widget.insert(tk.END, f"{url}|{parameter}|{title}\n")

    # #キーワードリストを表示
    # text_widget.insert(tk.END, "\nKeyword\n")
    # for k in keyword_list:
    #     text_widget.insert(tk.END, f"{k}\n")

    # レコードの追加
    cnt=0
    for url,parameter,title in zip(url_list,parameter_list,title_list):
        cnt+=1
        tree.insert(parent='', index='end', iid=cnt ,values=(url, parameter,title))

# ウィジェットの配置
tree.pack(fill=tk.BOTH, expand=True)


#ボタンの作成
scraping_button = tk.Button(root, text="実行", command=lambda:website_scraping(str(entry1.get()),str(entry2.get())))
scraping_button.pack()

#ウィンドウのメインループ
root.mainloop()

# #何かしらのエラーが発生したらエラー表示
# except Exception:
#     print("エラーが発生しました")
#     input("Enterを押すと終了します")



