# sitemap.xmlの作成をChatGPTに自動化してもらった
[](::tags::HTML,Web制作,Python,ChatGPT)

---

ブログをGoogle検索にヒットさせるにはsitemap.xmlを登録するのが必要らしい！  
しかし、記事を更新するたびにこのファイルを手動で更新するのは面倒...
というわけで、sitemap.xmlを自動で更新するスクリプトをChatGPTに書いてもらいました。

## sitemap.xmlとは
sitemap.xmlとは、XMLサイトマップの具体的なファイル名です。  
XMLサイトマップは個々のウェブサイトに紐づくデータであり、以下のようなものです。
- そのウェブサイト上のページの情報を検索エンジンが読み取れる形式（XML: 拡張可能マークアップ言語）で記述されたファイル
- そのウェブサイト上のすべてのページのURL、更新頻度、重要度などの情報が含まれる
    - ただし、すべての情報が絶対にそろってないとダメというわけではない
- これを用いることでそのウェブサイトのSEOが向上し、ユーザーがそのウェブサイト内の情報をより迅速に見つけられる


## ChatGPTに書いてもらったコード
ChatGPTにお願いして、以下のPythonコードを書いてもらいました。  
ChatGPTとのやり取りは[こんな感じ](https://chat.openai.com/share/f60f65b1-b84a-4189-96b1-c6b175bae28b)です。  

1. サイトマップファイル（sitemap.xml）の形式を例示してもらう
1. 「pythonで以下の処理をするコードを書いてください。～～～」みたいにお願いする
1. 細かい改良をしてもらう
    - 最終更新日時を「yyyy-mm-ddTHH:MM:SS+09:00」の形式にしてほしい
    - index.htmlにも同じ操作をしてサイトマップに含めてほしい

特に、最後の指示は[**間違えて途中までしか打ってない文章を送信した**](https://chat.openai.com/share/f60f65b1-b84a-4189-96b1-c6b175bae28b#:~:text=%E3%81%93%E3%81%AE%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AB%E4%BB%A5%E4%B8%8B%E3%81%AE%E6%A9%9F%E8%83%BD%E3%82%92%E4%BB%98%E3%81%91%E5%8A%A0%E3%81%88%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84%E3%80%82%0A%0A%2D%20index.html%EF%BC%88%E3%81%93%E3%82%8C%E3%81%AFposts%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%81%A7%E3%81%AF%E3%81%AA%E3%81%8F%E3%80%81python%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88%E3%81%A8%E5%90%8C%E3%81%98%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%81%AB%E3%81%82%E3%82%8B%EF%BC%89%E3%81%AB%E5%AF%BE%E3%81%97%E3%81%A6%E3%80%81posts%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E5%86%85%E3%81%AE)**にもかかわらず意図をくみ取ってもらえたので少しびっくりでした**...  
あとはPythonコード内の`https://example.com`の部分をちょろちょろっと変えれば、割とどなたでも使えるんじゃないかなと思います～

```Python
import glob
import os
import urllib.parse
from datetime import datetime

def get_last_modified_time(file_path):
    """
    Get the last modified time of a file.
    """
    modified_time = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(modified_time)

def generate_sitemap():
    """
    Generate sitemap.xml based on the files in the 'posts' directory.
    """
    # index.htmlの最終更新日時を取得
    index_last_modified = get_last_modified_time('index.html')

    files = glob.glob('posts/*.html')
    
    urls = []
    for file_path in files:
        file_name = os.path.basename(file_path)
        last_modified = get_last_modified_time(file_path)
        encoded_file_name = urllib.parse.quote(file_name)
        urls.append((encoded_file_name, last_modified))

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # index.htmlをsitemapに追加
    index_last_modified_str = index_last_modified.strftime('%Y-%m-%dT%H:%M:%S+09:00')
    sitemap_content += f'   <url>\n'
    sitemap_content += f'      <loc>https://example.com/index.html</loc>\n'
    sitemap_content += f'      <lastmod>{index_last_modified_str}</lastmod>\n'
    sitemap_content += f'   </url>\n'
    
    for file_name, last_modified in urls:
        last_modified_str = last_modified.strftime('%Y-%m-%dT%H:%M:%S+09:00')
        sitemap_content += f'   <url>\n'
        sitemap_content += f'      <loc>https://example.com/{file_name}</loc>\n'
        sitemap_content += f'      <lastmod>{last_modified_str}</lastmod>\n'
        sitemap_content += f'   </url>\n'
    
    sitemap_content += '</urlset>'
    
    with open('sitemap.xml', 'w') as sitemap_file:
        sitemap_file.write(sitemap_content)

if __name__ == "__main__":
    generate_sitemap()

```

## おまけ
上記のコードを仮に`generate_sitemap.py`として`programs`フォルダに入れている場合、以下のようなbatファイルを`programs`フォルダと同じ階層に作っておけば、このbatファイルをダブルクリックするだけでスクリプトを実行できます。
```
python ./programs/generate_sitemap.py
```

## まとめ
ブログをGoogle検索にヒットさせるために必要なsitemap.xmlを自動で更新するスクリプトを、  
ChatGPTに書いてもらいました。  
間違えて途中までしか打ってない文章を送信したにもかかわらず意図をくみ取ってもらえたので、少しびっくりでした...！  
sitemap.xmlを書いたりChatGPTを使ったりするときのご参考になればと思います～
