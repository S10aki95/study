"""
mockの使い方について

<このサンプルコードで学ぶ内容>
* pytest-mock(MockFixture)を使用する方法について
-> 単純なmockの方法では対応できないケースや、クラス内でのmockの方法について、基本的な内容をまとめる。

<テスト内容については以下を参照>
参照:test/test_example_2.py

<操作手順>
1. 名前と部署が管理されたエクセルシート読み込む
2. GUIでリストから必要な部署を選択する
3. 選択された部署の人物について名前を並び替えを行う
"""

#%%
# 必要なライブラリのインストール
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk


#%%
# GUIの作成
class Main(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # 表示場所の調節
        self.pack()
        #縦幅400横幅200に画面サイズを変更します。
        master.geometry("300x300")
        #タイトルを指定
        master.title("部署の選択")
        
        # 部署のリストの作成
        self.busho_list = ["担当役員", "部長", "-"]
        self.select_listbox  =  Listbox(
            master, 
            listvariable=StringVar(value=self.busho_list), 
            height=5, 
            selectmode= MULTIPLE
            )
        
        # リストボックスの場所の調整
        self.select_listbox.pack(side='left')
        # 入力完了ボタン関係の設定
        self.button = Button(master, text = "入力完了", command = lambda:[self.selection_input(), master.destroy()])
        # ボタンの位置の調整
        self.button.place(x=50, y=20)
        # タイトル入力
        font2 = font.Font(family='Times', size=10)
        label = Label(master, text="部署の選択", font=font2)
        label.pack()
        
        
    def selection_input(self):
        """選択された内容を保存する
        
        リストボックスで選択されたアイテムについてリスト形式で取り出す。
        """
        self.tmp =  [self.select_listbox.get(i) for i in self.select_listbox.curselection()]




class name_management(Main):
    def __init__(self):
        
        # 必要な部署情報の作成をGUI上で完結させる。
        # GUIのフレームワークの作成
        self.app = Tk()
        super().__init__(self.app)
        
        self.tmp = None
        
        # GUIの起動
        #self.activate_GUI()
        
        # 部署情報のエクセルシートの読み込み
        self.df = pd.read_csv('C:/Users/akihiro/study_memo/python/ユニットテスト/test_for_unittest/data/busho_list_example.csv', encoding='SHIFT-JIS')
        
        
    def activate_GUI(self):
        """GUIの起動
        GUIを起動して、必要な部署情報を入力させる。
        """
        self.app.mainloop()
    
    def person_sort(self):
        """GUIに入力された部署のリストをもとに人物の抽出と並びかえ
        
        注意:
        1. "self.tmp"はGUIで入力された部署のリスト
        ※このように明示的にDocstringに直接コメントしなければならないのか？
        ->明示的に継承クラスの変数を使っていることをいう方法があれば変更する。
        """
        self.df = self.df[self.df['部署名'].isin(self.tmp)]
        self.df.sort_values(by = '人物', ascending = False, inplace = True)


if __name__ == '__main__':
    test = name_management()