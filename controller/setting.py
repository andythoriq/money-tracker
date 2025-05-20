# from config.config_handler import load_config, save_config
# from config.translation import load_translation, get_available_languages
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QColorDialog, QVBoxLayout, QTextEdit,
    QHBoxLayout, QDialog, QComboBox, QDialogButtonBox, QWidget
)
from PyQt5.QtCore import QSettings, QObject, QUrl, pyqtSignal, QTimer
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json, os, sys, requests
from googletrans import Translator, LANGUAGES
from PyQt5.QtGui import QColor, QIcon

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
class LanguageDialog(QDialog):
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

# Get the path to the 'config.json' file located in the 'locales' folder
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "config.json"))
LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "lang"))
THEME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locales", "theme"))

class Setting:
    def __init__(self, view=None):
        self.view = view

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
        else:
            theme.setIcon(QtGui.QIcon("../money-tracker/img/icon/moon.svg"))

    def load_theme(self, theme, directory="locales/theme"):
        path = os.path.join(directory, f"{theme}.qss")
        
        if os.path.exists(path):
            with open(path, "r") as file:
                qss = file.read()
                self.view.setStyleSheet(qss)
        else:
            print(f"Warning: Stylesheet {path} not found!")

# ====== Settings Window ======
class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent # simpan referensi pemanggil
        self.setWindowTitle("Settings")

        # Buat settings
        self.settings = QSettings("Kelompok1A", "MoneyTracker")
        self.logic = Setting(self.parent_window)

        # UI
        layout = QVBoxLayout()

        self.label_desc1 = QLabel("Language")
        self.label_desc1.setStyleSheet("font-size: 10px;")

        self.label_language = QLabel("Hello, welcome to our app!")
        self.label_language.setStyleSheet("font-size: 18px;")

        self.lang_btn = QPushButton("Pengaturan Bahasa")
        self.lang_btn.clicked.connect(self.open_language_settings)

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
        self.dark_button.clicked.connect(lambda : self.logic.load_theme("dark"))
        self.light_button.clicked.connect(lambda : self.logic.load_theme("light"))
        self.mono_button.clicked.connect(lambda : self.logic.load_theme("mono"))

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
        layout.addWidget(self.label)
        layout.addWidget(self.check_btn)
        layout.addWidget(theme_widget)
        layout.addWidget(self.btn)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def load_and_apply_qss(self, window, base_color: QColor, saved_color: str, path="locales/theme/customize.qss"):
        with open(path, "r") as file:
            qss = file.read()

        # Gantikan placeholder dengan nilai warna aktual
        qss = qss.replace("$saved_color", saved_color)
        qss = qss.replace("$base_color_darker130", base_color.darker(130).name())
        qss = qss.replace("$base_color_darker140", base_color.darker(140).name())
        qss = qss.replace("$base_color_darker150", base_color.darker(150).name())
        qss = qss.replace("$base_color_lighter150", base_color.lighter(150).name())

        window.setStyleSheet(qss)

    def check_internet(self):
        self.label.setText("Status koneksi: Memeriksa...")
        self.checker.check()

    def update_status(self, is_connected):
        if is_connected:
            self.label.setText("Status koneksi: Terhubung ✅")
            self.lang_btn.setEnabled(True)
        else:
            self.label.setText("Status koneksi: Tidak Terhubung ❌")
            self.lang_btn.setEnabled(False)

    def open_language_settings(self):
        dialog = LanguageDialog(self)
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

    def choose_color(self):
        dialog = QColorDialog(self)
        dialog.currentColorChanged.connect(lambda color: self.preview_color(color))
        dialog.colorSelected.connect(lambda color: self.save_color(color))
        dialog.open()
        if dialog.exec_():
            # Load warna yang tersimpan untuk tombol ini
            color_key = "global_color"
            saved_color = self.settings.value(color_key, '')
            base_color = QColor(saved_color)
            self.load_and_apply_qss(self.parent_window, base_color, saved_color)


    def preview_color(self, color):
        self.btn.setStyleSheet(f"background-color: {color.name()};")

    def save_color(self, color):
        color_name = color.name()
        self.settings.setValue("global_color", color_name)

class Translation:
    FILE_PATH = "locales/lang/en.json"

    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.load_json_texts()
        self.init_ui()

    def load_json_texts(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, self.FILE_PATH)

            with open(json_path, "r", encoding="utf-8") as f:
                self.json_texts = json.load(f)

        except Exception as e:
            print(f"Error loading JSON: {e}")

    def init_ui(self):
        layout = QVBoxLayout()

        # Tampilkan 3 label contoh dari JSON
        self.label1 = QLabel(self.json_texts.get("label1", ""))
        self.label2 = QLabel(self.json_texts.get("label2", ""))
        self.label3 = QLabel(self.json_texts.get("label3", ""))

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)

        # Input text
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text here...")
        layout.addWidget(QLabel("Original Text:"))
        layout.addWidget(self.input_text)

        # Language selection
        lang_layout = QHBoxLayout()
        self.source_lang = QComboBox()
        self.target_lang = QComboBox()

        lang_names = list(LANGUAGES.values())
        self.source_lang.addItems(["auto"] + lang_names)
        self.target_lang.addItems(lang_names)

        self.source_lang.setCurrentText("auto")
        self.target_lang.setCurrentText("english")

        lang_layout.addWidget(QLabel("From:"))
        lang_layout.addWidget(self.source_lang)
        lang_layout.addWidget(QLabel("To:"))
        lang_layout.addWidget(self.target_lang)
        layout.addLayout(lang_layout)

        # Translate button
        self.translate_btn = QPushButton("Translate All JSON Values")
        self.translate_btn.clicked.connect(self.translate_all_json_texts)
        layout.addWidget(self.translate_btn)

        # Output text
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(QLabel("Translated JSON Values:"))
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def translate_all_json_texts(self):
        src = self.get_lang_code(self.source_lang.currentText())
        dest = self.get_lang_code(self.target_lang.currentText())

        try:
            translated_json = self.recursive_translate(self.json_texts, src, dest)
            formatted = json.dumps(translated_json, indent=2, ensure_ascii=False)
            self.output_text.setText(formatted)

            # OPTIONAL: Simpan hasil ke file
            save_path = f"locales/lang/online.json"
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(translated_json, f, ensure_ascii=False, indent=2)
            print(f"Translated JSON saved to: {save_path}")
        except Exception as e:
            self.output_text.setText(f"Error: {e}")

    def recursive_translate(self, data, src, dest):
        if isinstance(data, dict):
            return {k: self.recursive_translate(v, src, dest) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.recursive_translate(item, src, dest) for item in data]
        elif isinstance(data, str):
            try:
                return self.translator.translate(data, src=src, dest=dest).text
            except Exception as e:
                return f"[Error: {e}]"
        else:
            return data  # return unchanged for non-str types

    def get_lang_code(self, name):
        if name == "auto":
            return "auto"
        for code, lang in LANGUAGES.items():
            if lang.lower() == name.lower():
                return code
        return "en"
