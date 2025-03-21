from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory
from qt import Ui_MainWindow
from translate import Translator
import requests
import configparser
import os
import sys

# Reading
CONFIG_FILE = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8"): pass
    if not config.has_section("config"):
        config.add_section("config")
    config.set("config", "lang", "en")
    with open(CONFIG_FILE, "w", encoding="utf-8") as data: config.write(data)

language = config.get("config", "lang")
translator = Translator(to_lang="uk")

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEdit.setReadOnly(True)
        self.ui.pushButton.clicked.connect(self.clickedButton)
        self.ui.pushButton_2.clicked.connect(self.clickedButton2)

    def clickedButton(self):
        response = requests.get("https://catfact.ninja/fact").json()
        fact = response["fact"]
        factua = translator.translate(fact)
        if language == "ua":
            self.ui.textEdit.setPlainText(factua)
        if language == "en":
            self.ui.textEdit.setPlainText(fact)
    
    def clickedButton2(self):
        config.read(CONFIG_FILE)
        selected_language = self.ui.comboBox.currentText()
        if selected_language == "Українська мова":
            new_lang = "ua"
        elif selected_language == "English language":
            new_lang = "en"

        config.set("config", "lang", new_lang)
        with open(CONFIG_FILE, "w", encoding="utf-8") as data: config.write(data)

        global language
        language = new_lang
        self.clickedButton()
    
app = QApplication([])
window = MyWindow()
window.show()
app.exec()