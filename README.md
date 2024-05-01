## Page URL
[hitbug home page](https://hitbug0.github.io/)

## ファイル構成
「`-en`」は各ファイルの英語記事版です。

- **_posts_original**
    - `yyyy-mm-dd-filename.md` : 記事ページのソースファイル
    - `yyyy-mm-dd-filename.html` : 記事ページのHTMLファイル（中間ファイル）。VSCodeの拡張機能でmdファイルから自動作成
- **_programs** : ローカルで回すスクリプトが入っている
    - `make_posts.py` : 記事を作る
    - `make_index.py` : インデックスページとタグ表示要素を作る
    - `make_make_sort_by_date.py` : 日付降順の記事リストページを作る
    - `add_ad_to_posts.py` : 記事に広告を入れる
    - `make_sitemap.py` : サイトマップファイルを作る
    - `add_sitemap_to_google.py` : サイトマップファイルをGoogle Search Consoleに送信する(RPA)
    - `modules.py` : 共通の関数
    - `update.py` : 更新時に書く機能を呼び出すスクリプト
    - `last_modified_time.csv` : 最終更新日時を記録したファイル
- **_templates** : サイト用HTMLファイル作成のためののテンプレートが入っている
    - `index-temp.html`
    - `post-temp.html`
    - `tags-temp.html`
- **contents**
    - **icon** : アイコン画像が入っている
    - **img** : 記事に挿入する画像が入っている
    - **stl** : 記事に挿入する3D形状ファイルが入っている
- **includes**
    - **three.js** : 3Dモデル表示のスクリプトが入っている。[公式ページはこちら](https://threejs.org/)
    - `footer.html` : フッタのHTMLファイル
    - `header.html` : ヘッダのHTMLファイル
    - `hamburger-menu.html` : ウィンドウ幅が狭いときのハンバーガーメニューのHTMLファイル
    - `tags-index.html` : インデックスページ用のタグ表示要素。スクリプトで自動作成
    - `tags-post.html` : 記事ページ用のタグ表示要素。スクリプトで自動作成
    - `month.html` : 日付降順の記事リストページ用の月リスト
    - `style.css` : スタイルファイル
    - `clipboard-script.js` : コピー機能のスクリプト
    - `display-3dmodel.js` : three.jsの中身を呼び出すスクリプト
    - `hamburger-menu-trigger.js` : ハンバーガーメニューの動作のスクリプト
- **posts**
    - `yyyy-mm-dd-filename.html` : 記事ページのHTMLファイル。スクリプトで自動作成

- `index.html` : インデックスページのHTMLファイル。スクリプトで自動作成
- `sort-by-date.html` : 日付降順の記事リストページのHTMLファイル。スクリプトで自動作成
- `manifest.json` : アプリとしてのメタデータを定義するファイル
- `README.md` : このファイル
- `ads.txt` : Google AdSenseのためのファイル
- `add_sitemap_to_google.bat` : `add_sitemap_to_google.py`をローカルで実行するためのファイル
- `run.bat` : ページ更新とデバッグ用のファイル（`update.py`を実行してローカルホストでこのページを開く）
- `sitemap.xml` : SEOのためのサイトマップファイル。スクリプトで自動作成


## Copyright
Copyright 2024 hitbug
