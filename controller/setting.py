# from config.config_handler import load_config, save_config
# from config.translation import load_translation, get_available_languages
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton
import json
import os

# Get the path to the 'config.json' file located in the 'locales' folder
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "config.json"))
LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "lang"))

class Setting:
    def __init__(self, view):
        self.view = view
        # self.config = load_config()
    #     self.translations = load_translation(self.config["language"])

    #     self.init_ui()

    # def init_ui(self):
    #     self.view.label.setText(self.translations.get("welcome", "Welcome!"))

    #     # Setup Language Dropdown
    #     langs = get_available_languages()
    #     self.view.lang_select.addItems(langs)
    #     self.view.lang_select.setCurrentText(self.config["language"])
    #     self.view.lang_select.currentTextChanged.connect(self.change_language)

    #     # Setup Theme Dropdown
    #     self.view.theme_select.setCurrentText(self.config["theme_color"])
    #     self.view.theme_select.currentTextChanged.connect(self.change_theme)
    #     self.apply_theme()

    # def change_language(self, lang):
    #     self.config["language"] = lang
    #     self.translations = load_translation(lang)
    #     self.view.label.setText(self.translations.get("welcome", "Welcome!"))
    #     save_config(self.config)

    # def change_theme(self, theme):
    #     self.config["theme_color"] = theme
    #     self.apply_theme()
    #     save_config(self.config)

    def load_config():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Default config values when the file doesn't exist
            return {"language": "en", "theme_color": "light"}

    def save_config(config):
        # Ensure the directory exists before writing to the file
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    def load_language_file(lang, fallback="en", directory="locales/lang"):
        path = os.path.join(directory, f"{lang}.json")
        fallback_path = os.path.join(directory, f"{fallback}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{lang}.json not found. Falling back to {fallback}.json")
            with open(fallback_path, "r", encoding="utf-8") as f:
                return json.load(f)

    def get_available_languages():
        return [
            file.replace(".json", "")
            for file in os.listdir(LOCALE_DIR)
            if file.endswith(".json")
        ]

    def toggle_icon(self, theme):
        if theme.isChecked():
            theme.setIcon(QtGui.QIcon("../money-tracker/img/icon/sun.svg"))
            self.view.setStyleSheet("""
            #container, #calendar, #wishlist_container, QStackedWidget, #HomeSection{    
            background-color: #FFFFFF;
            }
            QWidget, QTableWidget, QLabel{    
            color: #000000;
            }
            """)
        else:
            theme.setIcon(QtGui.QIcon("../money-tracker/img/icon/moon.svg"))
            self.view.setStyleSheet("""
            #container, #calendar, #wishlist_container, QStackedWidget {    
            background-color: #252931;
            }
            #HomeSection {    
            background-color: #121D2C;
            }
            QTableWidget, QLabel{    
            color: #FFFFFF;
            }
            """)
