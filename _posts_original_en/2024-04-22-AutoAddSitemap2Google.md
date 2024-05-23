# Automating Screen Operations with Python (Includes Various Code Snippets for Beginners)
::tags{RPA, Python, Web Development}::

---

This article introduces methods to automate screen operations with Python.  
The example used here is "Registering an XML file with Google Search Console," but these methods can be applied to other scenarios as well, such as "performing the same operation repeatedly with software created by historical figures."  
(Note: These methods are based on recent versions of Windows, so they may not work on other operating systems or older versions of Windows. Please be aware of this...!)

## What You Will Learn from This Article
- How to automate screen operations with Python
  - Basic commands
  - Handy functions
- Automation Example: Automating the process of registering an XML sitemap with Google Search Console
  - Step-by-step procedure
  - Code for automation
  - Execution results (video)

## What Tools Are Used for Automation?
Various operations can be automated with Python.  
In this article, the following libraries were used.  
While these libraries alone can achieve quite a bit, there are many other useful libraries out there.

- **PyAutoGUI**
  - Automates GUI operations such as mouse movement and clicks, and keyboard inputs.
- **pyperclip**
  - Allows reading and writing to the clipboard.
- **subprocess**
  - Can start external processes and manipulate their input/output.
  - Especially useful for executing command prompt operations within Python.
  - It's a standard Python library, so no separate installation is required.
- **win32gui, win32con, win32api**
  - Allows access to Windows GUI elements and system resources.
- **time**
  - Provides functionalities such as obtaining the current time, pausing execution (sleep), performance measurement, converting time expressions, and performing time arithmetic.
  - It's a standard Python library, so no separate installation is required.

Here are the installation commands.  
Note that `win32***` libraries are bundled and installed with `pywin32`!

```
pip install pyperclip
pip install pyautogui
pip install pywin32
```

## What Operations Can Be Automated?
Here are some simple specific examples of the automation code used in this article.  
These are just a few examples, but there are many other things you can automate!

### Pressing Keys
With PyAutoGUI, you can automate the pressing of one or more keys.  
There are many other keys you can press, so feel free to explore further!

```Python
import pyautogui as pa

pa.hotkey('alt','d') # Focus the URL input field in Google Chrome
pa.hotkey('f5') # Refresh the page in the browser
```

### Typing Text
You can use PyAutoGUI and pyperclip to type text.  
To avoid issues with switching between Japanese/English input modes, it's better to use the "copy to clipboard and paste" method.

```Python
import pyautogui as pa
import pyperclip

pyperclip.copy("hoge, hoge") # Copy text to clipboard
pa.hotkey('ctrl','v') # Paste the text
```

### Locating an Image on the Screen and Clicking
PyAutoGUI can search for images on the screen.  
If found, it returns the center coordinates of the image's location.

```Python
import pyautogui as pa

position_im = pa.locateOnScreen(img, confidence=0.8)
```

In this example, I defined a `wait_disp` function to wait for an image to appear.  
Here's how it's used:

```Python
import pyautogui as pa

def wait_disp(img, wait_time=10):
    # Waits for an image to appear on the screen. Returns the image's location if found.
    dt = 0.5
    for i in range(int(wait_time/dt)):
        position_im = pa.locateOnScreen(img, confidence=0.8)
        if position_im:
            return position_im
        else:
            time.sleep(dt)
    return False

position_im = wait_disp('./hoge.png') # Search for hoge.png on the screen
pa.click(position_im, button='left', clicks=1) # Left-click the center of hoge.png
```

### Launching Applications
You can use subprocess to launch specified applications.  
For example, you can start Google Chrome with the following code.

```Python
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
subprocess.Popen(chrome_path)
```

### Adjusting Application Display Position/Screen, Maximizing, etc.
Using win32gui, win32con, and win32api, you can adjust the display state of applications.  
Sometimes, you may need to specify the window size if the buttons to be displayed are not visible in a small window.  
I'll skip the detailed explanation here!

```Python
import win32gui
import win32con
import win32api

def get_chrome_window():
    # Retrieves the handle of the most recently opened Chrome window.
    chrome_windows = []
    def enum_handler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and 'chrome' in win32gui.GetWindowText(hwnd).lower():
            chrome_windows.append(hwnd)
    win32gui.EnumWindows(enum_handler, None)
    return chrome_windows[0] if chrome_windows else None

def move_to_main_screen(hwnd, wait_time=10):
    # Switches the display monitor to the main device.
    dt = 0.5
    n = wait_time/dt
    count=0
    while count<=n:
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST))
        main_monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(0, win32con.MONITOR_DEFAULTTOPRIMARY))
        if monitor_info['Device'] == main_monitor_info['Device']:
            break
        else:
            # Switch the monitor displaying hwnd
            win32gui.MoveWindow(hwnd, 0, 0, 500, 500, True) # Position the window at 500*500 from the top left corner
            time.sleep(dt)
            count +=1

# Adjusting the display window
chrome_window = None
while not chrome_window:
    chrome_window = get_chrome_window()
    time.sleep(0.5)

move_to_main_screen(chrome_window) # Open in the main screen
time.sleep(0.5)

win32gui.ShowWindow(chrome_window, win32con.SW_MAXIMIZE) # Maximize the window
```

