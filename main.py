import sys
from PyQt5.QtWidgets import QApplication
from pages.view_splashscreen import SplashScreen
from pages.view_dashboard import Dashboard, load_stylesheet
from PyQt5.QtCore import QTimer

if __name__ == '__main__':
    app = QApplication(sys.argv)

    load_stylesheet(app)

    # Create and show splash screen
    splash = SplashScreen()
    splash.show()

    # Load main window after delay
    def start_main_window():
        splash.close()  # Close splash screen
        dashboard = Dashboard()
        dashboard.show()

    # Set delay before opening main window (e.g., 3 seconds)
    QTimer.singleShot(3000, start_main_window)

    sys.exit(app.exec_())
