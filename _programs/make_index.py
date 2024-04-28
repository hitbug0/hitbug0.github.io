from collections import Counter
from urllib.parse import unquote
from modules import replace_and_write, collect_articles_info, format_tag, GOOGLE_AD

index_introduction = """
                    <h1 id="posts-title">今までの投稿</h1>
                    <p></p>
                    <hr/>
                    <p>脈絡なくいろんな技術について書いてます。<br>タグごとに古いもの順でまとめています。<br>
                        <a href="../sort-by-date.html">新着順の記事リストはこちら</a>
                    </p>
"""


def make_index_page():
    """
    メイン処理。
    このコードでやっていることは2つ。
        1. index-temp.htmlに記事ファイル情報を組み込むことでindex.htmlを作成する
        2. tags-temp.htmlに記事ファイル情報を組み込むことでtags-*.htmlを作成する
    """

    # postディレクトリ内で記事ファイルを検索し、記事の情報を集約する
    df = collect_articles_info()
    df.sort_values(by='Date', inplace=True, ascending=True) # 日付で昇順ソート
    df.reset_index(drop=True, inplace=True) # インデックスのリセット

    # タグのバリエーションを抽出する
    all_elements = [element for sublist in df["Tags"] for element in sublist] # タグについて、重複を許して1次元リスト化する
    element_counts = Counter(all_elements) # 要素の出現回数をカウント
    tags = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
    tag_info_list = [(tag[0], format_tag(tag[0]), unquote(tag[0]), tag[1]) for tag in tags] # [オリジナル, 記号がある場合は「-」に変更, 表示用にURLエンコードを元に戻したもの, 出現回数]

    # タグリスト(左サイドバー)のコードを作成する
    tags_for_index = [f"""<li><a href="#{tag_info[1]}">{tag_info[2]}</a></li>""" for tag_info in tag_info_list]
    tags_for_index = '\n    '.join(tags_for_index)
    tags_for_posts = [f"""<li><a href="../#{tag_info[1]}">{tag_info[2]}</a></li>""" for tag_info in tag_info_list]
    tags_for_posts = '\n    '.join(tags_for_posts)

    # indexページの冒頭に表示するタグボタンを作成する
    tag_buttons = [f"""<a class="tags" href="#{tag_info[1]}">{tag_info[2]}</a>""" for tag_info in tag_info_list]
    tag_buttons = '&nbsp;&nbsp;\n'.join(tag_buttons) + '\n<br>\n<br>\n'

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
    style = f"""<style>\n        #{', #'.join([tag_info[1] for tag_info in tag_info_list])}""".replace('%', '\%')
    style += """{scroll-margin-top: 65px;}\n    </style>"""

    # テンプレートの読み込み
    with open('./_templates/index-temp.html', 'r', encoding='utf-8') as f:
        index_template = f.read()
    with open('./_templates/tags-temp.html', 'r', encoding='utf-8') as f:
        tags_template = f.read()

    # 置換と出力
    replace_and_write(index_template, ['::URL::', '::articles::', '::style::'], ["", index_introduction + tag_buttons + article_info, style], 'index.html')
    replace_and_write(tags_template,  ['::listname::', '::sections::'],         ["Tags", tags_for_index], './includes/tags-index.html')
    replace_and_write(tags_template,  ['::listname::', '::sections::'],         ["Tags", tags_for_posts], './includes/tags-post.html')


make_index_page()