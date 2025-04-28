import sys
from PyQt5 import QtWidgets
from view_otp_fixed import Ui_otpgui
from otp_fixed import Otp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    otpgui = QtWidgets.QWidget()
    ui = Ui_otpgui()
    key_dict = {"key": ""}
    ui.setupUi(otpgui, key_dict)
    print(key_dict["key"])
    otpgui.show()
    sys.exit(app.exec_()) 