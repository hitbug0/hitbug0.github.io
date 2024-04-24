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
    より具体的には、postディレクトリ内のhtmlファイルを解析し、各ファイル(=各記事)の中からindex.html等で表示すべき情報を抽出する関数。
    Returns:
        df: 記事情報をまとめたpandas DataFrame。 
    """
    data = []
    for file_path in glob.glob("posts/20*.html"):
        file_name = os.path.splitext(os.path.basename(file_path))[0] # ファイル名を取得
        date = ' - '.join(file_name.split('-')[:3]) # ファイル名から日付を取得
        
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
            data.append([file_name, title, date, tags, abstract])

    # データフレームに変換
    df = pd.DataFrame(data, columns=['File Name', 'Title', 'Date', 'Tags', 'Abstract'])
    df.sort_values(by='Date', inplace=True, ascending=False) # 日付で昇順ソート
    df.reset_index(drop=True, inplace=True) # インデックスのリセット
    return df


def make_index_page():
    """
    メイン処理。
    このコードでやっていることは2つ。
        1. index-temp.htmlに記事ファイル情報を組み込むことでindex.htmlを作成する
        2. tags-temp.htmlに記事ファイル情報を組み込むことでtags-*.htmlを作成する
    """

    # postディレクトリ内で記事ファイルを検索し、記事の情報を集約する
    df = collect_articles_info()

    # タグのバリエーションを抽出する
    all_elements = [element for sublist in df["Tags"] for element in sublist] # タグについて、重複を許して1次元リスト化する
    element_counts = Counter(all_elements) # 要素の出現回数をカウント
    tags = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
    tag_info_list = [(tag[0], format_tag(tag[0]), unquote(tag[0]), tag[1]) for tag in tags] # [オリジナル, 記号がある場合は「-」に変更, 表示用にURLエンコードを元に戻したもの, 出現回数]

    # タグリスト(左サイドバー)のコードを作成する
    tags_for_index = [f"""<li><a href="#{tag_info[1]}">{tag_info[2]}</a></li>""" for tag_info in tag_info_list]
    tags_for_index = '\n'.join(tags_for_index)
    tags_for_posts = [f"""<li><a href="../#{tag_info[1]}">{tag_info[2]}</a></li>""" for tag_info in tag_info_list]
    tags_for_posts = '\n'.join(tags_for_posts)

    # indexページの冒頭に表示するタグボタンを作成する
    tag_buttons = [f"""<a class="tags" href="#{tag_info[1]}">{tag_info[2]}</a>""" for tag_info in tag_info_list]
    tag_buttons = '&nbsp;&nbsp;\n'.join(tag_buttons)

    # タグごとの記事リスト（indexページのメインの内容）を作成する
    article_info = GOOGLE_AD
    for tag_info in tag_info_list:
        article_info += f"""<br><h1 id="{tag_info[1]}">{tag_info[2]}（{tag_info[3]} 件）</h1>\n"""
        
        # 記事毎のコードを作成
        filtered_df = df[df['Tags'].apply(lambda tags_: tag_info[0] in tags_)] # このtagが付いた記事のレコードだけを抽出する
        for _, row in filtered_df.iterrows(): 
            article_info += f"""<hr class="articles">
                                <div class="metadata-date">{row['Date']}</div>
                                <h3><a class="articles" href="../posts/{row['File Name']}.html">{row['Title']}</a></h3>
                                <div class="metadata-tags">
                            """
            
            for t_ in row['Tags']: # その記事に含まれるタグの表示
                article_info += f"""<a class="tags" href="#{format_tag(t_)}">{unquote(t_)}</a>&nbsp;&nbsp;\n"""

            article_info += f"""</div>\n<div class="metadata-abstract"><p>\n{row['Abstract']}\n</p></div>""" # 要約

        article_info += GOOGLE_AD
        article_info += "<br><br>"

    # 各タグ欄(各章)へのリンク押下時の挙動を設定するstyleコードの作成
    style = f"""<style>#{', #'.join([tag_info[1] for tag_info in tag_info_list])}""".replace('%', '\%')
    style += """{scroll-margin-top: 65px;}</style>"""

    # テンプレートの読み込み
    with open('./_templates/index-temp.html', 'r', encoding='utf-8') as f:
        index_template = f.read()
    with open('./_templates/tags-temp.html', 'r', encoding='utf-8') as f:
        tags_template = f.read()

    # 置換と出力
    replace_and_write(index_template, ['::articles::', '::style::'], [tag_buttons + article_info, style], 'index.html')
    replace_and_write(tags_template,  ['::sections::'],              [tags_for_index], './includes/tags-index.html')
    replace_and_write(tags_template,  ['::sections::'],              [tags_for_posts], './includes/tags-post.html')


make_index_page()