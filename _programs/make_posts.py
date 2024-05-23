import os
import re
import glob
from bs4 import BeautifulSoup
from modules import remove_newlines, replace_and_write, is_exist_modified


def analyze_code_blocks(html_code):
    """
    HTML内のコードブロックを分析し、置換すべき箇所と置換後のHTMLコードを作成する関数。
    
    Args:
        html_code: HTMLコンテンツの文字列
    
    Returns:
        old_codes (list): 置換対象のコードブロックのHTML文字列のリスト
        new_codes (list): コンテナとコピーボタンを追加した修正されたコードブロックのHTML文字列のリスト
    """
    
    # <pre class="hljs">タグを抽出し、編集
    soup = BeautifulSoup(html_code, 'html.parser')
    pre_tags = soup.find_all('pre', class_='hljs')
    old_codes = [str(p) for p in pre_tags]
    new_codes = []
    for index, pre_tag in enumerate(pre_tags):
        # 新しいdivタグを作成し、必要な要素を追加
        code_block_id = f'code-content{index}'
        new_div = soup.new_tag('div', **{'class': 'container'})
        inner_div = soup.new_tag('div', **{'id': code_block_id})
        copy_button_tag = soup.new_tag('button', **{'class': 'copy-button', 'data-clipboard-target': '#'+code_block_id})
        copy_button_tag.string = 'Copy'
        inner_div.append(copy_button_tag)
        inner_div.append(pre_tag)
        new_div.append(inner_div)
        new_codes += [str(new_div)]
    return (old_codes, new_codes)


def analyze_sections(html_code):
    """
    HTML内における「章」の記載を分析し、置換すべき箇所と置換後のHTMLコードを作成する関数。
    
    Args:
        html_code: HTMLコンテンツの文字列
    
    Returns:
        old_section_values (list): 置換対象のセクションのHTML文字列のリスト。
        new_section_values (list): 更新されたIDを含む修正されたセクションのHTML文字列のリスト。
        sections (str): サイドバーセクションリンクのHTMLコンテンツを表す文字列。
    """
    
    # セクションのid変更と左サイドバーにおけるリストの作成
    soup = BeautifulSoup(html_code, 'html.parser')
    section_tags = soup.find_all('h2')
    old_section_values = [str(s) for s in section_tags]
    new_section_values = []
    sections = []
    for index, section_tag in enumerate(section_tags):
        section_text = section_tag.get_text()
        new_section_values += [f"""<h2 id="section{index+1}">{section_text}</h2>"""]
        sections += [f"""<li><a href="#section{index+1}">{section_text}</a></li>"""]
    
    sections = '\n                        '.join(sections)
    return (old_section_values, new_section_values, sections)


def analyze_tags_info(html_code):
    """
    HTMLコード内の::tags{*}::の内容を分析し、置換すべき箇所と置換後のHTMLコードを作成する関数。
    
    Args:
        html_code (str): タグ情報を含むHTMLコード。
    
    Returns:
        old_codes (list): 置換対象のタグブロックの文字列のリスト。
        new_codes (list): 修正されたタグブロックのHTML文字列のリスト。
    """
    
    old_codes = ['::tags::'] # ここをmetaのtagに置き換える

    # ::tags{***}::を抽出
    old_codes += [re.findall(r'(::tags{.*?}::)', html_code, re.DOTALL)[0]] # ""::tags{" と "}::" を含める。ここを消す
    tags       =  re.findall(r'::tags{(.*?)}::', html_code, re.DOTALL)[0] # ""::tags{" と "}::" を含めない
    
    # tagsを出力用に整形
    new_code  = [f"<meta name=\"tag\" content=\"{tag}\">" for tag in tags.split(',')]
    new_code  = '\n    '.join(new_code)
    new_codes = [new_code, ""]
    
    return (old_codes, new_codes)


def analyze_img_info(html_code):
    """
    HTMLコード内の::img{*}::の内容を分析し、置換すべき箇所と置換後のHTMLコードを作成する関数。
    
    Args:
        html_code (str): 画像情報を含むHTMLコード。
    
    Returns:
        old_codes (list): 置換対象の画像ブロックの文字列のリスト。
        new_codes (list): 修正された画像ブロックのHTML文字列のリスト。
    """
    
    # ::img{***}::を抽出
    old_codes = re.findall(r'(::img{.*?}::)', html_code, re.DOTALL) # ""::img{" と "}::" を含める
    blocks    = re.findall(r'::img{(.*?)}::', html_code, re.DOTALL) # ""::img{" と "}::" を含めない
    
    info_list=[]
    height_list = []
    for block in blocks:
        # file要素を解析してリストに追加
        file_matches = re.findall(r'file{(.*?)}', block, re.DOTALL)
        file_info = remove_newlines(file_matches[0].replace(' ', ''))
        
        file_info = file_info.split(';')
        info_list += [[remove_newlines(s).split(':') for s in file_info if s != '']]
        
        # height要素を解析して文字列として定義
        height_match = re.search(r'height:\s*([\d\w]+);', block)
        if height_match:
            height_list.append(height_match.group(1))
    
    new_codes=[]
    for info, height in zip(info_list, height_list):
        new_code = """<div class="photo-list">"""
        for i_ in info:
            new_code += f"""<a href="../contents/img/{i_[0]}" data-lightbox="group" data-title="{i_[1]}" alt="{i_[1]}">
                                   <img src="../contents/img/{i_[0]}" height="{height}">
                                </a>
                             """
        
        new_code += """</div>"""
        new_codes += [new_code]
    
    return (old_codes, new_codes)


