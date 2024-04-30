from collections import Counter
from urllib.parse import unquote
from modules import replace_and_write, collect_articles_info, format_tag, GOOGLE_AD


def make_tags(df, output_file_names):
    """
    メイン処理。
    tags-temp.htmlに記事ファイル情報を組み込むことでtags-*.htmlを作成する
    """

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

    # テンプレートの読み込み
    with open('./_templates/tags-temp.html', 'r', encoding='utf-8') as f:
        tags_template = f.read()

    # 置換と出力
    replace_and_write(tags_template,  ['::listname::', '::sections::'], ["Tags", tags_for_index], output_file_names[0])
    replace_and_write(tags_template,  ['::listname::', '::sections::'], ["Tags", tags_for_posts], output_file_names[1])


def make_index_page(df, config):
    """
    メイン処理。
    このコードでやっていることは2つ。
        1. index-temp.htmlに記事ファイル情報を組み込むことでindex.htmlを作成する
        2. tags-temp.htmlに記事ファイル情報を組み込むことでtags-*.htmlを作成する
    """
    df.sort_values(by='Date', inplace=True, ascending=True) # 日付で昇順ソート
    df.reset_index(drop=True, inplace=True) # インデックスのリセット

    # タグのバリエーションを抽出する
    all_elements = [element for sublist in df["Tags"] for element in sublist] # タグについて、重複を許して1次元リスト化する
    element_counts = Counter(all_elements) # 要素の出現回数をカウント
    tags = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
    tag_info_list = [(tag[0], format_tag(tag[0]), unquote(tag[0]), tag[1]) for tag in tags] # [オリジナル, 記号がある場合は「-」に変更, 表示用にURLエンコードを元に戻したもの, 出現回数]

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
                                <h3><a class="articles" href="../{config['article dir']}/{row['File Name']}.html">{row['Title']}</a></h3>
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

    # 置換と出力
    main_contents = config["introduction"] + tag_buttons + article_info
    replace_and_write(index_template, 
                      ['::tagfilename::',          '::headerfilename::',       '::language::',     '::URL::',     '::description::',    '::articles::', '::style::'], 
                      [config["tag file name"][0], config["header file name"], config["language"], config["url"], config["description"], main_contents,  style], 
                      config["output file name"])



INTRODUCTION_JA ="""
                    <h1 id="posts-title">今までの投稿</h1>
                    <p></p>
                    <hr/>
                    <p>脈絡なくいろんな技術について書いてます。<br>タグごとに古いもの順でまとめています。<br><br>
                        <a href="../sort-by-date.html">新着順の記事リストはこちら</a><br><br>
                        <a href="../index-en.html">Click here for articles in English</a><br><br>
                    </p>"""

INTRODUCTION_EN ="""
                    <h1 id="posts-title">Previous Posts</h1>
                    <p></p>
                    <hr/>
                    <p>I write about various technologies without any particular context.<br>They are organized by tags in chronological order.<br><br>
                        <a href="../sort-by-date-en.html">Click here for a list of articles in descending order of publication date</a><br><br>
                        <a href="/">日本語版はこちら</a><br><br>
                    </p>"""

CONFIG = {
    "ja": {
        "language":      "ja",
        "url":           "",
        "description":   "脈絡なくいろんな技術について書いてます。",
        "introduction":  INTRODUCTION_JA,
        "tag file name": ['./includes/tags-index.html', './includes/tags-post.html'],
        "header file name": './includes/header.html',
        "article dir":    "posts",
        "output file name": 'index.html'
    },
    "en": {
        "language":      "en",
        "url":           "index-en.html",
        "description":   "I write about various technologies without any particular context.",
        "introduction":  INTRODUCTION_EN,
        "tag file name": ['./includes/tags-index-en.html', './includes/tags-post-en.html'],
        "header file name": './includes/header-en.html',
        "article dir":    "posts_en",
        "output file name": 'index-en.html'
    },
}


print("="*50)
print("="*18+"  make index  "+"="*18)
print("="*50)
for lang in ["ja", "en"]:
    search_key = CONFIG[lang]["article dir"]+"/20*.html"
    df = collect_articles_info(search_key)
    make_tags(df, CONFIG[lang]["tag file name"])
    make_index_page(df, CONFIG[lang])

print("\n")

