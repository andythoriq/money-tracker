from PyQt5 import QtCore, QtGui, QtWidgets
from otp import Otp


class otpview(object):
    def setupUi(self, Form, otp, email):
        key = otp
        otpin = Otp()
        self.resend = Otp()
        Form.setObjectName("Form")
        Form.resize(238, 82)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 221, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(180, 50, 51, 25))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(
            lambda: otpin.otpcheck(self.lineEdit.text().strip(), key["key"])
        )
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 50, 131, 25))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.resendOTP(email, key))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        print(key)

    def resendOTP(self, email, out):
        getOTP = {}
        self.resend.startsmtp(email, getOTP)
        out = getOTP
        print(out)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Masukan Kode OTP"))
        self.pushButton.setText(_translate("Form", "Lanjut"))
        self.pushButton_2.setText(_translate("Form", "Kirim Ulang Kode OTP"))
