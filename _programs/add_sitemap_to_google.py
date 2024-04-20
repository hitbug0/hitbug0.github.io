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
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST))
        main_monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(0, win32con.MONITOR_DEFAULTTOPRIMARY))
        if monitor_info['Device'] == main_monitor_info['Device']:
            break
        else:
            # hwndを表示するモニターを切り替える
            win32gui.MoveWindow(hwnd, main_monitor_info['Monitor'][0], main_monitor_info['Monitor'][1], monitor_info['Monitor'][2]-monitor_info['Monitor'][0], monitor_info['Monitor'][3]-monitor_info['Monitor'][1], True)
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