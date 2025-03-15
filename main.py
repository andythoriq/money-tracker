import sys
from PyQt5.QtWidgets import QApplication
from pages.view_splashscreen import SplashScreen
from pages.Das
from PyQt5.QtCore import QTimer

if __name__ == '__main__':
    app = QApplication(sys.argv)

    load_stylesheet(app)

    splash = SplashScreen()
    splash.show()

    def start_main_window():
        splash.close()  
        dashboard = Dashboard()
        dashboard.show()

    QTimer.singleShot(3000, start_main_window)

    sys.exit(app.exec_())
