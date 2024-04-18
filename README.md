## Page URL
[hitbug home page](https://hitbug0.github.io/)

## ファイル構成

- **.git** : Gitリポジトリ
- **_posts_original**
    - `yyyy-mm-dd-filename.md` : 記事ページのソースファイル
    - `yyyy-mm-dd-filename.html` : 記事ページのHTMLファイル（中間ファイル）。VSCodeの拡張機能でmdファイルから自動作成
- **_programs** : ローカルで回すスクリプトが入っている
    - `make_posts.py` : 記事を作る
    - `make_index.py` : インデックスページとタグ表示要素を作る
    - `make_sitemap.py` : サイトマップファイルを作る
    - `modules.py` : 共通の関数
- **_templates** : サイト用HTMLファイル作成のためののテンプレートが入っている
    - `index-temp.html`
    - `post-temp.html`
    - `tags-temp.html`
- **contents**
    - **icon** : かわいいアイコン画像が入っている
    - **img** : 記事に挿入する画像が入っている
    - **stl** : 記事に挿入する3D形状ファイルが入っている
- **includes**
    - **three.js** : 3Dモデル表示のスクリプトが入っている。[公式ページはこちら](https://threejs.org/)
    - `footer.html` : フッタのHTMLファイル
    - `header.html` : ヘッダのHTMLファイル
    - `hamburger-menu.html` : ウィンドウ幅が狭いときのハンバーガーメニューのHTMLファイル
    - `tags-index.html` : インデックスページ用のタグ表示要素。スクリプトで自動作成
    - `tags-post.html` : 記事ページ用のタグ表示要素。スクリプトで自動作成
    - `style.css` : スタイル
    - `clipboard-script.js` : コピー機能のスクリプト
    - `display-3dmodel.js` : three.jsの中身を呼び出すスクリプト
    - `hamburger-menu-trigger.js` : ハンバーガーメニューの動作のスクリプト
- **posts**
    - `yyyy-mm-dd-filename.html` : 記事ページのHTMLファイル。スクリプトで自動作成

- `ads.txt` : Google AdSenseのためのファイル
- `manifest.json` : アプリとしてのメタデータを定義するファイル
- `index.html` : インデックスページのHTMLファイル。スクリプトで自動作成
- `README.md` : このファイル
- `run.bat` : _programsのスクリプトをローカルで実行するためのファイル
- `sitemap.xml` : SEOのためのサイトマップファイル。スクリプトで自動作成


## Copyright
Copyright 2024 hitbug
