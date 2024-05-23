# How to Synthesize AI Voices with COEIROINK (v2 Compatible) [Easy, Free, and Commercial Use Allowed]
::tags{Voice Synthesis, COEIROINK}::

---

This guide will show you how to synthesize voices using COEIROINK.  
It's a highly recommended software that is free, easy to set up, intuitive to use, and can be used for commercial purposes (under certain conditions).  
(For commercial use, make sure to read the entire article. Also, check the terms again when you use it, as they might change in the future.)

## What You'll Learn from This Article
If you're only interested in the usage instructions, jump to [Initial Setup](#section4).  
If you want to learn about the API, check out the [article about COEIROINK's API](./2024-04-26-CoeiroinkAPI01.html).

- What AI voice synthesis is (briefly)
- Benefits of using voice synthesis
- Commercial use (as of April 2024)
- How to use COEIROINK (detailed)
    - Initial setup
    - Basic usage

## Introduction
### What is AI Voice Synthesis?
AI voice synthesis is a technology that uses AI to create voice from text data.  
Here’s an example of the kind of voice you can create.

<iframe src="https://www.youtube.com/embed/RLPVL3Hmbio?si=CcpI9LMNzVUJaIAX" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

By "AI," we mean a machine learning model that has learned from a large amount of data, combining text and the corresponding spoken voice.  
I’ll skip the detailed explanation!

### Benefits of Voice Synthesis
Using voice synthesis instead of recording human voices has several advantages:
- No noise in the audio source (such as air conditioning sounds)
- Clear articulation
- Standard narration speed, which can be controlled
- Voice files can be automatically created from text data while you work on other tasks
- Ability to add intonation
    - However, the output may still have some unnatural parts
- Easy to re-record as many times as needed
    - For example, you can edit the narration with the same voice even if the person in charge changes

Additionally, by integrating it with programs or language models, you can create robots that can converse, for example.  
(Some applications already use it this way!)

## About Commercial Use
Here are the terms of use for COEIROINK and the voice models used in this guide.

### Software (COEIROINK) Terms
The [COEIROINK Terms of Use](https://coeiroink.com/terms) are posted on the official website.  
As of April 2024, the terms are as follows:

- The software itself can be used commercially for free, even by corporations
- Voice models need to be checked individually
    - Some voice models have additional usage restrictions, while others do not

However, the terms may change in the future.  
The terms are clear and easy to understand, so please read them before starting to use the software.

### Terms for the Voice Models Used in This Guide
I used two voice models, `AI Voice Actor - Kinnae (Al声優・金苗)` and `AI Voice Actor - Akahana (Al声優・朱花)`.  
You can find the terms of use on the [AI Voice Actor official website](https://aiseiyou.com/).  
According to the terms as of April 2024, credit notation is required.  
This means you need to include the following in a corner of your video:

- COEIROINK:Al声優・金苗
- COEIROINK:Al声優・朱花

The terms vary by voice model, so please check them each time you use a new one!

## Initial Setup
This guide will cover how to set up `COEIROINK_CPU_v.2.3.4 (Windows)` with `AI Voice Actor - Kinnae` and `AI Voice Actor - Akahana`.  
There are three main steps for the initial setup:
1. Download the necessary files
2. Install the software
3. Organize the folder structure

Versions might change over time, so adjust as needed.

### 1. Download the Necessary Files
- Download the software
    - From the [official COEIROINK download page](https://coeiroink.com/download), download `COEIROINK_CPU_v.2.3.4 (Windows)` from the "Download" section.

    - You can use either BOOTH or DropBox.
    - Mac users or those with GPUs can download different files as needed.
- Download the voice models
    - Go to the [lower part of the COEIROINK official download page](https://coeiroink.com/download#:~:text=v.2.3.4(Mac)-,%E9%9F%B3,%E3%83%89%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E4%B8%8A%E3%81%A7) and find the section labeled "Voice Download."

    - Download `AI Voice Actor - Kinnae v.1.3.0` and `AI Voice Actor - Akahana v.1.1.0`.
    - Generally, choose the latest version available.

- Extract the three downloaded zip files separately.
    - You can extract them anywhere.
    - The file names will likely be:
        - `COEIROINK_WIN_CPU_v.2.3.4.zip`
        - `d1143ac1-c486-4273-92ef-a30938d01b91.zip`
        - `d41bcbd9-f4a9-4e10-b000-7a431568dd01.zip`

### 2. Install the Software
- Run the installer

    - Open the extracted **COEIROINK WIN_CPU_V.2.3.4** folder.
    - Double-click `COEIROINK_WIN_CPU_V.2.3.4.exe` to run it.
    - A command prompt will open, and the installation will begin.
    - Once the installation is complete, a folder named `COEIROINK_WIN_CPU_V.2.3.4` will appear at the same level as `COEIROINK_WIN_CPU_V.2.3.4.exe`.

### 3. Organize the Folder Structure
After step 2, the contents of the **COEIROINK WIN_CPU_V.2.3.4** folder should look like this:  
(Folders in **bold**, files in `orange`)

<br>

- **COEIROINK WIN_CPU_V.2.3.4**

    - `COEIROINK_WIN_CPU_v.2.3.4.7z.001`

    - `COEIROINK_WIN_CPU_v.2.3.4.exe`
    - **COEIROINK_WIN_CPU_v.2.3.4**
        - `COEIROINKv2.exe`
        - **engine**
        - **speaker_info**

<br>

Place the extracted voice model folders into the **speaker_info** folder.  
Initially, **speaker_info** should contain the following:

<br>

- **speaker_info**

    - **Tsukuyomi-chan**

        - **model**
        - **icons**
        - ... (and a few other items)

<br>

"Tsukuyomi-chan" is the default voice model.  
So, place the two extracted folders here, similar to the **Tsukuyomi-chan** structure.  
After adding the two folders, the **speaker_info** folder should look like this:

<br>

- **speaker_info**

    - **Tsukuyomi-chan**
        - **model**
        - **icons**
        - ... (and a few other items)

    - **d1143ac1-c486-4273-92ef-a30938d01b91**
        - **model**
        - **icons**
        - ... (and a few other items)

    - **d41bcbd9-f4a9-4e10-b000-7a431568dd01**
        - **model**
        - **icons**
        - ... (and a few other items)

<br>

That's it for the initial setup! Well done!

### Easy Installation Method for Official Voice Models (Added on 2024/04/27)
The voice models in the "AI Voice Actor Series" are officially recognized by COEIROINK, so you can install them directly from COEIROINK without downloading them individually!  
(Thanks to AoTokie from the management team for letting me know!)  
Considering this, the easiest installation method is as follows:
- Install the software: follow the method described on this page
- Install voice models:
    - For official COEIROINK models: use the method from the tweet
    - For non-official COEIROINK models: follow the method described on this page

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">ブログ拝見しました！「AI声優シリーズ」のボイスモデルはCOEIROINK公認モデルなので、モデルを個別にダウンロードせずともCOEIROINK上から直接インストールできたりします！<br>こちらの方が簡単なので連絡いたしました<br>(すでにご存じでしたらすみません…) <a href="https://t.co/9NzqJiMqGW">pic.twitter.com/

9NzqJiMqGW</a></p>&mdash; AI声優-/運営・青トキエ (@aotokie) <a href="https://twitter.com/aotokie/status/1783462483329765810?ref_src=twsrc%5Etfw">April 25, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## Basic Usage
- Start the software
    - Run `COEIROINKv2.exe` to start the software.
        - Note that it is not `COEIROINK_WIN_CPU_v.2.3.4.exe`.
        - Creating a shortcut and placing it on the desktop might be convenient.
- Basic operations
    - Here’s a diagram showing the basic operations! (Click to enlarge)

::img{
    file{
        how-to-use-coeiroink.png: Basic Usage of COEIROINK;
    }
    height: 250px;
}::

## Summary
I have provided a detailed guide on how to synthesize voices using COEIROINK.  
Give it a try!