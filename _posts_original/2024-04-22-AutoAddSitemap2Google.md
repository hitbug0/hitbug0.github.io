# Pythonで画面操作を自動化してみた（初心者向けの色々詰め合わせコードあります）
[](::tags::RPA,Python,Web制作)

---

Pythonで画面操作を自動化する方法を紹介します。  
今回の題材は「Google Search ConsoleにXMLファイルを登録する」ですが、  
他の場面でも、例えば「過去の偉人が作ったソフトで毎回同じ操作が必要...」みたいなときに使える方法だと思います。  
（最近のWindowsを前提にしているので、他のOSや古めのWindowsでは動作しないと思います。ご注意ください...！）

## この記事でわかる事
- Pythonを使って画面操作を自動化する方法
    - 基本的なコマンド
    - 便利な関数もあるよ
- 自動化の例: XMLサイトマップをGoogle Search Consoleに登録する操作の自動化
    - 操作の手順
    - 自動化のためのコード
    - 実行結果(動画)


## 何を使ったら自動化できるの？
Pythonで色々な操作を自動化できます。  
今回は以下のようなライブラリを使いました。  
これだけでも割といろいろできちゃいますが、他にも便利なライブラリはあるかもです。

- **PyAutoGUI**
    - マウスの移動やクリック、キーボードの入力など、GUI操作を自動化できます。

- **pyperclip**
    - クリップボードの読み込みや書き込みができます。
- **subprocess**
    - 外部プロセスを起動し、その入出力を操作できます。
    - 特に、コマンドプロンプトでの操作をPython内で実行できます。
    - Pythonの標準ライブラリなので個別のインストールは不要です。
- **win32gui, win32con, win32api**
    - WindowsのGUI要素やシステムリソースにアクセスすることができます。
- **time**
    - 時間の取得や一時停止(スリープ)、性能測定、時間表現の変換、時間の演算などができます。
    - Pythonの標準ライブラリなので個別のインストールは不要です。

インストールコマンドも置いておきます。  
win32***はまとめて`pywin32`でインストールなので注意です！
```
pip install pyperclip
pip install pyautogui
pip install pywin32
```


## どんな操作を自動化できるの？
自動化コードの簡単な具体例として、今回使ったものをいくつか挙げておきます。  
ほんの一例なので、他にもたくさんできることありますよ～


### キーを押す操作
PyAutoGUIで、1つ以上のキーを押す操作を自動化できます。  
もちろん他にも押せるキーはたくさんありますので、詳しくは調べてみてください～
```Python
import pyautogui as pa

pa.hotkey('alt','d') # GoogleChromeでURL入力欄にカーソルを合わせる
pa.hotkey('f5') # ブラウザ上でページを更新
```

### 文字入力
PyAutoGUIとpyperclipで、文字を入力することができます。  
直接タイプすると日本語/英語の切り替えとかで躓きやすいので、「クリップボードにコピーして貼り付け」という方法がよさそうです。
```Python
import pyautogui as pa
import pyperclip

pyperclip.copy("hoge,hoge") # 文字列をクリップボードにコピー
pa.hotkey('ctrl','v') # 貼り付ける
```

### 画面内での画像表示位置の特定　→　クリック
PyAutoGUIで、画面内で画像を探すことができます。  
見つかった場合はその画像が表示されている位置の中央を教えてくれます。  

```Python
import pyautogui as pa

position_im = pa.locateOnScreen(img, confidence=0.8)
```
今回はこれを使って、表示されるのを待つ動作を`wait_disp`関数で定義しました。  
以下のような感じで使っています。

```Python
import pyautogui as pa

def wait_disp(img, wait_time=10):
    # 画像が画面内に表示されるのを待つ。表示されたら画像の表示位置を返す。
    dt = 0.5
    for i in range(int(wait_time/dt)):
        position_im = pa.locateOnScreen(img, confidence=0.8)
        if position_im:
            return position_im
        else:
            time.sleep(dt)
    return False

position_im = wait_disp('./hoge.png') # hoge.png を画面内で探す
pa.click(position_im, button='left', clicks=1) # hoge.png の中央を左クリック
```
### アプリの起動
subprocessを使って、指定したアプリを起動することができます。  
例えば、Google Chromeならこんな感じのコードで起動できます。

```Python
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
subprocess.Popen(chrome_path)
```

### アプリの表示位置/表示画面の変更、最大化など
win32gui, win32con, win32apiを使って、アプリの表示状態を変更できます。  
ウィンドウが小さすぎたりすると表示されるべきボタンが表示されなかったりするので、ウィンドウのサイズを指定するケースがあります。  
細かい説明は省略します！  

```Python
import win32gui
import win32con
import win32api

def get_chrome_window():
    # Chromeのウィンドウのうち直前に開いたもののハンドルを取得する。
    chrome_windows = []
    def enum_handler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and 'chrome' in win32gui.GetWindowText(hwnd).lower():
            chrome_windows.append(hwnd)
    win32gui.EnumWindows(enum_handler, None)
    return chrome_windows[0] if chrome_windows else None


def move_to_main_screen(hwnd, wait_time=10):
    # 表示するモニターデバイスをメインデバイスに切り替える。
    dt = 0.5
    n = wait_time/dt
    count=0
    while count<=n:
        monitor_info = win32api.GetMonitorInfo(
            win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
            )
        main_monitor_info = win32api.GetMonitorInfo(
            win32api.MonitorFromWindow(0, win32con.MONITOR_DEFAULTTOPRIMARY)
            )
        if monitor_info['Device'] == main_monitor_info['Device']:
            break
        else:
            # hwndを表示するモニターを切り替える
            win32gui.MoveWindow(hwnd, 
                main_monitor_info['Monitor'][0], 
                main_monitor_info['Monitor'][1], 
                monitor_info['Monitor'][2]-monitor_info['Monitor'][0], 
                monitor_info['Monitor'][3]-monitor_info['Monitor'][1], 
                True)
            time.sleep(dt) 
            count +=1

chrome_window = None # Chromeのハンドルの初期化
while not chrome_window: # ハンドルに値が入るまで get_chrome_window() をトライする
    chrome_window = get_chrome_window()
    time.sleep(0.05)
move_to_main_screen(chrome_window) # メイン画面で開く
win32gui.ShowWindow(chrome_window, win32con.SW_MAXIMIZE) # ウィンドウを最大化する

```


