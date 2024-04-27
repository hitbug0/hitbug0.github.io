# ディレクトリ構成図を作る方法（Pythonコードもあるよ）
[](::tags::RPA,Python)

---

ディレクトリ構成図を作る方法について、場面に応じて2通り紹介します。

## この記事でわかること
以下のような図を簡単に作る方法がわかります。
```
C:\Users\xxx
 ├── aa
 │    ├── aa
 │    ├── bb
 │    │    └── cc
 │    ├── dd
 │    │    ├── ee
 │    │    │    └── ff
 │    │    └── gg
 │    │         ├── hh
 │    │         └── ii
 │    └── jj
 ├── kk
 └── ll
```

## 2通りの方法
### [Tree](https://tree.nathanfriend.io/)
- Webページ上にディレクトリ構成をテキストで書き込むと、いい感じの図(テキストベース)に書き換えてくれます。
- まだそのフォルダが実在しない場合に有効です。

- [ソースコード](https://gitlab.com/nfriend/tree-online)も公開されています。

### [directory-structure-diagram](https://github.com/hitbug0/directory-structure-diagram)
- ローカル環境でこのPythonコードを実行すると、いい感じの図(`directory_structure.txt`)を出してくれます。
- すでにフォルダやその中身がある場合に有効です。
- 会社の業務で使うときとかはローカルなので安心ですし、自分でやるべき操作はプログラムの実行だけなのでお手軽だと思います。

- 他のプログラムにも楽に組み込めると思います。

## 方法2について
コード書いたの自分なので軽く紹介しておきます。 

### 使い方 
1. Pythonをインストールする
    - バージョンについて：自分は `3.10` ですが、`3.6` 以降ならたぶん大丈夫

1. [GitHubにアップしているコード](https://github.com/hitbug0/directory-structure-diagram)をダウンロードする
1. `directory-structure-diagram.py` と `run.bat` を、中身の構成を知りたいディレクトリに配置する
1. `run.bat`を実行する
    - あるいは `directory-structure-diagram.py` を実行するでも大丈夫です（batファイルは楽に操作するためだけのものなので）

以上です！

### コード
#### directory-structure-diagram.py
```Python
import os

NUM_INDENTS = 1
BRANCH = " "*NUM_INDENTS + "├── "
LEAF   = " "*NUM_INDENTS + "└── "
LINE   = " "*NUM_INDENTS + "│   "
SPACE  = " "*NUM_INDENTS + "    "

def make_line(lst):
    result = ""
    for item in lst:
        if item == 0:
            result += SPACE
        elif item == 1:
            result += LINE
    return result

def make_branch(item, depth, shape=BRANCH):
    return make_line(depth) + shape + item + "\n"

def explore_directory(directory, depth=[]):
    result = ""
    items = os.listdir(directory)
    items.sort()
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            if index == len(items) - 1:
                result += make_branch(item, depth, shape=LEAF)
                add_depth = 0
            else:
                result += make_branch(item, depth)
                add_depth = 1
            result += explore_directory(path, depth + [add_depth])
        else:
            if index == len(items) - 1:
                result += make_branch(item, depth, shape=LEAF)
                depth = depth[:-1]+[0]
            else:
                result += make_branch(item, depth)
    return result

def output_directory_structure(directory):
    structure = explore_directory(directory)
    with open("directory_structure.txt", "w", encoding="utf-8") as file:
        file.write(directory + "\n")
        file.write(structure)

current_directory = os.getcwd()
output_directory_structure(current_directory)
```

#### run.bat
```cmd
python directory-structure-diagram.py
```

## まとめ
ディレクトリ構成図を作る方法について、場面に応じて良さげな方法を2通り紹介しました。   
お役に立てば嬉しいです～
