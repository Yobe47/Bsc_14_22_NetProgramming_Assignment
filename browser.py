# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys

#Referenced  google for the ui from geeks website

# creating main window class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # creating a QWebEngineView
        self.browser = QWebEngineView()

        # setting default browser url to be the previous assignment HTTP server
        self.browser.setUrl(QUrl("http://localhost:8085"))

        # adding action when url gets changed
        self.browser.urlChanged.connect(self.update_urlbar)

        # adding action when loading is finished
        self.browser.loadFinished.connect(self.update_title)

        # set this browser as the central widget or main window
        self.setCentralWidget(self.browser)

        # creating a status bar object
        self.status = QStatusBar()

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")

        # adding this tool bar to the main window
        self.addToolBar(navtb)

        # adding actions to the toolbar
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigationto_home)
        navtb.addAction(home_btn)

        # adding a separator in the toolbar
        navtb.addSeparator()

        # creating a line edit for the URL
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading the current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # showing all the components
        self.show()

    # method for updating the title of the window
    def updating_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - Net Programming")

    # method called by the home action
    def navigationto_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    # method for handling missing pages
    def page_not_found(self):
        html_content = """
        <html>
        <head><title>Page Not Found</title></head>
        <body>
            <h1>Page Not Found</h1>
            <p>Try searching for it on General Engine:</p>
            <p><a href='http://www.google.com'>Click here to search on Google</a></p>
        </body>
        </html>
        """
        self.browser.setHtml(html_content)

    # method called by the line edit when return key is pressed
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        if q.toString().startswith("http://localhost:8085"):
            print(f"Loading local page: {q.toString()}")  # Debugging
            self.browser.setUrl(q)
        else:
            print("Page not found! Redirecting to custom error message.")  
            self.page_not_found()

    # method for updating the URL bar
    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

# creating a PyQt5 application
app = QApplication(sys.argv)
app.setApplicationName("Simple Browser App")

# creating a main window object
window = MainWindow()

#Styling the browser app using css
app.setStyleSheet("""
    QMainWindow {
        background-color: #2E2E2E;
        color: white;
    }
    
    QToolBar {
        background: #3C3C3C;
        border: none;
    }
    
    QLineEdit {
        background: #1E1E1E;
        color: white;

    }
 """ )                                            


# loop
app.exec_()