import os
import re
import glob
from bs4 import BeautifulSoup
from modules import replace_and_write

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

def add_ad_to_post(file_path):
    """
    1つの記事HTMLファイルを作成する関数。
    
    Args:
        file_path (str): HTMLファイルのパス。
    """
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    center = soup.find("div", id="center")
    h2_tags = re.findall(r'(<h2.*?</h2>)', str(center), re.DOTALL)
    
    replace_and_write(html, h2_tags, 
                     [GOOGLE_AD + h2_tag for h2_tag in h2_tags],
                     file_path)

    

def add_ad_to_posts(directory):
    """
    複数の記事HTMLファイルを作成する関数。
    
    Args:
        directory (str): ディレクトリのパス。
    """
    
    files = glob.glob(os.path.join(directory, '*.html')) # input_dir内のhtmlファイルを検索
    for file_path in files:
        # htmlファイルを読み込み
        add_ad_to_post(file_path)


def main():
    """
    メイン処理。
    指定したディレクトリ内の全HTMLファイルを書き換える。
    """
    
    # カレントディレクトリの取得
    base_dir = os.getcwd()
    
    # メイン処理
    add_ad_to_posts(base_dir+"\\posts") # posts
    add_ad_to_posts(base_dir+"\\for_debug") # for_debug


main()