def analyze_stl_info(html_code):
    """
    HTMLコード内の::stl{*}::の内容を分析し、置換すべき箇所と置換後のHTMLコードを作成する関数。
    
    Args:
        html_code (str): 立体形状情報を含むHTMLコード。
    
    Returns:
        old_codes (list): 置換対象の立体形状ブロックの文字列のリスト。
        new_codes (list): 修正された立体形状ブロックのHTML文字列のリスト。
    """
    
    # ::stl{***}::を抽出
    old_codes = re.findall(r'(::stl{.*?}::)', html_code, re.DOTALL) # ""::stl{" と "}::" を含める
    blocks = re.findall(r'::stl{(.*?)}::', html_code, re.DOTALL) # ""::stl{" と "}::" を含めない
    
    info_list=[]
    for block in blocks:
        file_match = re.search(r'file:\s*(\w+\.stl);', block)
        camera_match = re.search(r'camera:\s*\[(.*?)\];', block)
        color_match = re.search(r'color:\s*(\w+);', block)
        # 抽出した情報をリストに追加
        if file_match and camera_match and color_match:
            file_name = os.path.splitext(file_match.group(1))[0]
            camera = camera_match.group(1)
            color = color_match.group(1)
            info_list.append([file_name, camera, color])
    
    new_codes=[]
    insert_code = """
                   <script>
                       const OBJ_INFO=["""
    for index, info in enumerate(info_list):
        file_name, camera, color = info
        insert_code += f"""
                           [
                               '../contents/stl/{file_name}.stl',
                               ['{file_name}-{index}'],
                               [[{camera}]],
                               [['{color}', 'white']],
                               [1, 1000]
                           ],
                       """
        
        new_codes += [f"""<div class="model-container" id="{file_name}-{index}"></div>"""]
    
    insert_code += """];
                    </script>
                    <script async src="https://unpkg.com/es-module-shims@1.3.6/dist/es-module-shims.js"></script>
                    <script src="../includes/display-3dmodel.js" type="module"></script>
                   """
    
    if not info_list:
        insert_code = ''
    
    return (old_codes, new_codes, insert_code)


def add_blank_links(html_code):
    """
    HTML内のリンクにtarget="_blank" rel="noopener noreferrer"を追加する関数。
    
    Args:
        html_code (str): HTMLコード。
    
    Returns:
        str: 更新されたHTMLコード。
    """
    
    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html_code, 'html.parser')
    
    # <a>タグをすべて取得
    a_tags = soup.find_all('a')
    
    # href属性の値をチェックしてtarget="_blank" rel="noopener noreferrer"を追加
    for a_tag in a_tags:
        if 'href' in a_tag.attrs:
            href_value = a_tag['href']
            if not href_value.startswith(('https://hitbug0.github.io/', '.', '#')):
                a_tag['target'] = '_blank'
                a_tag['rel'] = 'noopener noreferrer'
    
    # 更新されたHTMLを文字列として返す
    return str(soup)


def wrap_sns_elements(html):
    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # title属性が"YouTube video player"の<iframe>要素を抽出して、<div class="photo-list">で囲む
    for iframe in soup.find_all('iframe', title="YouTube video player"):
        div_tag = soup.new_tag('div', attrs={'class': 'photo-list'})
        iframe.wrap(div_tag)
    
    # class属性が"twitter-tweet"の<blockquote>要素を抽出して、<div class="photo-list">で囲む
    for blockquote in soup.find_all('blockquote', class_="twitter-tweet"):
        div_tag = soup.new_tag('div', attrs={'class': 'photo-list'})
        blockquote.wrap(div_tag)
    
    # 変更を適用したHTMLを返す
    return str(soup)


def extract_abstract(soup):
    description = ""
    start_tag_found = False
    for element in soup.find_all(['hr', 'h2', 'p']):
        if element.name == 'hr':
            start_tag_found = True
            continue
        if start_tag_found:
            if element.name == 'h2':
                break
            description += element.get_text()
    return description.replace('<br>','\n').replace('\n','\n        ')


