import os
import glob
from datetime import datetime
from urllib.parse import quote
from modules import get_modified_time

ROOT_URL = "https://hitbug0.github.io/"


def add_code(sitemap, file, url):
    lastmod = get_modified_time(file).split(".")[0]+"+09:00" # 最終更新日時を取得
    sitemap.append(f"<url>\n  <loc>{url}</loc>\n  <lastmod>{lastmod}</lastmod>\n</url>\n") # sitemap.xmlへの記載内容に追加
    return sitemap


def make_sitemap():
    """
    メイン処理。
    sitemap.xmlに記載すべきファイルの情報を収集し、sitemap.xmlの形式に整え、出力する。
    """
    # index.htmlに対する処理
    sitemap = add_code([], "index.html", ROOT_URL)
    
    # 他のHTMLファイルに対する処理
    files = ["sort-by-date.html", "index-en.html", "sort-by-date-en.html"] + glob.glob("posts/20*.html") + glob.glob("posts_en/20*.html")
    for file in files:
        url = ROOT_URL + quote(file.replace('\\','/'))  # URLエンコーディング
        sitemap = add_code(sitemap, file, url)
    
    # sitemap.xmlを出力する
    with open('sitemap.xml', "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
        for url in sitemap:
            f.write(url)
        f.write("</urlset>")


make_sitemap()
