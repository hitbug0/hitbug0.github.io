import os
import glob
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup
from urllib.parse import unquote
from modules import remove_newlines, replace_and_write


GOOGLE_AD = """"""


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
    df.sort_values(by='Date', inplace=True, ascending=False) # 日付で降順ソート
    df.reset_index(drop=True, inplace=True) # インデックスのリセット
    return df


def make_sortbydate_page():
    """
    メイン処理。
    このコードでやっていることは2つ。
        1. sort-by-date-temp.htmlに記事ファイル情報を組み込むことでsort-by-date.htmlを作成する
        2. tags-temp.htmlに記事ファイル情報を組み込むことでtags-*.htmlを作成する
    """
    
    # postディレクトリ内で記事ファイルを検索し、記事の情報を集約する
    df = collect_articles_info()
    
    # monthのバリエーションを抽出する
    element_counts = Counter(list(df["Month"])) # 要素の出現回数をカウント
    months = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
    month_info_list = [(month[0], 'posts-'+month[0].replace(' ',''), month[1]) for month in months] # [オリジナル, 空白無しアルファベット始まり, 出現回数]
    
    # monthリスト(左サイドバー)のコードを作成する
    months_for_sortbydate = [f"""<li><a href="#{month_info[1]}">{month_info[0]}</a></li>""" for month_info in month_info_list]
    months_for_sortbydate = '\n'.join(months_for_sortbydate)
    
    # sortbydateページの冒頭に表示するmonthボタンを作成する
    month_buttons = [f"""<a class="tags" href="#{month_info[1]}">{month_info[0]}</a>""" for month_info in month_info_list]
    month_buttons = '&nbsp;&nbsp;\n'.join(month_buttons)
    
    # monthごとの記事リスト（sortbydateページのメインの内容）を作成する
    article_info = GOOGLE_AD
    for month_info in month_info_list:
        article_info += f"""<br><h1 id="{month_info[1]}">{month_info[0]}（{month_info[2]} 件）</h1>\n"""
        
        # 記事毎のコードを作成
        filtered_df = df[df['Month']==month_info[0]] # このmonthの記事のレコードだけを抽出する
        for _, row in filtered_df.iterrows(): 
            article_info += f"""<hr class="articles">
                                <div class="metadata-date">{row['Date']}</div>
                                <h3><a class="articles" href="../posts/{row['File Name']}.html">{row['Title']}</a></h3>
                                <div class="metadata-tags">
                            """
            
            for t_ in row['Tags']: # その記事に含まれるタグの表示
                article_info += f"""<a class="tags" href="../#{format_tag(t_)}">{unquote(t_)}</a>&nbsp;&nbsp;\n"""
            
            article_info += f"""</div>\n<div class="metadata-abstract"><p>\n{row['Abstract']}\n</p></div>""" # 要約
        
        article_info += GOOGLE_AD
        article_info += "<br><br>"
    
    # 各タグ欄(各章)へのリンク押下時の挙動を設定するstyleコードの作成
    style = f"""<style>#{', #'.join([month_info[1] for month_info in month_info_list])}""".replace('%', '\%')
    style += """{scroll-margin-top: 65px;}</style>"""
    
    # テンプレートの読み込み
    with open('./_templates/sort-by-date-temp.html', 'r', encoding='utf-8') as f:
        sortbydate_template = f.read()
    with open('./_templates/months-temp.html', 'r', encoding='utf-8') as f:
        months_template = f.read()
    
    # 置換と出力
    replace_and_write(sortbydate_template, ['::articles::', '::style::'], [month_buttons + article_info, style], 'sort-by-date.html')
    replace_and_write(months_template,  ['::sections::'],              [months_for_sortbydate], './includes/month.html')




make_sortbydate_page()