def make_post(post_template, input_file_path, output_dir, language):
    """
    1つの記事HTMLファイルを作成する関数。
    
    Args:
        post_template (str): ポストのテンプレートHTMLコード。
        input_file_path (str): 入力HTMLファイルのパス。
        output_dir (str): 出力先ディレクトリのパス。
    """
    
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_html = f.read()
    
    file_name = os.path.basename(input_file_path) # ファイル名(拡張子あり)を取得
    print(f"    {file_name}")
    date = '-'.join(file_name.split('-')[:3]) # ファイル名から日付を取得
    
    # BeautifulSoupでパース
    soup = BeautifulSoup(input_html, 'html.parser')
    
    title = soup.find('body').find('h1').get_text() # <h1>タグで囲まれた文字列を抽出
    
    old_tag_codes, new_tag_codes = analyze_tags_info(input_html)
    old_code_blocks, new_code_blocks = analyze_code_blocks(input_html) # コードブロックの置き換え前後箇所特定
    old_section_codes, new_section_codes, sections = analyze_sections(input_html) # セクションのid変更と左サイドバーにおけるリストの作成
    
    body = str(soup.find('body')).replace('<body>', '').replace('</body>', '') # <body>タグで囲まれた範囲のコードを抽出
    old_img_codes, new_img_codes = analyze_img_info(body)
    old_stl_codes, new_stl_codes, insert_code  = analyze_stl_info(body)
    body += insert_code
    body = add_blank_links(body)
    body = wrap_sns_elements(body)
    
    hreflang = f"""
    <link rel="alternate" hreflang="ja" href="https://hitbug0.github.io/posts/{file_name}" />
    <link rel="alternate" hreflang="en" href="https://hitbug0.github.io/posts_en/{file_name}" />
    """

    thumbnail = """https://avatars.githubusercontent.com/u/166343381?v=4?s=400"""
    description = extract_abstract(soup)

    include_files_old = ['::hamburgermenufilename::', '::headerfilename::','::tagfilename::']
    include_files_new = [
        "./includes/hamburger-menu.html",
        "./includes/header.html",
        "./includes/tags-post.html"
    ]
    if language == "en":
        include_files_new = [
            "./includes/hamburger-menu-en.html",
            "./includes/header-en.html",
            "./includes/tags-post-en.html"
        ]


    replace_and_write(post_template, 
                     ['::hreflang::', '::language::', '::filename::', '::thumbnail::', '::body::','::date::','::description::','::title::', '::sections::','::directory::']     + include_files_old + old_tag_codes + old_code_blocks + old_section_codes + old_img_codes + old_stl_codes, 
                     [   hreflang,       language,       file_name,      thumbnail,       body,      date,      description,      title,       sections   ,DIRECTORY[language]] + include_files_new + new_tag_codes + new_code_blocks + new_section_codes + new_img_codes + new_stl_codes,
                     os.path.join(output_dir, file_name))


def make_posts(input_dir, output_dir, post_template, language):
    """
    複数の記事HTMLファイルを作成する関数。
    
    Args:
        input_dir (str): 入力ディレクトリのパス。
        output_dir (str): 出力先ディレクトリのパス。
        post_template (str): ポストのテンプレートHTMLコード。
    """
    count=0
    count_all = 0
    print(f"directory: {input_dir}")
    input_files = glob.glob(os.path.join(input_dir, '*.html')) # input_dir内のhtmlファイルを検索
    for input_file_path in input_files:
        count_all+=1
        if is_exist_modified(['_programs\\modules.py', '_programs\\make_posts.py', '_templates\\post-temp.html', '_posts_'+input_file_path.split('_posts_')[-1]]):
            make_post(post_template, input_file_path, output_dir, language)
            count+=1
    print(f"\nupdated {count}/{count_all} files.")
    print("="*30)


def main():
    """
    メイン処理。
    指定したディレクトリ内の全HTMLファイルを元に記事HTMLファイルを作成し、指定した出力先に出力する。
    """
    
    # テンプレートの読み込み
    with open('./_templates/post-temp.html', 'r', encoding='utf-8') as f:
        post_template = f.read()
    
    # カレントディレクトリの取得
    base_dir = os.getcwd()
    
    print("="*50)
    print("="*18+"  make posts  "+"="*18)
    print("="*50)

    # メイン処理
    make_posts(base_dir+"\\_posts_original",    base_dir+"\\posts",    post_template, "ja") # _posts_original -> posts
    make_posts(base_dir+"\\_posts_original_en", base_dir+"\\posts_en", post_template, "en") # in English
    make_posts(base_dir+"\\_posts_original\\for_debug", base_dir+"\\for_debug", post_template, "ja") # for_debug
    print("\n")



DIRECTORY = {
    "ja": "posts",
    "en": "posts_en"
}
main()
