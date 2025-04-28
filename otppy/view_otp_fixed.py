from PyQt5 import QtCore, QtWidgets, QtGui
from otp_fixed import Otp
import time


class Ui_otpgui(object):
    def setupUi(self, otpgui, key_dict):
        otpgui.setObjectName("otpgui")
        otpgui.resize(261, 220)
        otpgui.setAcceptDrops(False)

        self.otp_backend = Otp()
        self.emailin = QtWidgets.QLineEdit(otpgui)
        self.emailin.setGeometry(QtCore.QRect(10, 40, 241, 31))
        self.emailin.setObjectName("inputemail")
        self.otpin = QtWidgets.QLineEdit(otpgui)
        self.otpin.setGeometry(QtCore.QRect(10, 110, 241, 31))
        self.otpin.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(otpgui)
        self.label.setGeometry(QtCore.QRect(10, 10, 241, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(otpgui)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 241, 17))
        self.label_2.setObjectName("label_2")

        # Tambahkan label untuk cooldown
        self.cooldown_label = QtWidgets.QLabel(otpgui)
        self.cooldown_label.setGeometry(QtCore.QRect(10, 150, 241, 17))
        self.cooldown_label.setObjectName("cooldown_label")
        self.cooldown_label.setStyleSheet("color: red;")
        self.cooldown_label.hide()

        self.pushButton = QtWidgets.QPushButton(otpgui)
        self.pushButton.setGeometry(QtCore.QRect(190, 190, 61, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.clicked.connect(
            lambda: self.verify_otp(self.otpin.text().strip(), key_dict)
        )
        self.pushButton_2 = QtWidgets.QPushButton(otpgui)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 190, 171, 25))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(
            lambda: self.send_otp(self.emailin.text().strip(), key_dict)
        )

        # Timer untuk update cooldown
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_cooldown)

        self.retranslateUi(otpgui)
        QtCore.QMetaObject.connectSlotsByName(otpgui)

    def update_cooldown(self):
        cooldown_active, remaining_time = self.otp_backend.is_cooldown_active()
        if cooldown_active:
            self.cooldown_label.setText(
                f"Harap tunggu {remaining_time} detik sebelum mengirim OTP lagi"
            )
            self.cooldown_label.show()
            self.pushButton_2.setEnabled(False)
        else:
            self.cooldown_label.hide()
            self.pushButton_2.setEnabled(True)
            self.timer.stop()

    def send_otp(self, email, key_dict):
        if self.otp_backend.startsmtp(email, key_dict):
            self.timer.start(1000)  # Update setiap detik
            self.pushButton_2.setEnabled(False)

    def verify_otp(self, user_otp, key_dict):
        result = self.otp_backend.otpcheck(user_otp, key_dict["key"])
        if result:
            # Jika OTP benar, lakukan sesuatu di sini
            pass

    def retranslateUi(self, otpgui):
        _translate = QtCore.QCoreApplication.translate
        otpgui.setWindowTitle(_translate("otpgui", "Pemulihan Password"))
        self.label.setText(
            _translate("otpgui", "Masukan E-mail anda yang telah terdaftar")
        )
        self.label_2.setText(_translate("otpgui", "Masukan Kode Otp"))
        self.pushButton.setText(_translate("otpgui", "Cek OTP"))
        self.pushButton_2.setText(_translate("otpgui", "Kirim Kode"))
        self.cooldown_label.setText(_translate("otpgui", ""))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    otpgui = QtWidgets.QWidget()
    ui = Ui_otpgui()
    key_dict = {"key": ""}
    ui.setupUi(otpgui, key_dict)
    print(key_dict["key"])
    otpgui.show()
    sys.exit(app.exec_())

