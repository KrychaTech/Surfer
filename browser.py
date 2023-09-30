from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import *
import sys
import random
import argparse
import keyboard
import configparser
import pyperclip

config = configparser.ConfigParser()
config.read("config.ini")
shortcut = config['hotkeys']

# Define arguments. More can be found on the GitHub page.

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url")
parser.add_argument("-q", "--query")
parser.add_argument("-dm", "--dark_mode", action="store_true")
parser.add_argument("-g", "--google", action="store_true")
parser.add_argument("-w", "--windowed", action="store_true")
parser.add_argument("-t", "--tabbed", action="store_true")
parser.add_argument("-i", "--incognito", action="store_true")
args = parser.parse_args()

class KeyboardHandler(QObject):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    search_signal = pyqtSignal()
    copy_url = pyqtSignal()
    def start(self):
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['back_key']}", self.back_signal.emit, suppress=True)
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['exit_key']}", self.exit_signal.emit, suppress=True) 
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['return_to_search']}", self.search_signal.emit, suppress=True)
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['copy_url']}", self.copy_url.emit, suppress=True)

class Tabs(QObject):
    tab_left = pyqtSignal()
    tab_right = pyqtSignal()
    new_tab_signal = pyqtSignal()
    clear_tab_signal = pyqtSignal()
    def start(self):
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['previous_tab']}", self.tab_left.emit, suppress=True)
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['next_tab']}", self.tab_right.emit, suppress=True)
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['new_tab']}",  self.new_tab_signal.emit, suppress=True)
        keyboard.add_hotkey(f"{shortcut['control_key']}+{shortcut['reset_tabs']}", self.clear_tab_signal.emit, suppress=True)

# Updated handling of keyboard. Removed unneccessary classes.

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        with open("blocked_sites.txt", 'r') as f: 
            self.blocked_sites = f.read().split("\n")[:-1]
            print(self.blocked_sites)
        self.setWindowIcon(QtGui.QIcon('browser_icon.png'))
        self.browser = QWebEngineView()
        if args.incognito:
            self.browser.page().profile().cookieStore().deleteAllCookies()
            self.profile = QWebEngineProfile(f"cookie-{random.randint(1,9999999)}", self.browser)
            self.webpage = QWebEnginePage(self.profile, self.browser)
            self.browser.setPage(self.webpage)
        if args.query is not None:
            if args.google:
                self.browser.setUrl(QUrl(f"https://www.google.com/search?q={str(args.query).replace(' ', '+')}"))
            else:
                self.browser.setUrl(QUrl(f"https://duckduckgo.com/?q={str(args.query).replace(' ', '+')}"))
        elif args.url is not None:
            self.browser.setUrl(QUrl(args.url))
        elif args.google:
            self.browser.setUrl(QUrl("https://www.google.com"))
        else:
            self.browser.setUrl(QUrl("https://www.duckduckgo.com"))
        if args.tabbed:
            self.current_tab = 0
            self.tabs = []
        self.setCentralWidget(self.browser)
        if args.windowed:
            self.showMaximized()
        else:
            self.showFullScreen()

        # Functions for Tabs

        def new_tab():
            self.tabs.append(self.browser.url().toString())
            self.current_tab += 1
            print(f"Created tab. Current tab pointer: {self.current_tab} List of tabs: {self.tabs}")

        def clear_tabs():
            self.current_tab = 0
            self.tabs = []

        def move_tab_left():
            try:
                if self.current_tab > 0 and self.current_tab - 1 <= len(self.tabs):
                    self.current_tab -= 1
                    self.browser.setUrl(QUrl(self.tabs[self.current_tab]))
                    print(f"current tab pointer: {self.current_tab}")
            except:
                print("Too much tabs backward!")

        def move_tab_right():
            try:
                if self.current_tab >= 0 and self.current_tab + 1 <= len(self.tabs):
                    self.current_tab += 1
                    self.browser.setUrl(QUrl(self.tabs[self.current_tab]))
                    print(f"current tab pointer: {self.current_tab}")
            except:
                print("Too much tabs forward!")

        # Website blocking

        def block_websites():
            # This functions as a site blocker, redirecting users that want to procrastinate into
            # a motivational quotes website.
            for site in self.blocked_sites:
                if site in self.browser.url().toString():
                    print(f"Procrastination site {site} was found in {self.browser.url().toString()}, Blocking access and redirecting!")
                    self.browser.setUrl(QUrl("https://www.paulinaszczepanska.pl/cytaty-motywujace/"))

        
        def return_to_search():
            if args.google:
                self.browser.setUrl(QUrl("https://www.google.com"))
            else:
                self.browser.setUrl(QUrl("https:/www.duckduckgo.com"))

        def copy_url():
                pyperclip.copy(self.browser.url().toString())

        # define shortcuts - win+j for back, win+x for exit, win+r for returning to ddg or google
        keyboard_manager = KeyboardHandler(self)
        keyboard_manager.back_signal.connect(self.browser.back)
        keyboard_manager.exit_signal.connect(app.quit)
        keyboard_manager.search_signal.connect(return_to_search)
        keyboard_manager.copy_url.connect(copy_url)
        keyboard_manager.start()


        tab_manager = Tabs(self)
        tab_manager.tab_left.connect(move_tab_left)
        tab_manager.tab_right.connect(move_tab_right)
        tab_manager.new_tab_signal.connect(new_tab)
        tab_manager.clear_tab_signal.connect(clear_tabs)
        tab_manager.start()
        # wish there was a better method to do that... :/

        self.browser.page().urlChanged.connect(block_websites)

        def _downloadRequested(item):
            print('downloading to', item.path())
            item.accept()
        
        self.browser.page().profile().downloadRequested.connect(_downloadRequested)

if args.dark_mode: app = QApplication(sys.argv + ["--blink-settings=forceDarkModeEnabled=true"])
else: app = QApplication(sys.argv)
QApplication.setApplicationName("Surfer")
window = MainWindow()

app.exec_()