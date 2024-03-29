import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv


#エラー処理
try:


    #ウィンドウサイズに応じてGUIの調整をする関数
    def on_window_resize(event):
        # ウィンドウの幅と高さを取得
        window_width = event.width

        # 表の幅と高さを調整
        result_treeview.column("URL", width=window_width // 4)
        result_treeview.column("パラメータ", width=window_width // 4)
        result_treeview.column("ページタイトル", width=window_width // 4)
        result_treeview.column("キーワード", width=window_width // 4)

        # 入力欄の幅を調整
        entry1.config(width=window_width)
        entry2.config(width=window_width)

        # ボタンのサイズを調整
        scraping_button.config(width=window_width)
        csv_export_button.config(width=window_width)



    #Tkinterウィンドウの作成
    root = tk.Tk()
    root.title("自動巡回ツール")
    #ウィンドウの初期サイズを設定
    root.geometry('600x500')
    # ウィンドウの最小サイズを設定
    root.minsize(600, 500)

    #ウィンドウサイズが変化したときにGUIのサイズを調整する
    root.bind("<Configure>", on_window_resize)

    #URLの入力欄
    label1 = tk.Label(root, text="対象サイトのURLを入力してください（例：https://example.com/)")
    label1.pack()

    entry1 = tk.Entry(root)
    entry1.pack(padx=10,pady=10)

    #ドメインの入力欄
    label2 = tk.Label(root, text="対象のドメインを入力してください（例：example.com)")
    label2.pack()

    entry2 = tk.Entry(root)
    entry2.pack(padx=10,pady=10)


    # 列名を設定
    column = ('URL', 'パラメータ', 'ページタイトル','キーワード')

    # Treeviewの生成
    result_treeview = ttk.Treeview(root, columns=column)
    # 列の設定
    result_treeview.column('#0',width=0, stretch='no')
    result_treeview.column('URL', anchor='w', width=80)
    result_treeview.column('パラメータ',anchor='w', width=80)
    result_treeview.column('ページタイトル', anchor='w', width=80)
    result_treeview.column('キーワード', anchor='w', width=80)

    # 列の見出し設定
    result_treeview.heading('#0',text='')
    result_treeview.heading('URL', text='URL',anchor='w')
    result_treeview.heading('パラメータ', text='パラメータ', anchor='w')
    result_treeview.heading('ページタイトル',text='ページタイトル', anchor='w')
    result_treeview.heading('キーワード',text='キーワード', anchor='w')


    #URLを格納するリスト
    url_list = []

    #パラメータを格納するリスト
    parameter_list=[]

    #ページタイトルを格納するリスト
    title_list=[]

    #抽出したキーワード(MBSD{xxxx})を格納するリスト
    keyword_list = []

    #ウェブサイトの規模を調査する関数
    def website_scraping(start_url,target_domain):

        #treeviewの内容をクリア
        result_treeview.delete(*result_treeview.get_children())

        #各リストの内容をクリア
        url_list.clear()
        parameter_list.clear()
        title_list.clear()
        keyword_list.clear()


        #URLからリンクを収集、再帰的に処理する関数
        def get_urls(url):

            # URLをurl_listに追加
            url_list.append(url)

            try:
                # ページのコンテンツを取得
                response = requests.get(url)
            except requests.exceptions.MissingSchema:
                messagebox.showerror("エラー", "URLの形式が正しくありません。\nURLはhttp:// または https://から始まる形式で入力してください")

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
            #取得できなかった場合、パラメータリストに"なし"を追加
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
            keywords=re.findall(r'MBSD\{[^\}]*\}', website_text)

            #キーワードが取得できた場合、キーワードリストに追加
            if keywords:
                keywords=','.join(map(str, keywords))
                keyword_list.append(keywords)
            #取得できなかった場合、キーワードリストに"なし"を追加
            else:
                keyword_list.append("なし")

            for link in links:
                #aタグのhref属性（URL部分）を取得
                href = link.get('href')
                if href and href not in url_list and target_domain in href:
                    # 収集済みのURLでない場合に再帰的に処理
                    get_urls(href)

        #URLを収集
        if target_domain in start_url:
            get_urls(start_url)

        #実行結果を表形式にする
        cnt=0
        for url,parameter,title,keyword in zip(url_list,parameter_list,title_list,keyword_list):
            cnt+=1
            result_treeview.insert(parent='', index='end', iid=cnt ,values=(url, parameter,title,keyword))

    #csvでエクスポートする関数
    def export_to_csv():
        #表が空の時の処理
        if not result_treeview.get_children():
            messagebox.showerror("エラー", "出力前に実行してください。")
            return
        
        # ファイル保存ダイアログを表示し、CSVファイルのファイル名と保存場所を選択
        file_path = filedialog.asksaveasfilename(title = "名前を付けて保存",defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

        # ファイル名が空のときは処理をしない
        if not file_path:
            return

        with open(file_path, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["URL", "パラメータ", "ページタイトル","キーワード"])
            for item in result_treeview.get_children():
                values = result_treeview.item(item)["values"]
                csvwriter.writerow(values)

    #実行結果の表
    result_treeview.pack(fill=tk.BOTH, expand=True)


    #実行ボタン
    scraping_button = tk.Button(root, text="実行", command=lambda:website_scraping(str(entry1.get()),str(entry2.get())))
    scraping_button.pack(padx=10,pady=10)

    # エクスポートボタン
    csv_export_button = tk.Button(root, text="実行結果をCSVで出力", command=export_to_csv)
    csv_export_button.pack(padx=10,pady=10)

    #ウィンドウのメインループ
    root.mainloop()

# #何かしらのエラーが発生したらエラー表示
except Exception as e:
    messagebox.showerror("エラー", "エラーが発生しました。")



