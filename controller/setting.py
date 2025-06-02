# from config.config_handler import load_config, save_config
# from config.translation import load_translation, get_available_languages
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QColorDialog, QVBoxLayout, QRadioButton, QStackedWidget,
    QHBoxLayout, QDialog, QComboBox, QDialogButtonBox, QWidget, QGroupBox, QButtonGroup
)
from PyQt5.QtCore import QSettings, QObject, QUrl, pyqtSignal, QTimer, QSize
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json, os, sys, requests
from googletrans import Translator, LANGUAGES
from PyQt5.QtGui import QColor, QIcon

# Get the path to the 'config.json' file located in the 'locales' folder
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "config.json"))
LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "lang"))
THEME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "theme"))
SRC_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "lang", "en.json"))


# ====== API Translation Function ======
def translate_text(text, target_lang):
    source_lang = "en"
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["responseData"]["translatedText"]
        else:
            return f"[Error: {response.status_code}]"
    except Exception as e:
        return f"[Translation Error: {e}]"

# ====== Language Selection Dialog ======
class RemoteLanguageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pilih Bahasa")

        self.languages = {
            "English": "en",
            "Indonesian": "id",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Japanese": "ja",
            "Chinese": "zh"
        }

        self.combo = QComboBox()
        self.combo.addItems(self.languages.keys())

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def selected_language_code(self):
        return self.languages[self.combo.currentText()]

class InternetChecker(QObject):
    internetStatusChanged = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.handle_response)

    def check(self):
        request = QNetworkRequest(QUrl("http://www.google.com"))
        self.manager.get(request)

    def handle_response(self, reply):
        if reply.error():
            self.internetStatusChanged.emit(False)
        else:
            self.internetStatusChanged.emit(True)
        reply.deleteLater()

class Setting:
    def __init__(self):
        pass

    def load_config():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Default config values when the file doesn't exist
            return {"local_language": "default", "theme_color": "light"}

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
        else:
            theme.setIcon(QtGui.QIcon("../money-tracker/img/icon/moon.svg"))

    def load_theme(self, theme, directory="locales/theme"):
        path = os.path.join(directory, f"{theme}.qss")
        
        if os.path.exists(path):
            with open(path, "r") as file:
                if theme == "customize":
                    qss = file.read()
                    # Load warna yang tersimpan untuk tombol ini
                    self.settings = QSettings("Kelompok1A", "MoneyTracker")
                    saved_color = self.settings.value("global_color", '')
                    base_color = QColor(saved_color)

                    # Gantikan placeholder dengan nilai warna aktual
                    qss = qss.replace("$saved_color", saved_color)
                    qss = qss.replace("$base_color_darker130", base_color.darker(130).name())
                    qss = qss.replace("$base_color_darker140", base_color.darker(140).name())
                    qss = qss.replace("$base_color_darker150", base_color.darker(150).name())
                    qss = qss.replace("$base_color_lighter150", base_color.lighter(150).name())
                else:
                    qss = file.read()
                return qss
        else:
            print(f"Warning: Stylesheet {path} not found!")

    def load_color(self, color, directory="locales/theme"):
        path = os.path.join(directory, "customize.qss")
        if os.path.exists(path):
            with open(path, "r") as file:
                qss = file.read()
                base_color = QColor(color)

                # Gantikan placeholder dengan nilai warna aktual
                qss = qss.replace("$saved_color", color)
                qss = qss.replace("$base_color_darker130", base_color.darker(130).name())
                qss = qss.replace("$base_color_darker140", base_color.darker(140).name())
                qss = qss.replace("$base_color_darker150", base_color.darker(150).name())
                qss = qss.replace("$base_color_lighter150", base_color.lighter(150).name())
                return qss
        else:
            print(f"Warning: Stylesheet {path} not found!")