## What Operations Are Automated This Time?
This time, the operation being automated is the registration of an XML sitemap with Google Search Console.  
Specifically, the operation involves the following steps:

1. Launch Google Chrome

1. Adjust the display window
    - Open in the main window
    - Maximize the window
1. Enter the Google Search Console URL in the URL field of Google Chrome and press the `Enter` key
1. Confirm that the Google Search Console page has opened
    - Find `sitemap1.png` on the screen
1. Enter the file name (sitemap.xml) in the specified field
    - After clicking `sitemap1.png` to focus on the input field, press the `Tab` key
    - Copy the file name to the clipboard and paste it into the input field
1. Click the submit button (`sitemap2.png`)
1. Confirm that the submission process is complete and refresh the page
    - When `sitemap3.png` (the button to close the submission completion popup) appears, click it
    - Wait for a moment and then press the `F5` key

Here are the images used as triggers for the automated operations.
::img{
    file{
        sitemap1.png: sitemap1.png (Image of text on the page);
        sitemap2.png: sitemap2.png (Submit button);
        sitemap3.png: sitemap3.png (Button to close the popup);
    }
    height: 80px;
}::

## What Does the Code Look Like?
Here's the code!  
At the very least, replace the URL at the beginning with your own!

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
    # Waits for an image to appear on the screen. Returns the image's location if found.
    dt = 0.5
    for i in range(int(wait_time/dt)):
        position_im = pa.locateOnScreen(img, confidence=0.8)
        if position_im:
            return position_im
        else:
            time.sleep(dt)
    return False

def get_chrome_window():
    # Retrieves the handle of the most recently opened Chrome window.
    chrome_windows = []
    def enum_handler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and 'chrome' in win32gui.GetWindowText(hwnd).lower():
            chrome_windows.append(hwnd)
    win32gui.EnumWindows(enum_handler, None)
    return chrome_windows[0] if chrome_windows else None

def move_to_main_screen(hwnd, wait_time=10):
    # Switches the display monitor to the main device.
    dt = 0.5
    n = wait_time/dt
    count=0
    while count<=n:
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow

(hwnd, win32con.MONITOR_DEFAULTTONEAREST))
        main_monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(0, win32con.MONITOR_DEFAULTTOPRIMARY))
        if monitor_info['Device'] == main_monitor_info['Device']:
            break
        else:
            # Switch the monitor displaying hwnd
            win32gui.MoveWindow(hwnd, 0, 0, 500, 500, True) # Position the window at 500*500 from the top left corner
            time.sleep(dt)
            count +=1

def main():
    # Execute command to launch Google Chrome
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    subprocess.Popen(chrome_path)
    
    # Adjust the display window
    time.sleep(0.5)  # Wait time for Chrome to launch
    chrome_window = None
    while not chrome_window:
        chrome_window = get_chrome_window()
        time.sleep(0.5)
    
    move_to_main_screen(chrome_window) # Open in the main screen
    time.sleep(0.5)
    
    win32gui.ShowWindow(chrome_window, win32con.SW_MAXIMIZE) # Maximize the window
    time.sleep(0.5)
    
    # Enter URL
    pa.hotkey('alt','d')
    time.sleep(2)
    pyperclip.copy(URL)
    pa.hotkey('ctrl','v')
    time.sleep(0.05)
    pa.hotkey('enter')

    # Find and click sitemap1.png on the screen
    time.sleep(0.05)
    position_im = wait_disp('./contents/img/sitemap1.png')
    pa.click(position_im, button='left', clicks=1)
    
    # Enter file name and submit
    pa.hotkey('tab')
    time.sleep(0.05)
    pyperclip.copy("sitemap.xml")
    pa.hotkey('ctrl','v')
    time.sleep(0.05)
    position_im = wait_disp('./contents/img/sitemap2.png')
    pa.click(position_im, button='left', clicks=1)
    
    # Refresh page after submission is complete
    position_im = wait_disp('./contents/img/sitemap3.png', wait_time=40)
    time.sleep(0.05)
    pa.click(position_im, button='left', clicks=1)
    time.sleep(1)
    pa.hotkey('f5')

main()
```

## What Does the Execution Result Look Like?
I'll upload a video soon!

## Summary
Using the example of "registering an XML file with Google Search Console," I introduced a method to automate screen operations with Python.  
This method can be useful in scenarios like "performing the same operation repeatedly with software created by historical figures."  
I have personally used this method for work several times, so if you find it useful, please give it a try!