import re
import os
import glob
import pandas as pd
from bs4 import BeautifulSoup

GOOGLE_AD = """"""

def remove_newlines(text):
    """
    文字列の先頭と末尾にある改行コードを除外する関数。
    中間の改行コードは残す。
    
    Args:
        text: 文字列
        
    Returns:
        (定義なし): 処理後の文字列
    """
    return re.sub(r"(^\n+)|(\n+$)", "", text)

def replace_and_write(text, replaced_markers, replace_contents, output_file_name):
    """
    テキスト内の特定のマーカーを置換し、結果をファイルに書き込む関数。
    
    Args:
        text: 置換対象の文字列
        replaced_markers: 置換するマーカーのリスト
        replace_contents: 置換する内容のリスト。replaced_markersと同じ長さである必要あり
        output_file_name: 結果を書き込むファイルの名前
    """
    
    # 置換
    for m,c in zip(replaced_markers, replace_contents):
        text = text.replace(m, c, 1) # mをcで1回だけ置換
    
    # 出力
    with open(output_file_name, 'w', encoding='utf-8') as f:
        f.write(text)


def format_tag(tag):
    # tagに記号やスペースがある場合はハイフンに置き換える
    return tag.replace('.','-').replace('_','-').replace(' ','-').replace(',','-')


def collect_articles_info():
    """
    記事の情報を集約する関数。
    より具体的には、postディレクトリ内のhtmlファイルを解析し、各ファイル(=各記事)の中からsort-by-date.html等で表示すべき情報を抽出する関数。
    Returns:
        df: 記事情報をまとめたpandas DataFrame。 
    """
    data = []
    for file_path in glob.glob("posts/20*.html"):
        file_name = os.path.splitext(os.path.basename(file_path))[0] # ファイル名を取得
        date = ' - '.join(file_name.split('-')[:3]) # ファイル名から日付を取得
        month = ' - '.join(file_name.split('-')[:2])
        
        with open(file_path, 'r', encoding='utf-8') as file:
            # BeautifulSoupを用いてHTMLを解析
            soup = BeautifulSoup(file, 'html.parser')
            
            # タイトルの取得
            title = soup.find('div', id='center').find('h1').get_text()
            
            # メタデータとして設定している記事のタグの取得
            tags = []
            meta_tags = soup.find_all('meta', attrs={'name': 'tag'})
            for tag in meta_tags:
                tag_content = tag.get('content')
                if tag_content:
                    tags.append(tag_content)
            
            # 要約の取得
            abstract = ""
            center_div = soup.find('div', id='center')
            if center_div:
                text_div = center_div.find('div', class_='text')
                if text_div:
                    h1_tag = text_div.find('h1')
                    h2_tag = text_div.find('h2')
                    if h1_tag and h2_tag:
                        abstract = text_div.text[text_div.text.index(h1_tag.text) + len(h1_tag.text):text_div.text.index(h2_tag.text)]
                        abstract = remove_newlines(abstract).replace('\n','<br>')
            
            # データに追加
            data.append([file_name, title, date, month, tags, abstract])
    
    # データフレームに変換
    df = pd.DataFrame(data, columns=['File Name', 'Title', 'Date', 'Month', 'Tags', 'Abstract'])
    return df