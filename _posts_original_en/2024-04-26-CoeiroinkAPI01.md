# Trying Voice Synthesis with COEIROINK v2 API in Python
::tags{Voice Synthesis, COEIROINK, Python}::

---

I tried running the COEIROINK voice synthesis software from Python.  
I'll specifically introduce the methods and results from that attempt.  
The code is also uploaded on GitHub as [basic-codes-coeiroink-api](https://github.com/hitbug0/basic-codes-coeiroink-api), so feel free to check it out!

## What You Will Learn from This Article
In this article, I'll introduce specific steps and example code for running COEIROINK (v2) from Python.  
For an overview of COEIROINK, its terms of use, and what AI voice synthesis is, check out my [previous COEIROINK article](./2024-04-25-CoeiroinkGUI.html).

## Steps
If you want to execute with minimal code, follow these steps including the preparation.  
You only need to do steps 2, 5, and 6 each time.  
If you think this is too much hassle, check out the [handy scripts](#section5).

1. Install Python and its libraries (only once)
    - Install Python.
        - I use version 3.10, but anything from 3.6 onwards should work.
    - Install `requests` and `pydub` via pip.
    - `json` is a standard library, so no need to install it if Python is already installed.
2. Set up COEIROINK in a usable state via the GUI and start it.

    - The method is described in my [previous COEIROINK article](./posts_2024-04-25-CoeiroinkGUI.html/#section4).
3. Run the `check_speaker_info.py` script and note the results (only when adding new models).
4. Based on the `check_speaker_info.py` execution results, update `SPEAKER_INFO` in `text2audio.py`.
5. Write the conversation content you want to convert to audio in `input.txt`.
6. Run `text2audio.py`.

## Code
Automatically create a conversation between AI Voice Actor Ayaka and AI Voice Actor Kanae from a text file.  
We'll use the following three files.

- `check_speaker_info.py` (only when adding new models)
    - This script retrieves information about the voice models (`speaker`) and their speaking styles (`style`).  
    - Specify the obtained information in your program.
    - You can run this script from any directory.
- `text2audio.py`
    - Converts the conversation written in `input.txt` into an audio file.
    - Update `SPEAKER_INFO` based on the output from `check_speaker_info.py`.

- `input.txt`
    - Written in the format "Voice Model Name: Dialogue."
    - When adding voice models, ensure the voice model names match those in the program.

Here are the contents of each file.  
The functionality of `text2audio.py` is minimal, so customize it as needed!

### check_speaker_info.py
This script retrieves information about the voice models (`speaker`) and their speaking styles (`style`).  
Specify the obtained information in your program.  
You can run this script from any directory.

```Python
import json
import requests

# Local server for communication
URL = "http://localhost:50032/"

# List speaker information
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

Here is an example output.  

```javascript
==============================
name: AI Voice Actor Ayaka
id:   d1143ac1-c486-4273-92ef-a30938d01b91
styles:
       50 : normalv2

==============================
name: AI Voice Actor Kanae
id:   d41bcbd9-f4a9-4e10-b000-7a431568dd01
styles:
      100 : normal
      101 : joy A type
      103 : joy B type
      102 : happiness

==============================
name: Tsukuyomi-chan
id:   3c37646f-3881-5374-2a83-149267990abc
styles:
        0 : calm
```

### input.txt (example)
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

# Local server for communication
URL = "http://localhost:50032/"

# Voice model information
# Voice model name: [voice model (speaker) id, speaking style (style) id]
SPEAKER_INFO = {
    "kanae": ['d41bcbd9-f4a9-4e10-b000-7a431568dd01', '100'], # AI Voice Actor Kanae
    "ayaka": ['d1143ac1-c486-4273-92ef-a30938d01b91', '50' ], # AI Voice Actor Ayaka
}

def make_wav(text, speed_scale, speaker_info):
    # Function to generate wav from text using the voice model
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
    
    if response.content == b'Internal Server Error':
        print('Internal Server Error')
    
    return response.content

def play_wav(wav):
    # Function to play wav
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
    # Function to write wav file
    # file_path: Path to save the file
    # audio_data: Audio data to save (binary string)
    # sample_width: Sample bit width (byte size) default is 2 (16bit)
    # sample_rate: Sample rate default is 44100Hz
    # channels: Number of channels default is 1 (mono)
    audio_segment = AudioSegment(audio_data, sample_width=sample_width, frame_rate=sample_rate, channels=channels)
    # Save as wav file
    audio_segment.export(file_path, format="wav")

# Main process
def text2audio():
    # Read text file
    with open("input.txt", "r", encoding='utf-8') as file:
        # Read each line as a list
        lines = file.readlines()

    speed_scale = 1.0 # Speaking speed
    
    # Voice synthesis
    audio_data = b''
    for line in lines:
        speaker, text = line.split(":")
        w0 = make_wav(text, speed_scale, SPEAKER_INFO[speaker])
        # _ = play_wav(w0) # Use this to play each part individually
        audio_data += w0

    # Output concatenated audio
    play_wav(audio_data) # Play
    write_wav_file("output.wav", audio_data) # Save

text2audio()
```

## Results
Here are the results of running the above code.  

<iframe src="https://www.youtube.com/embed/ObrSrKgrjMQ?si=VvjUSx0-2EsiLsob" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

The intonation may still be a bit unnatural, but considering it's free and easy to use, it's pretty impressive.  
If you find it insufficient, I've included hints for further adjustments in the next section, so take a look!

## Handy Scripts
There are too many manual operations, so I've made things a bit easier with these three scripts.  
The procedure is now as follows:

1. Run `start.bat`.

    - COEIROINK will start automatically.
    - The API documentation page will also open automatically.
        - If you want to improve the program, refer to this! It might be a bit hard to understand...

    - `check_speaker_info.py` will also run automatically.
        - When adding models, update `SPEAKER_INFO` in `text2audio.py` based on this output.

1. Write the conversation content you want to convert to audio in `input.txt`.
1. Run `run.bat`.
    - `text2audio.py` will run automatically.

Please note that this assumes the following folder structure.  
(It's neat to keep the scripts organized in a folder.)

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
You need to replace the path of `COEIROINKv2.exe` with the correct one,  
so make sure to edit the second line before using it!
```cmd
@echo off
start C:\Users\xxxxxxxxxxxxx\COEIROINKv2.exe
powershell -ExecutionPolicy Bypass -File "./scripts

/connect.ps1"
python ./scripts/check_speaker_info.py
pause
```

### connect.ps1
A file called by `start.bat`.  
This script will open the page in Chrome once the local server is ready for communication.  
If the path to Google Chrome is different, edit the second-to-last line.

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
A batch file to execute `text2audio.py`.
```cmd
python ./scripts/text2audio.py
pause
```

## Summary
I introduced specific methods and results for running COEIROINK from Python.  
In the future, I plan to explore more advanced applications.