# ====== Settings Window ======
class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        # Buat settings
        self.settings = QSettings("Kelompok1A", "MoneyTracker")
        self.logic = Setting()
        self.config = Setting.load_config()

        # UI
        Setting_widget = QWidget()
        layout = QVBoxLayout(Setting_widget)

        self.label_desc1 = QLabel("Language")
        self.label_desc1.setStyleSheet("font-size: 10px;")

        self.label_language = QLabel("Hello, welcome to our app!")
        self.label_language.setStyleSheet("font-size: 18px;")

        self.lang_btn = QPushButton("Pengaturan Bahasa")
        self.lang_btn.clicked.connect(self.open_language_settings)


        self.radioGlobal = QRadioButton("Global")
        self.radioLocal = QRadioButton("Local")
        self.comboBoxGlobal = QComboBox()
        self.comboBoxLocal = QComboBox()
        self.languageGroup = QButtonGroup()
        self.languageGroup.addButton(self.radioGlobal)
        self.languageGroup.addButton(self.radioLocal)

        self.comboBoxGlobal.addItems(["EN", "FR", "ES"])
        languages = Setting.get_available_languages()
        self.comboBoxLocal.addItems(languages)
        self.comboBoxLocal.setCurrentIndex(self.comboBoxLocal.findText(self.config.get("local_language")))
        self.comboBoxLocal.currentIndexChanged.connect(self.change_language)

        # Connect logic
        self.radioGlobal.toggled.connect(self.toggleCombos)
        self.radioLocal.toggled.connect(self.toggleCombos)

        self.toggleCombos()

        # Global section
        global_widget = QWidget()
        global_layout = QVBoxLayout(global_widget)
        global_layout.addWidget(self.radioGlobal)
        global_layout.addWidget(self.comboBoxGlobal)

        # Local section
        local_widget = QWidget()
        local_layout = QVBoxLayout(local_widget)
        local_layout.addWidget(self.radioLocal)
        local_layout.addWidget(self.comboBoxLocal)

        # Container
        language_widget = QWidget()
        language_layout = QHBoxLayout(language_widget)
        language_layout.addWidget(global_widget)
        language_layout.addWidget(local_widget)

        # Cek preferensi bahasa sebelumnya
        saved_lang = self.settings.value("language", "en")
        if saved_lang != "en":
            self.update_translation(saved_lang)

        self.label = QLabel("Status koneksi: Unknown")
        self.label.setStyleSheet("font-size: 18px;")

        self.check_btn = QPushButton("Cek Koneksi Internet")
        self.check_btn.clicked.connect(self.check_internet)

        self.checker = InternetChecker()
        self.checker.internetStatusChanged.connect(self.update_status)

        # Cek pertama kali saat mulai
        self.check_internet()

        # Auto check setiap 10 detik
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_internet)
        self.timer.start(10000)  # 10.000 ms = 10 detik

        theme_widget = QWidget()
        theme_widget.setObjectName("groupBox")
        layout_theme = QHBoxLayout(theme_widget)

        # buttons
        self.dark_button = QPushButton(QIcon("img/icon/dark.svg"), "Dark")
        self.light_button = QPushButton(QIcon("img/icon/light.svg"), "Light")
        self.mono_button = QPushButton(QIcon("img/icon/mono.svg"), "Mono")
        self.dark_button.clicked.connect(lambda : self.set_dark_theme())
        self.light_button.clicked.connect(lambda : self.set_light_theme())
        self.mono_button.clicked.connect(lambda : self.set_mono_theme())

        layout_theme.addWidget(self.dark_button)
        layout_theme.addWidget(self.light_button)
        layout_theme.addWidget(self.mono_button)

        self.btn = QPushButton("Custom Warna")

        # Sambungkan tombol ke fungsi untuk memilih warna
        self.btn.clicked.connect(lambda : self.choose_color())
        
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.label_desc1)
        layout.addWidget(self.label_language)
        layout.addWidget(self.lang_btn)
        layout.addWidget(language_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.check_btn)
        layout.addWidget(theme_widget)
        layout.addWidget(self.btn)
        layout.addWidget(self.buttonBox)

        # Layout utama
        main_layout = QHBoxLayout()
        main_layout.addWidget(Setting_widget)
        self.mini_window = MiniMainWindow()
        main_layout.addWidget(self.mini_window)
        self.setLayout(main_layout)

    def set_dark_theme(self):
        self.config["theme_color"] = "dark"
        Setting.save_config(self.config)

    def set_light_theme(self):
        self.config["theme_color"] = "light"
        Setting.save_config(self.config)

    def set_mono_theme(self):
        self.config["theme_color"] = "mono"
        Setting.save_config(self.config)

    def set_custom_theme(self):
        self.config["theme_color"] = "customize"
        Setting.save_config(self.config)

    def check_internet(self):
        self.label.setText("Status koneksi: Memeriksa...")
        self.checker.check()

    def update_status(self, is_connected):
        if is_connected:
            self.label.setText("Status koneksi: Terhubung ✅")
            self.radioGlobal.setEnabled(True)
        else:
            self.label.setText("Status koneksi: Tidak Terhubung ❌")
            self.radioGlobal.setEnabled(False)
            self.comboBoxGlobal.setEnabled(False)

    def open_language_settings(self):
        dialog = RemoteLanguageDialog(self)
        if dialog.exec_():
            lang_code = dialog.selected_language_code()
            self.settings.setValue("language", lang_code)
            self.update_translation(lang_code)

    def update_translation(self, lang_code):
        if lang_code == "en":
            self.label_language.setText("Hello, welcome to our app!")
        else:
            translated = translate_text("Hello, welcome to our app!", lang_code)
            self.label_language.setText(translated)

    def change_language(self):
        """Mengubah bahasa UI berdasarkan bahasa yang dipilih"""
        self.config["local_language"] = self.comboBoxLocal.currentText()
        Setting.save_config(self.config)
        self.language_data = Setting.load_language_file(self.comboBoxLocal.currentText())
    
    def toggleCombos(self):
        if self.radioGlobal.isChecked():
            self.comboBoxGlobal.setEnabled(True)
            self.comboBoxLocal.setEnabled(False)
        else:
            self.comboBoxGlobal.setEnabled(False)
            self.comboBoxLocal.setEnabled(True)

    def choose_color(self):
        dialog = QColorDialog(self)
        dialog.currentColorChanged.connect(lambda color: self.preview_color(color))
        dialog.colorSelected.connect(lambda color: self.save_color(color))
        dialog.move(0, 0)
        dialog.open()
        if dialog.exec_():
            self.set_custom_theme()

    def preview_color(self, color):
        self.btn.setStyleSheet(f"background-color: {color.name()};")
        self.mini_window.setStyleSheet(self.logic.load_color(color.name()))

    def save_color(self, color):
        color_name = color.name()
        self.settings.setValue("global_color", color_name)

