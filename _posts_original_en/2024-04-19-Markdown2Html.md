# How to Convert Markdown to HTML in VSCode
::tags{Web Development, HTML, markdown, VSCode}::

---

With VSCode, you can automatically convert Markdown files to HTML. In this article, I will briefly touch on the significance of automatic conversion and the benefits of using VSCode, followed by a detailed explanation of how to use it.

## The Significance of Automatic Conversion from Markdown to HTML
Markdown is a simple way to write structured documents, offering the following advantages:
- You can write it almost anywhere, anytime.
- No need to worry about layout or style.
- Various platforms like GitHub and Qiita can nicely convert and display it.
- Being plain text, it allows for version control.

However, when using it as a web page or displaying it in a browser, HTML files are typically used instead of Markdown files. Therefore, being able to automatically convert Markdown to HTML makes it easy to deploy documents created in Markdown as web pages.

## Benefits of Using VSCode
VSCode is a flexible and highly extensible text editor available for various environments such as Windows, macOS, and Linux. It is also well-suited for editing Markdown and can add the following features as extensions:
- Real-time conversion and preview of Markdown to HTML.
- Output of Markdown in HTML format.

Thus, I believe it is a suitable tool for efficiently editing Markdown and converting it to HTML to quickly create content. (I've tried various other text editors, but VSCode has a great user experience and supports drawing with Mermaid, so I ended up sticking with it.)

## How to Use It
### Initial Setup
Follow these steps to enable the preview and output features in VSCode.  
(Note: These steps are written for Windows 10. Sorry if it’s different on macOS, etc.!)

1. Install VSCode
    - Download the installer from the [VSCode download page](https://code.visualstudio.com/download).
        - Choose the installer appropriate for your OS.
    - Run the downloaded installer.

1. Install Extensions
    - Launch VSCode and open the extension search bar with `ctrl+shift+X`.
    - Search for and install the following extensions by pressing the `Install` button:
        - **markdown PDF**
            - For outputting functionality.
        - **Markdown Preview Mermaid Support**
            - For preview functionality, including diagrams written with Mermaid.
            - For more about Mermaid, check out [How to Draw Diagrams in Markdown with Mermaid](../posts-en/2024-04-19-mermaid.html).
        - **Mermaid Markdown Syntax Highlighting**
            - For syntax highlighting when writing Mermaid diagrams in Markdown files.

1. Open a Markdown File
    - Change the text file extension to `.md` and drag and drop it into the VSCode window to open it.
    - If a popup appears at this point, it should be fine to click `OK` (I can't remember what the popup was about).

1. Initial Setup for the Preview Feature
    - Press `ctrl+K` followed by `ctrl+T`, and select `Light Modern` from the list that appears.
        - The text was not visible with a dark background, if I remember correctly.
        - It might be possible that it will display correctly with a dark background in the future.
    - Click somewhere in the window of the open Markdown file to activate it, then press `ctrl+shift+V` to display the preview.

1. Initial Setup for the Output Feature
    - Open the search bar with `ctrl+shift+P` and search for `Markdown PDF: Export (html)`, then left-click on the gear icon.
    - Double-click the `Keybinding` field.
    - Press the key you want to use as a shortcut, and confirm with `Enter`.
        - Many keys are already in use by default, so there may be conflicts. `ctrl+shift+/` seemed to work without conflict.
    - Click somewhere in the window of the open Markdown file to activate it, then press the shortcut key you set. An HTML file will be output in the same directory as the Markdown file.

### Regular Usage
1. Open a Text File
    - Drag and drop it into the screen.
1. Edit the File
    - Works like a general text editor.
1. Display the Preview
    - Activate the window of the file you want to preview, then press `ctrl+shift+V`.
        - Alternatively, you can click the magnifying glass icon in the top right of the window to display the preview.
1. Save the Markdown File
    - Press `ctrl+S`.
1. Output in HTML Format
    - Press the shortcut key set during the initial setup.


## Conclusion
I introduced the automatic conversion from Markdown to HTML using VSCode. VSCode and Markdown are very user-friendly, so please give them a try!