# COEIROINK v2 API をつかってPythonで音声合成してみた
[](::tags::音声合成,COEIROINK,Python)

---

COEIROINKという音声合成ソフトを、Pythonから実行してみました。  
そのときの方法と結果を具体的に紹介します。  
コードは[GitHub](https://github.com/hitbug0/basic-codes-coeiroink-api)にもアップしているので見てみてくださいね！


## この記事でわかること
この記事ではCOEIROINK (v2)をPythonから動かすときの具体的な手順とコード(例)について紹介します。  
COEIROINKの概要やその利用規約、そもそもAI音声合成とは何かみたいなことは[前回の記事](./2024-04-25-CoeiroinkGUI.html)を読んでみてください～  


## 手順
最小限のコードで実行する場合は、準備含めて以下のステップになります。  
毎回やるのは 2., 5., 6. です。  
...めんどくさくない？　という人は[便利なスクリプト](#section5)も併せてご覧ください～
1. Pythonおよびそのライブラリをインストールする（初回のみ）
    - Pythonをインストールします。
        - バージョンについて、自分は3.10ですが、たぶん3.6以降であればOKかと思います
    - `requests`と`pydub`をpipでインストールします
    - `json`は標準ライブラリなので、Pythonが入っていればインストール不要です
1. COEIROINKをGUIで使える状態にして、起動する

    - [前回の記事](./2024-04-25-CoeiroinkGUI.html/#section4)に方法を書いてます
1. 以下の`check_speaker_info.py`を実行し、結果をメモしておく（モデル追加時のみ）
1. `check_speaker_info.py`の実行結果に応じて、`text2audio.py`の`SPEAKER_INFO`を書き換える
1. 音声にしたい会話内容を`input.txt`に書く
1. `text2audio.py`を実行する



## コード
AI声優-朱花とAI声優-金苗の会話をtxtファイルから自動作成します。  
以下の3つのファイルを使います。

- `check_speaker_info.py`（モデル追加時のみ）
    - このコードを実行することで、音声モデル(`speaker`)の情報と、話し方(`style`)の情報が取得できます。  
    - ここで取得した情報をプログラムで指定します。
    - 実行するディレクトリはどこでも大丈夫です。  
- `text2audio.py`
    - `input.txt`に書かれた会話を音声ファイルに変換するコードです
    - `check_speaker_info.py`の出力結果に応じてSPEAKER_INFOを書き換えてくださいね

- `input.txt`
    - 「音声モデル名: セリフ」の形式で書くようにしています
    - 音声モデルを追加するときは、音声モデル名をプログラムと連動させるようにしてくださいね

それぞれの中身は以下の通りです。  
`text2audio.py`の機能は最低限なので、ここからカスタマイズしていってください！

### check_speaker_info.py
このコードを実行することで、音声モデル(`speaker`)の情報と、話し方(`style`)の情報が取得できます。  
ここで取得した情報をプログラムで指定します。
実行するディレクトリはどこでも大丈夫です。  

```Python
import json
import requests

# やり取りするローカルサーバ
URL = "http://localhost:50032/"

# スピーカーの情報を一覧表示
def check_speaker_info():
    response = requests.get(URL+"v1/speakers")
    speakers = response.json()
    for speaker in speakers:
        print("\n"+"="*30)
        print(f"name: {speaker['speakerName']}\nid:   {speaker['speakerUuid']}")
        styles = speaker['styles']
        print('styles:')
        for style in styles:
            print(f"     {style['styleId']:>4} : {style['styleName']}")

check_speaker_info()
```

以下が実行結果例です。  

```javascript
==============================
name: AI声優-朱花
id:   d1143ac1-c486-4273-92ef-a30938d01b91
styles:
       50 : のーまるv2

==============================
name: AI声優-金苗
id:   d41bcbd9-f4a9-4e10-b000-7a431568dd01
styles:
      100 : のーまる
      101 : 愉悦 Aタイプ
      103 : 愉悦 Bタイプ
      102 : 喜び

==============================
name: つくよみちゃん
id:   3c37646f-3881-5374-2a83-149267990abc
styles:
        0 : れいせい
```


### input.txt（例です）
```javascript
ayaka: 今日はいい天気だね～
ayaka: そうだ！　お姉ちゃん、外に行こうよ！
kanae: うーん、でもちょっと寒くない？
```

### text2audio.py
```Python
import json
import requests
from pydub import AudioSegment, playback

# やり取りするローカルサーバ
URL = "http://localhost:50032/"

# 音声モデルの情報
# 音声モデル名: [音声モデル(speaker)のid, 話し方(style)のid]
SPEAKER_INFO = {
    "kanae": ['d41bcbd9-f4a9-4e10-b000-7a431568dd01', '100'], # AI声優-金苗
    "ayaka": ['d1143ac1-c486-4273-92ef-a30938d01b91', '50' ], # AI声優-朱花
}

def make_wav(text, speed_scale, speaker_info):
    # 音声モデルを使ってtextからwavを生成する関数
    speaker_uuid, style_id = speaker_info
    response = requests.post(
        URL+"v1/predict",
        json={
            "speakerUuid": speaker_uuid,
            "styleId": style_id,
            "text": text,
            "speedScale": speed_scale
            }
        )
    
    if response.content==b'Internal Server Error':
        print('Internal Server Error')
    
    return response.content

def play_wav(wav):
    # wavを再生する関数
    playback.play(
        AudioSegment(
            wav,
            sample_width=2, 
            frame_rate=44100, 
            channels=1
            )
        )
    return 0

def write_wav_file(file_path, audio_data, sample_width=2, sample_rate=44100, channels=1):
    # wavを書き出す関数
    # file_path: 書き出すファイルのパス
    # audio_data: 書き出す音声データ（バイナリ形式の文字列）
    # sample_width: サンプルのビット幅（バイト数）デフォルトは2（16bit）
    # sample_rate: サンプルレート デフォルトは44100Hz
    # channels: チャンネル数 デフォルトは1（ステレオ）
    audio_segment = AudioSegment(audio_data, sample_width=sample_width, frame_rate=sample_rate, channels=channels)
    # wavファイルとして保存
    audio_segment.export(file_path, format="wav")

# メイン処理
def text2audio():
    # テキストファイルの読み込み
    with open("input.txt", "r", encoding='utf-8') as file:
        # ファイルの各行をリストとして読み込む
        lines = file.readlines()

    speed_scale = 1.0 # 発話速度
    
    # 音声合成
    audio_data = b''
    for line in lines:
        speaker, text = line.split(":")
        w0 = make_wav(text, speed_scale, SPEAKER_INFO[speaker])
        # _ = play_wav(w0) # 一つずつ再生する場合は使う
        audio_data += w0

    # 連結した音声の出力
    play_wav(audio_data) # 再生
    write_wav_file("output.wav", audio_data) # 保存

text2audio()
```


## 結果
上記のコードを実行した結果を貼っておきます。  

＜●●●●●youtube●●●●●＞


少しイントネーションの不自然さは残りますが、無料で気軽に使えるものの割には本当にすごいなぁと思います。  
物足りない方は、もっと調整していくヒントを次の章に書いたので見ていってくださいね！

## 便利なスクリプト
あまりにも手動操作が多いので、以下3つのスクリプトで少し便利にしました。  
手順はこんな感じになりました。  

1. `start.bat`を実行する

    - COEIROINKが自動で起動する
    - apiのドキュメントのページも自動で開く
        - プログラムを改良したい人はここを参考にしてください！　ちょっとわかりにくいですが...

    - `check_speaker_info.py`も自動で実行される
        - モデル追加時はこの出力に応じて`text2audio.py`の`SPEAKER_INFO`を書き換える

1. 音声にしたい会話内容を`input.txt`に書く
1. `run.bat`を実行する
    - `text2audio.py`が自動で実行される

以下のようなフォルダ構成を前提としていますのでご注意くださいね。  
（スクリプトはフォルダに入れてまとめておくのがすっきりしてよいと思います。）

<br>

- **scripts**
    - `text2audio.py`
    - `check_speaker_info.py`
    - `connect.ps1`
- `input.txt`
- `run.bat`
- `start.bat`

<br>

### start.bat
`COEIROINKv2.exe`のパスを正しいものに置き換える必要があるので、  
使う前に2行目を書き換えてくださいね！
```cmd
@echo off
start C:\Users\xxxxxxxxxxxxx\COEIROINKv2.exe
powershell -ExecutionPolicy Bypass -File "./scripts/connect.ps1"
python ./scripts/check_speaker_info.py
pause
```

### connect.ps1
`start.bat`の実行時に呼び出すファイルです。  
ローカルサーバと通信できるようになったらChromeでそのページを開くスクリプトです。  
Google Chromeのパスが違う場合は最後から2行目を書き換えてください！

```PowerShell
$maxAttempts = 100
$waitTimeSeconds = 0.5

for ($i = 1; $i -le $maxAttempts; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:50032/docs" -Method Head
        if ($response.StatusCode -eq 200) {
            Write-Host "HTTP connection successful: HTTP status code 200 OK"
            break
        } else {
            Write-Host "HTTP connection succeeded, but the HTTP status code is not 200."
        }
    } catch {
        Write-Host "waiting for HTTP connection..."
    } finally {
        Start-Sleep -Seconds $waitTimeSeconds
    }
}

$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Start-Process -FilePath $chromePath -ArgumentList "http://localhost:50032/docs"
```

### run.bat
`text2audio.py`を実行するためのbatファイルです。  
```cmd
python ./scripts/text2audio.py
pause
```

## まとめ
COEIROINKをPythonから実行する際の方法と結果を具体的に紹介しました。  
追々もう少し応用的なところもいじってみたいと思います。

