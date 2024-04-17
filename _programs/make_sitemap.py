import os
from datetime import datetime
from urllib.parse import quote

ROOT_URL = "https://hitbug0.github.io/"

def get_last_modified_time(file_path):
    # ファイルの最終更新日時を取得し、指定された形式の文字列に変換する
    modified_time = os.path.getmtime(file_path)
    formatted_time = datetime.fromtimestamp(modified_time).isoformat()
    return formatted_time.split(".")[0]+"+09:00"  # 秒の小数点以下を切り捨てる

def generate_sitemap():
    directory = os.getcwd()
    sitemap = []
    
    # index.htmlのメタデータを取得
    index_path = os.path.join(directory, "index.html")
    index_lastmod = get_last_modified_time(index_path)
    sitemap.append(f"<url>\n  <loc>{ROOT_URL}</loc>\n  <lastmod>{index_lastmod}</lastmod>\n</url>\n")
    
    # postディレクトリ内のHTMLファイルのメタデータを取得
    post_dir = os.path.join(directory, "posts")
    for file_name in os.listdir(post_dir):
        if file_name.endswith(".html"):
            file_path = os.path.join(post_dir, file_name)
            lastmod = get_last_modified_time(file_path)
            encoded_file_name = quote(file_name)  # URLエンコーディング
            sitemap.append(f"<url>\n  <loc>{ROOT_URL}posts/{encoded_file_name}</loc>\n  <lastmod>{lastmod}</lastmod>\n</url>\n")
    
    # sitemap.xmlに書き込む
    with open(os.path.join(directory, "sitemap.xml"), "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
        for url in sitemap:
            f.write(url)
        f.write("</urlset>")

# カレントディレクトリでsitemap.xmlを生成する
generate_sitemap()