class Translation:
    FILE_PATH = ".../locales/lang/en.json"

    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.load_json_texts()
        self.refresh_language()

    def load_json_texts(self):
        try:
            with open(SRC_FILE, "r", encoding="utf-8") as f:
                self.json_texts = json.load(f)

        except Exception as e:
            print(f"Error loading JSON: {e}")

    def init_ui(self):
        pass
        # layout = QVBoxLayout()

        # lang_names = list(LANGUAGES.values())

        # # Language selection
        # lang_layout = QHBoxLayout()
        # self.target_lang = QComboBox()
        # self.target_lang.addItems(lang_names)
        # self.target_lang.setCurrentText("english")
        # self.target_lang.currentIndexChanged.connect(self.save_remote)
        # lang_layout.addWidget(self.target_lang)
        # layout.addLayout(lang_layout)

        # # Translate button
        # self.translate_btn = QPushButton("Translate All JSON Values")
        # self.translate_btn.clicked.connect(self.translate_all_json_texts)
        # layout.addWidget(self.translate_btn)

        # self.setLayout(layout)

    def translate_all_json_texts(self):
        self.refresh_language(self)
        try:
            translated_json = self.recursive_translate(self.json_texts)

            # OPTIONAL: Simpan hasil ke file
            save_path = f"locales/lang/online.json"
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(translated_json, f, ensure_ascii=False, indent=2)
            print(f"Translated JSON saved to: {save_path}")
        except Exception as e:
            print(f"Error: {e}")

    def recursive_translate(self, data):
        src = self.src
        dest = self.dest
        if isinstance(data, dict):
            return {k: self.recursive_translate(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.recursive_translate(item) for item in data]
        elif isinstance(data, str):
            try:
                return self.translator.translate(data, src=src, dest=dest).text
            except Exception as e:
                return data
        else:
            return data  # return unchanged for non-str types

    def get_lang_code(self, name):
        for code, lang in LANGUAGES.items():
            if lang.lower() == name.lower():
                return code
        return "en"
    
    def save_remote(self):
        language = Setting.load_config()
        language["remote_language"] = self.target_lang.currentText()
        Setting.save_config(language)

    def refresh_language(self):
        self.src = "auto"
        self.target = Setting.load_config()
        self.target = self.target["remote_language"]
        self.dest = self.get_lang_code(self.target)

class MiniMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mini Money Tracker")
        self.setMinimumSize(400, 200)  # Ukuran sangat kecil

        self.stack = QStackedWidget()
        self.container = QGroupBox()

        # Sidebar kiri (mini)
        self.HomeSection = QGroupBox()
        self.HomeSection.setMinimumWidth(80)

        # Tampilan halaman kosong di stack
        self.dummy_view = QLabel("Konten")
        self.stack.addWidget(self.container)
        self.stack.addWidget(self.dummy_view)

        # Layout utama
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(4)
        main_layout.addWidget(self.HomeSection, 1)
        main_layout.addWidget(self.stack, 3)
        self.setLayout(main_layout)

        self.init_main_menu()

    def init_main_menu(self):
        layout = QVBoxLayout()

        # Tombol kecil dengan ikon kecil
        buttons = [
            ("../money-tracker/img/icon/logo-app-new.png", self.container),
            ("../money-tracker/img/icon/add-income.png", self.dummy_view),
            ("../money-tracker/img/icon/add-outcome.png", self.dummy_view),
            ("../money-tracker/img/icon/wallet.png", self.dummy_view),
            ("../money-tracker/img/icon/history.png", self.dummy_view),
            ("../money-tracker/img/icon/statistic.png", self.dummy_view),
            ("../money-tracker/img/icon/category.png", self.dummy_view),
            ("../money-tracker/img/icon/wishlist.png", self.dummy_view),
            ("../money-tracker/img/icon/aboutUs.png", self.dummy_view),
        ]

        for icon_path, target_widget in buttons:
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24, 24))  # Ukuran ikon kecil
            btn.setFixedSize(60, 24)        # Ukuran tombol kecil
            btn.clicked.connect(lambda _, w=target_widget: self.stack.setCurrentWidget(w))
            layout.addWidget(btn)

        # Tombol Tema
        self.btn_theme = QPushButton()
        self.btn_theme.setIcon(QIcon("../money-tracker/img/icon/Setting.svg"))
        self.btn_theme.setIconSize(QSize(20, 20))
        self.btn_theme.setFixedSize(30, 30)
        layout.addWidget(self.btn_theme)

        layout.addStretch()
        self.HomeSection.setLayout(layout)