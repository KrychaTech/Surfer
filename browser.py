from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import *
import sys
import random
import argparse
import keyboard

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

class Back_Action(QObject):
    back_signal = pyqtSignal()
    def start(self):
        keyboard.add_hotkey("win+j", self.back_signal.emit, suppress=True)

class Exit_Action(QObject):
    exit_signal = pyqtSignal()
    def start(self):
        keyboard.add_hotkey("win+x", self.exit_signal.emit, suppress=True) 

class Search_Action(QObject):
    search_signal = pyqtSignal()
    def start(self):
        keyboard.add_hotkey("win+r", self.search_signal.emit, suppress=True)


class Tabs(QObject):
    tab_left = pyqtSignal()
    tab_right = pyqtSignal()
    new_tab_signal = pyqtSignal()
    clear_tab_signal = pyqtSignal()
    def start(self):
        keyboard.add_hotkey("win+left", self.tab_left.emit, suppress=True)
        keyboard.add_hotkey("win+right", self.tab_right.emit, suppress=True)
        keyboard.add_hotkey("win+t",  self.new_tab_signal.emit, suppress=True)
        keyboard.add_hotkey("win+y", self.clear_tab_signal.emit, suppress=True)


# THERE CERTAINLY IS NOT OTHER POSSIBLE METHOD TO WRITE THIS

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


        # define shortcuts - win+j for back, win+x for exit, win+r for returning to ddg or google
        back = Back_Action(self)
        back.back_signal.connect(self.browser.back)
        back.start()

        leave = Exit_Action(self)
        leave.exit_signal.connect(app.quit)
        leave.start()

        search = Search_Action(self)
        search.search_signal.connect(return_to_search)
        search.start()

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