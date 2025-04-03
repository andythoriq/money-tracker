import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout,
    QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, pyqtSignal

class SlidingStackedWidget(QStackedWidget):
    """QStackedWidget dengan efek slide animasi antar halaman."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setDuration(500)  # durasi 500ms
        self._currentIndex = 0

    def slideToIndex(self, newIndex, direction='right'):
        """Animasi dari halaman saat ini ke halaman newIndex."""
        if newIndex < 0 or newIndex >= self.count():
            return
        
        # Halaman saat ini dan halaman tujuan
        oldWidget = self.currentWidget()
        newWidget = self.widget(newIndex)
        
        if oldWidget == newWidget:
            return  # Tidak perlu animasi kalau sama

        self._currentIndex = newIndex
        self.setCurrentIndex(newIndex)
        
        # Kita animasikan QStackedWidget itu sendiri, 
        # atau bisa juga animasikan 'pos' child widget
        startRect = self.geometry()
        endRect = QRect(startRect)

        screenWidth = self.parent().width() if self.parent() else 400

        if direction == 'right':
            # Geser halaman baru dari kanan
            # Start: widget di posisi x = +screenWidth
            self.move(startRect.x() + screenWidth, startRect.y())
            endRect.moveLeft(startRect.x())
        else:
            # Geser halaman baru dari kiri
            self.move(startRect.x() - screenWidth, startRect.y())
            endRect.moveLeft(startRect.x())
        
        self.animation.stop()
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(endRect)
        self.animation.start()