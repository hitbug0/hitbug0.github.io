import os
import glob
from bs4 import BeautifulSoup

# temp.htmlを読み込み
with open('./_templates/post_template.html', 'r', encoding='utf-8') as f:
    temp_content_0 = f.read()

# _posts_original内のhtmlファイルを検索
base_dir = os.getcwd()
os.chdir(base_dir+"\\_posts_original")
html_files = glob.glob('*.html')

for file in html_files:
    temp_content = temp_content_0
    
    # htmlファイルを読み込み
    with open(file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # BeautifulSoupでパース
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # <pre class="hljs">タグを抽出し、編集
    pre_tags = soup.find_all('pre', class_='hljs')
    replace_pre = []
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
        
        # オリジナルの<pre class="hljs">を新しいdivで置き換える
        replace_pre += [(str(pre_tag), str(new_div))]


    soup = BeautifulSoup(html_content, 'html.parser')

    # <body>タグで囲まれた範囲のコードを抽出
    body_content = str(soup.find('body')).replace('<body>', '').replace('</body>', '')

    for r in replace_pre:
        body_content = body_content.replace(r[0], r[1])
    
    """
    # <script>タグで囲まれたコードを除外
    for script in soup.find_all('script'):
        script_content = str(script)
        body_content = body_content.replace(script_content, '')
    """
        
    # <a href="::tags::*">タグを抽出
    tags_tag = soup.find('a', href=lambda href: href and href.startswith('::tags::'))
    body_content = body_content.replace(str(tags_tag), '')

    # tagsの文字列を抽出し整形
    tags_values = tags_tag['href'].replace('::tags::', '').split(',')
    tags_metas  = ["<meta name=\"tag\" content=\""+tag+"\">" for tag in tags_values]
    tags_meta   = '\n'.join(tags_metas)

    # <h1>タグで囲まれた文字列を抽出
    title = soup.find('body').find('h1').get_text()

    # date
    date_value = '-'.join(file.split('-')[:3])


    # セクションのid変更と左サイドバーにおけるリストの作成
    section_list = []
    section_tags = soup.find_all('h2')
    for index, section_tag in enumerate(section_tags):
        section_id = section_tag['id']
        section_text = section_tag.get_text()
        section_values = [str(section_tags[index]), f"""<h2 id="section{index+1}">{section_text}</h2>"""]
        body_content = body_content.replace(section_values[0], section_values[1])
        section_list += [f"""<li><a href="#section{index+1}">{section_text}</a></li>"""]

    sections = '\n'.join(section_list)

    # 文字列をtempに挿入
    temp_content = temp_content.replace('::body::', body_content, 1)
    temp_content = temp_content.replace('::date::', date_value, 1)
    temp_content = temp_content.replace('::title::', title, 1)
    temp_content = temp_content.replace('::tags::', tags_meta, 1)
    temp_content = temp_content.replace('::sections::', sections, 1)

    # 出力
    os.chdir(base_dir+"\\posts")
    with open(f'{file}', 'w', encoding='utf-8') as f:
        f.write(temp_content)

    os.chdir(base_dir+"\\_posts_original")
    