## 今回はどういう操作を自動化したの？
今回自動化するのは、XMLサイトマップをGoogle Search Consoleに登録する操作です。  
具体的には、以下のような操作手順になります。

1. Google Chromeを起動する

1. 表示ウィンドウを調整する
    - メインウィンドウで開く
    - ウィンドウを最大化する
1. Google ChromeのURL欄にGoogle Search ConsoleのURLを記入し、`Enter`キーを押す
1. Google Search Consoleの画面が開いたことを確認する
    - 画面内で `sitemap1.png` を見つける
1. ファイル名(sitemap.xml)を所定の欄に入力する
    - 入力欄にカーソルを合わせるために、 `sitemap1.png` をクリックした後で`Tab`キーを押す
    - カーソルがあっている状態でファイル名をクリップボードにコピーしてペーストする
1. 送信ボタン(`sitemap2.png`)を押す
1. 送信処理が終わったことを確認し、ページを更新する
    - `sitemap3.png` (送信完了のポップアップを閉じるボタン)が表示されたら、これをクリックする
    - 少し待ってから`F5`キーを押す


## 具体的なコードは？
こんな感じです！  
少なくとも冒頭のURLの部分はご自身のものに書き換えてくださいね！

```Python
import pyautogui as pa
import pyperclip
import time
import subprocess
import win32gui
import win32con
import win32api

URL = "https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fhitbug0.github.io%2F"

def wait_disp(img, wait_time=10):
    # 画像が画面内に表示されるのを待つ。表示されたら画像の表示位置を返す。
    dt = 0.5
    for i in range(int(wait_time/dt)):
        position_im = pa.locateOnScreen(img, confidence=0.8)
        if position_im:
            return position_im
        else:
            time.sleep(dt)
    return False

def get_chrome_window():
    # Chromeのウィンドウのうち直前に開いたもののハンドルを取得する。
    chrome_windows = []
    def enum_handler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and 'chrome' in win32gui.GetWindowText(hwnd).lower():
            chrome_windows.append(hwnd)
    win32gui.EnumWindows(enum_handler, None)
    return chrome_windows[0] if chrome_windows else None

def move_to_main_screen(hwnd, wait_time=10):
    # 表示するモニターデバイスをメインデバイスに切り替える。
    dt = 0.5
    n = wait_time/dt
    count=0
    while count<=n:
        monitor_info = win32api.GetMonitorInfo(
            win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
            )
        main_monitor_info = win32api.GetMonitorInfo(
            win32api.MonitorFromWindow(0, win32con.MONITOR_DEFAULTTOPRIMARY)
            )
        if monitor_info['Device'] == main_monitor_info['Device']:
            break
        else:
            # hwndを表示するモニターを切り替える
            win32gui.MoveWindow(hwnd, 
                main_monitor_info['Monitor'][0], 
                main_monitor_info['Monitor'][1], 
                monitor_info['Monitor'][2]-monitor_info['Monitor'][0], 
                monitor_info['Monitor'][3]-monitor_info['Monitor'][1], 
                True)
            time.sleep(dt) 
            count +=1

def main():
    # コマンドを実行してGoogle Chromeを起動
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    subprocess.Popen(chrome_path)
    
    # 表示ウィンドウの調整
    time.sleep(0.5)  # Chromeの起動待ち時間
    chrome_window = None
    while not chrome_window:
        chrome_window = get_chrome_window()
        time.sleep(0.05)
    move_to_main_screen(chrome_window) # メイン画面で開く
    win32gui.ShowWindow(chrome_window, win32con.SW_MAXIMIZE) # ウィンドウを最大化する
    
    # URL記入
    pa.hotkey('alt','d')
    time.sleep(0.05)
    pyperclip.copy(URL)
    pa.hotkey('ctrl','v')
    time.sleep(0.05)
    pa.hotkey('enter')

    # sitemap1.pngを画面内で見つけてクリック
    time.sleep(2)
    position_im = wait_disp('./contents/img/sitemap1.png')
    pa.click(position_im, button='left', clicks=1)
    
    # ファイル名を入力して送信
    pa.hotkey('tab')
    time.sleep(0.05)
    pyperclip.copy("sitemap.xml")
    pa.hotkey('ctrl','v')
    time.sleep(0.05)
    position_im = wait_disp('./contents/img/sitemap2.png')
    pa.click(position_im, button='left', clicks=1)
    
    # 送信処理が終わったらページを更新
    position_im = wait_disp('./contents/img/sitemap3.png', wait_time=40)
    time.sleep(0.05)
    pa.click(position_im, button='left', clicks=1)
    time.sleep(1)
    pa.hotkey('f5')

main()
```

## 実行結果はどんな感じ？
今度動画とって載せます！

## まとめ
「Google Search ConsoleにXMLファイルを登録する」という操作を題材に、
Pythonで画面操作を自動化する方法を紹介しました。  
例えば「過去の偉人が作ったソフトで毎回同じ操作が必要...」
みたいなときに使える方法だと思います。  
私自身仕事で何度か使っていますので、使えそうな場面があったらぜひ使ってみてください～

