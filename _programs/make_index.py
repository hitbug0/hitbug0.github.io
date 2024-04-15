import os
import re
import glob
import pandas as pd
from itertools import chain
from bs4 import BeautifulSoup
from urllib.parse import unquote

# 改行コードを除外する関数(冒頭と末尾のみ除外。中間は残す)
def remove_newlines(text):
    return re.sub(r"(^\n+)|(\n+$)", "", text)

# ファイルパスの取得
file_paths = glob.glob("posts/*.html")

# データを格納するためのリスト
data = []

# ファイルごとに処理
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        # ファイル名を取得
        file_name = os.path.basename(file_path).rsplit('.', 1)[0]
        date = ' - '.join(file_name.split('-')[:3])
        
        # BeautifulSoupを用いてHTMLを解析
        soup = BeautifulSoup(file, 'html.parser')
        
        title = soup.find('div', id='center').find('h1').get_text()

        # タグの取得
        tags = []
        meta_tags = soup.find_all('meta', attrs={'name': 'tag'})
        for tag in meta_tags:
            tag_content = tag.get('content')
            if tag_content:
                tags.append(tag_content)
        
        # アブストラクトの取得
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
df.sort_values(by='Date', inplace=True) # タイトルで昇順ソート
df.reset_index(drop=True, inplace=True) # インデックスのリセット
# print(df) # 表示

# タグのバリエーションを抽出
tags = sorted(list(set(list(chain(*list(df['Tags']))))))


# タグごとの記事リスト作成
# 記事数が増えたら作りを変える
titles_in_tag = ""
section_list1 = ""
section_list2 = ""
tags_at_top   = ""
for tag in tags:
    tag_disp = tag
    if '%' in tag: # URLエンコードを元に戻す
        tag_disp = unquote(tag_disp)
    
    tags_at_top += f"""<a class="tags" href="#{tag}">{unquote(tag)}</a>&nbsp;&nbsp;
                    """

    filtered_df = df[df['Tags'].apply(lambda tags_: tag in tags_)] # このタグが付いた記事のレコードだけを抽出する
    
    section_list1 += f"""<li><a href="#{tag}">{tag_disp}</a></li>
                      """
    section_list2 += f"""<li><a href="../#{tag}">{tag_disp}</a></li>
                      """
    
    # テンプレートに組み込むコードを作成する
    titles_in_tag += f"""<br><br><br><h1 id="{tag}">{tag_disp}（{len(filtered_df)} 件）</h1>
                      """
    
    for index, row in filtered_df.iterrows():
        titles_in_tag += f"""<hr class="articles">
                            <div class="metadata-date">{row['Date']}</div>
                            <h3><a class="articles" href="../posts/{row['File Name']}.html">{row['Title']}</a></h3>
                            <div class="metadata-tags">
                        """
        # タグを追加
        for tag in row['Tags']:
            titles_in_tag += f"""<a class="tags" href="#{tag}">{unquote(tag)}</a>&nbsp;&nbsp;
                            """

        titles_in_tag += f"""</div>
                            <div class="metadata-abstract"><p>
                                {row['Abstract']}
                            </p></div>
                        """



    titles_in_tag += "<br><br>"


style = f"""<style>#{', #'.join(tags)}""".replace('%', '\%')
style += """{scroll-margin-top: 65px;}</style>"""

# temp.htmlを読み込み
with open('./_templates/index_template.html', 'r', encoding='utf-8') as f:
    temp_content = f.read()

# テンプレートへ組み込む
temp_content = temp_content.replace('::articles::', tags_at_top+titles_in_tag, 1)
temp_content = temp_content.replace('::style::', style, 1)

# 出力
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(temp_content)


# temp.htmlを読み込み
with open('./_templates/tags_template.html', 'r', encoding='utf-8') as f:
    temp_content = f.read()

temp_content1 = temp_content.replace('::sections::', section_list1, 1)
temp_content2 = temp_content.replace('::sections::', section_list2, 1)

# 出力
with open('./includes/tags.html', 'w', encoding='utf-8') as f:
    f.write(temp_content1)

with open('./includes/tags-post.html', 'w', encoding='utf-8') as f:
    f.write(temp_content2)

