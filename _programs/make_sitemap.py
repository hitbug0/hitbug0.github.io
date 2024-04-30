import os
import glob
from datetime import datetime
from urllib.parse import quote

ROOT_URL = "https://hitbug0.github.io/"


def get_last_modified_time(file_path):
    """
    ファイルの最終更新日時を取得し、指定された形式の文字列に変換する。
    
    Args:
        file_path: ファイルのパス。
        
    Returns:
        formatted_time: file_pathで指定したファイルの最終更新日時を指定された形式に整形した文字列。
    """
    modified_time = os.path.getmtime(file_path)
    formatted_time = datetime.fromtimestamp(modified_time).isoformat().split(".")[0]+"+09:00"
    return formatted_time


def make_sitemap():
    """
    メイン処理。
    sitemap.xmlに記載すべきファイルの情報を収集し、sitemap.xmlの形式に整え、出力する。
    """
    files = ["index.html", "sort-by-date.html", "index-en.html", "sort-by-date-en.html"] + glob.glob("posts/*.html") + glob.glob("posts-en/*.html")

    # postディレクトリ内のHTMLファイルに対する処理
    sitemap = []
    for file in files:
        lastmod = get_last_modified_time(file) # 最終更新日時を取得
        encoded_file_name = quote(os.path.basename(file))  # URLエンコーディング
        sitemap.append(f"<url>\n  <loc>{ROOT_URL}posts/{encoded_file_name}</loc>\n  <lastmod>{lastmod}</lastmod>\n</url>\n") # sitemap.xmlへの記載内容に追加
    
    # sitemap.xmlを出力する
    with open('sitemap.xml', "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
        for url in sitemap:
            f.write(url)
        f.write("</urlset>")


make_sitemap()
