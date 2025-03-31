import sys, os
from PyQt5.QtWidgets import QApplication
from pages.view_splashscreen import SplashScreen
from PyQt5.QtGui import QPalette, QColor
from pages.Dashboard_v1_2 import Dashboard
from PyQt5.QtCore import QTimer

def load_stylesheet(app, file):
    filename="styles/"+file+".qss"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            qss = file.read()
            app.setStyleSheet(qss)
    else:
        print(f"Warning: Stylesheet {filename} not found!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#252931"))

    splash = SplashScreen()
    splash.show()

    def start_main_window():
        splash.close()  
        load_stylesheet(app,"style")
        dashboard = Dashboard()
        dashboard.show()

    QTimer.singleShot(3000, start_main_window)

    sys.exit(app.exec_())
