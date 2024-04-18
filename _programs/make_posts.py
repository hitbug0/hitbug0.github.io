import os
import re
import glob
from bs4 import BeautifulSoup


def extract_img_info(html_code):
    img_info_list = []
    img_height_list = []
    
    # 正規表現を使用して::img{***}::を抽出
    img_blocks = re.findall(r'::img{(.*?)}::', html_code, re.DOTALL)
    
    img_info_list=[]
    for block in img_blocks:
        # file要素を解析してリストに追加
        file_matches = re.findall(r'file{(.*?)}', block, re.DOTALL)
        file_info = remove_newlines(file_matches[0].replace(' ', ''))
        
        file_info = file_info.split(';')
        img_info_list += [[remove_newlines(s).split(':') for s in file_info if s != '']]
        
        # height要素を解析して文字列として定義
        height_match = re.search(r'height:\s*([\d\w]+);', block)
        if height_match:
            img_height_list.append(height_match.group(1))
    
    return img_info_list, img_height_list


def extract_stl_info(html_code):
    stl_info_list = []
    stl_height_list = []
    
    # 正規表現を使用して::stl{***}::を抽出
    stl_blocks = re.findall(r'::stl{(.*?)}::', html_code, re.DOTALL)
    
    stl_info_list=[]
    for block in stl_blocks:
        file_match = re.search(r'file:\s*(\w+\.stl);', block)
        camera_match = re.search(r'camera:\s*\[(.*?)\];', block)
        color_match = re.search(r'color:\s*(\w+);', block)
        # 抽出した情報をリストに追加
        if file_match and camera_match and color_match:
            file_name = os.path.splitext(file_match.group(1))[0]
            camera = camera_match.group(1)
            color = color_match.group(1)
            stl_info_list.append([file_name, camera, color])
    
    return stl_info_list


def replace_img_code(html_code, img_info_list, img_height_list):
    replace_code_list=[]
    for img_info, img_height in zip(img_info_list, img_height_list):
        replace_temp = """<div class="photo-list">"""
        for i_ in img_info:
            replace_temp += f"""<a href="../contents/img/{i_[0]}"  data-lightbox="group" data-title="{i_[1]}" alt="">
                                   <img src="../contents/img/{i_[0]}" height="{img_height}">
                               </a>
                            """
        
        replace_temp += """</div>"""
        replace_code_list += [replace_temp]
    
    # 正規表現を使用して::img{***}::を抽出
    img_blocks = re.findall(r'(::img{.*?}::)', html_code, re.DOTALL)
    
    for replace_code,img_block in zip(replace_code_list,img_blocks):
        html_code = html_code.replace(img_block, replace_code)
    
    return html_code


def replace_stl_code(html_code, stl_info_list):
    replace_code_list=[]
    insert_code = """
                   <script>
                       const OBJ_INFO=["""
    for index, stl_info in enumerate(stl_info_list):
        file_name, camera, color = stl_info
        insert_code += f"""
                           [
                               '../contents/stl/{file_name}.stl',
                               ['{file_name}-{index}'],
                               [[{camera}]],
                               [['{color}', 'white']],
                               [1, 1000]
                           ],
                       """
        
        replace_code_list += [f"""<div class="model-container" id="{file_name}-{index}"></div>"""]
    
    insert_code += """];
                    </script>
                    <script async src="https://unpkg.com/es-module-shims@1.3.6/dist/es-module-shims.js"></script>
                    <script src="../includes/display-3dmodel.js" type="module"></script>
    """
    
    # 正規表現を使用して::stl{***}::を抽出
    stl_blocks = re.findall(r'(::stl{.*?}::)', html_code, re.DOTALL)
    
    for replace_code,stl_block in zip(replace_code_list,stl_blocks):
        html_code = html_code.replace(stl_block, replace_code)
    
    return (html_code, insert_code)



# 改行コードを除外する関数(冒頭と末尾のみ除外。中間は残す)
def remove_newlines(text):
    return re.sub(r"(^\n+)|(\n+$)", "", text)


def add_blank_links(html_code):
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

    img_info_list, img_height = extract_img_info(body_content)
    stl_info_list = extract_stl_info(body_content)
    
    # 置換処理
    body_content = replace_img_code(body_content, img_info_list, img_height)
    body_content, insert_code = replace_stl_code(body_content, stl_info_list)
    body_content += insert_code
    
    body_content = add_blank_links(body_content)

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




