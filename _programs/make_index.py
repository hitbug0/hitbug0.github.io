import os
import glob
import pandas as pd
from itertools import chain
from bs4 import BeautifulSoup
from urllib.parse import unquote
from modules import remove_newlines, replace_and_write


GOOGLE_AD = """
                <script async 
                    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5830432592137126"
                    crossorigin="anonymous">
                </script>
                <!-- disp1 -->
                <ins class="adsbygoogle"
                    style="display:block"
                    data-ad-client="ca-pub-5830432592137126"
                    data-ad-slot="4558728851"
                    data-ad-format="auto"
                    data-full-width-responsive="true">
                </ins>
                <script>
                    (adsbygoogle = window.adsbygoogle || []).push({});
                </script>
"""


def collect_articles_info():
    # 記事の情報を集約する
    data = []
    for file_path in glob.glob("posts/*.html"):
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
    df.sort_values(by='Date', inplace=True) # タイトルで昇順ソート
    df.reset_index(drop=True, inplace=True) # インデックスのリセット
    return df


def main():
    df = collect_articles_info() # 記事の情報を集約する

    # タグのバリエーションを抽出
    tags = sorted(list(set(list(chain(*list(df['Tags'])))))) # 全タグを1次元のリストにし、重複を除外する

    # タグごとの記事リスト作成
    # 記事数が増えたらサイトの作りを変えるつもり
    tags_at_top = ""
    sections_for_index = ""
    sections_for_posts = ""
    article_info = ""
    for tag in tags:
        tags_at_top += f"""<a class="tags" href="#{tag}">{unquote(tag)}</a>&nbsp;&nbsp;\n"""

        tag_disp = unquote(tag) # URLエンコードを元に戻す
        sections_for_index += f"""<li><a href="#{tag}">{tag_disp}</a></li>\n"""
        sections_for_posts += f"""<li><a href="../#{tag}">{tag_disp}</a></li>\n"""
        
        # テンプレートに組み込むコードを作成する
        filtered_df = df[df['Tags'].apply(lambda tags_: tag in tags_)] # tagが付いた記事のレコードだけを抽出する
        article_info += f"""<br><h1 id="{tag}">{tag_disp}（{len(filtered_df)} 件）</h1>\n"""
        
        for index, row in filtered_df.iterrows():
            article_info += f"""<hr class="articles">
                                <div class="metadata-date">{row['Date']}</div>
                                <h3><a class="articles" href="../posts/{row['File Name']}.html">{row['Title']}</a></h3>
                                <div class="metadata-tags">
                            """
            # タグを追加
            for tag in row['Tags']:
                article_info += f"""<a class="tags" href="#{tag}">{unquote(tag)}</a>&nbsp;&nbsp;\n"""

            article_info += f"""</div>\n<div class="metadata-abstract"><p>\n{row['Abstract']}\n</p></div>"""

        article_info += GOOGLE_AD
        article_info += "<br><br>"


    style = f"""<style>#{', #'.join(tags)}""".replace('%', '\%')
    style += """{scroll-margin-top: 65px;}</style>"""

    # テンプレートの読み込み
    with open('./_templates/index-temp.html', 'r', encoding='utf-8') as f:
        index_template = f.read()

    with open('./_templates/tags-temp.html', 'r', encoding='utf-8') as f:
        tags_template = f.read()

    replace_and_write(index_template, ['::articles::', '::style::'], [tags_at_top + article_info, style], 'index.html')
    replace_and_write(tags_template,  ['::sections::'], [sections_for_index], './includes/tags-index.html')
    replace_and_write(tags_template,  ['::sections::'], [sections_for_posts], './includes/tags-post.html')

main()