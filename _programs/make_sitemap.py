import os
import glob
from datetime import datetime
from urllib.parse import quote

ROOT_URL = "https://hitbug0.github.io/"

def get_last_modified_time(file_path):
    # ファイルの最終更新日時を取得し、指定された形式の文字列に変換する
    modified_time = os.path.getmtime(file_path)
    return datetime.fromtimestamp(modified_time).isoformat().split(".")[0]+"+09:00"

def make_sitemap():
    sitemap = []
    
    # index.htmlのメタデータを取得
    lastmod = get_last_modified_time("index.html")
    sitemap.append(f"<url>\n  <loc>{ROOT_URL}</loc>\n  <lastmod>{lastmod}</lastmod>\n</url>\n")
    
    # postディレクトリ内のHTMLファイルのメタデータを取得
    for file_path in glob.glob("posts/*.html"):
        lastmod = get_last_modified_time(file_path)
        encoded_file_name = quote(os.path.basename(file_path))  # URLエンコーディング
        sitemap.append(f"<url>\n  <loc>{ROOT_URL}posts/{encoded_file_name}</loc>\n  <lastmod>{lastmod}</lastmod>\n</url>\n")
    
    # sitemap.xmlに書き込む
    with open('sitemap.xml', "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
        for url in sitemap:
            f.write(url)
        f.write("</urlset>")

# sitemap.xmlを生成する
make_sitemap()
