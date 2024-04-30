from collections import Counter
from urllib.parse import unquote
from modules import replace_and_write, collect_articles_info, format_tag, GOOGLE_AD



def make_months(df):
    """
    メイン処理。
    このコードでやっていることは2つ。
        1. index-temp.htmlに記事ファイル情報を組み込むことでsort-by-date.htmlを作成する
        2. tags-temp.htmlに記事ファイル情報を組み込むことでtags-*.htmlを作成する
    """
    df.sort_values(by='Date', inplace=True, ascending=False) # 日付で降順ソート
    df.reset_index(drop=True, inplace=True) # インデックスのリセット
    
    # monthのバリエーションを抽出する
    element_counts = Counter(list(df["Month"])) # 要素の出現回数をカウント
    months = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
    month_info_list = [(month[0], 'posts-'+month[0].replace(' ',''), month[1]) for month in months] # [オリジナル, 空白無しアルファベット始まり, 出現回数]
    
    # monthリスト(左サイドバー)のコードを作成する
    months_for_sortbydate = [f"""<li><a href="#{month_info[1]}">{month_info[0]}</a></li>""" for month_info in month_info_list]
    months_for_sortbydate = '\n    '.join(months_for_sortbydate)
    
    # テンプレートの読み込み
    with open('./_templates/tags-temp.html', 'r', encoding='utf-8') as f:
        tags_template = f.read()
    
    # 置換と出力
    replace_and_write(tags_template, ['::listname::', '::sections::'], ['Months', months_for_sortbydate], './includes/month.html')



def make_sortbydate_page(df, config):
    """
    メイン処理。
    このコードでやっていることは2つ。
        1. index-temp.htmlに記事ファイル情報を組み込むことでsort-by-date.htmlを作成する
        2. tags-temp.htmlに記事ファイル情報を組み込むことでtags-*.htmlを作成する
    """
    
    df.sort_values(by='Date', inplace=True, ascending=False) # 日付で降順ソート
    df.reset_index(drop=True, inplace=True) # インデックスのリセット
    
    # monthのバリエーションを抽出する
    element_counts = Counter(list(df["Month"])) # 要素の出現回数をカウント
    months = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
    month_info_list = [(month[0], 'posts-'+month[0].replace(' ',''), month[1]) for month in months] # [オリジナル, 空白無しアルファベット始まり, 出現回数]
    
    # sortbydateページの冒頭に表示するmonthボタンを作成する
    month_buttons = [f"""<a class="tags" href="#{month_info[1]}">{month_info[0]}</a>""" for month_info in month_info_list]
    month_buttons = '&nbsp;&nbsp;\n'.join(month_buttons) + '\n<br>\n<br>\n'
    
    # monthごとの記事リスト（sortbydateページのメインの内容）を作成する
    article_info = GOOGLE_AD
    for month_info in month_info_list:
        article_info += f"""<br><h1 id="{month_info[1]}">{month_info[0]}（{month_info[2]} 件）</h1>\n"""
        
        # 記事毎のコードを作成
        filtered_df = df[df['Month']==month_info[0]] # このmonthの記事のレコードだけを抽出する
        for _, row in filtered_df.iterrows(): 
            article_info += f"""<hr class="articles">
                                <div class="metadata-date">{row['Date']}</div>
                                <h3><a class="articles" href="../{config['article dir']}/{row['File Name']}.html">{row['Title']}</a></h3>
                                <div class="metadata-tags">
                            """
            
            for t_ in row['Tags']: # その記事に含まれるタグの表示
                article_info += f"""<a class="tags" href="..{config['top page url']}#{format_tag(t_)}">{unquote(t_)}</a>&nbsp;&nbsp;\n"""
            
            article_info += f"""</div>\n<div class="metadata-abstract"><p>\n{row['Abstract']}\n</p></div>""" # 要約
        
        article_info += GOOGLE_AD
        article_info += "<br><br>"
    
    # 各タグ欄(各章)へのリンク押下時の挙動を設定するstyleコードの作成
    style = f"""<style>\n        #{', #'.join([month_info[1] for month_info in month_info_list])}""".replace('%', '\%')
    style += """{scroll-margin-top: 65px;}\n    </style>"""
    
    # テンプレートの読み込み
    with open('./_templates/index-temp.html', 'r', encoding='utf-8') as f:
        sortbydate_template = f.read()
    
    # 置換と出力
    main_contents = config["introduction"] + month_buttons + article_info
    replace_and_write(sortbydate_template, 
                      ['::tagfilename::',       '::language::',     '::URL::',                  '::headerfilename::',       '::description::',     '::description::',    '::articles::', '::style::'], 
                      ['./includes/month.html', config["language"], config["output file name"], config["header file name"], config["description"], config["description"], main_contents,  style], 
                      config["output file name"])


INTRODUCTION_JA = """
                    <h1 id="posts-title">新着順の記事リスト</h1>
                    <p></p>
                    <hr/>
                    <p>全記事を新着順で並べています。<br>
                        <a href="../">タグごとにまとめたページはこちら</a>
                    </p>
"""
INTRODUCTION_EN = """
                    <h1 id="posts-title">Latest Articles</h1>
                    <p></p>
                    <hr/>
                    <p>All articles sorted by date here.<br><br>
                        <a href="../index-en.html">Browse by tag</a><br><br>
                    </p>
"""


CONFIG = {
    "ja": {
        "language":      "ja",
        "url":           "",
        "description":   "脈絡なくいろんな技術について書いてます。",
        "introduction":  INTRODUCTION_JA,
        "tag file name": ['./includes/tags-index.html', './includes/tags-post.html'],
        "header file name": './includes/header.html',
        "article dir":    "posts",
        "output file name": 'sort-by-date.html',
        "top page url": ""
    },
    "en": {
        "language":      "en",
        "url":           "index-en.html",
        "description":   "I write about various technologies without any particular context.",
        "introduction":  INTRODUCTION_EN,
        "tag file name": ['./includes/tags-index-en.html', './includes/tags-post-en.html'],
        "header file name": './includes/header-en.html',
        "article dir":    "posts_en",
        "output file name": 'sort-by-date-en.html',
        "top page url": "/index-en.html"
    },
}

print("="*50)
print("="*14+"  make sort-by-date   "+"="*14)
print("="*50)
for lang in ["ja", "en"]:
    search_key = CONFIG[lang]["article dir"]+"/20*.html"
    df = collect_articles_info(search_key)
    make_months(df)
    make_sortbydate_page(df, CONFIG[lang])


print("\n")
