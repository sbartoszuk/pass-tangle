#!/usr/bin/env python3

'''module: taskGrabber'''

from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
from pywinauto.application import Application
import psutil

web_browsers = ['chrome', 'opera', 'msedge', 'firefox', 'vivaldi', 'brave', 'duckduckgo', 'maxthon', 'browser']

web_browsers_tab = ['google chrome', 'microsoft​ edge', 'opera', 'mozilla firefox', 'vivaldi',
                    'brave', 'chromium', 'tor browser', 'duckduckgo', 'maxthon', 'yandex browser']

popular_sites = ['facebook', 'gmail', 'youtube', 'instagram', 'amazon', 'reddit', 'twitter', 'tiktok', 'netflix', 'spotify',
                 'pinterest', 'apple', 'linkedin', 'booking', 'adobe', 'allegro', 'ebay', 'craigslist', 'target',
                 'bestbuy', 'olx', 'steam']

def activeTask():
    window = GetForegroundWindow()
    tid, pid = GetWindowThreadProcessId(window)

    try:
        process = psutil.Process(pid)
    except:
        return ' '
    process_name = process.name()[:-4]
    process_name = process_name.lower()

    if process_name in web_browsers:
        to_check = True
        app = Application().connect(process=pid, time_out=10)
        dlg = app.top_window()
        site_name = dlg.wrapper_object().window_text()
        site_name = site_name.lower()
        for pop_site in popular_sites:
            if pop_site in site_name:
                site_name = pop_site
                to_check = False
                break
        if to_check:
            for browser in web_browsers_tab:
                end = len(browser)
                if site_name[-end:] == browser:
                    end += 3
                    site_name = site_name[:-end]
                    break
        return site_name
    else:
        return process_name