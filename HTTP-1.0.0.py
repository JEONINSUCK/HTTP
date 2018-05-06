from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import socket
import sys

Form = uic.loadUiType("GUI_HTTP.ui")[0]

class MyMain(QtWidgets.QMainWindow,Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.switch = 0
        # 초기 세팅 값
        self.Header_Text_Edit.setText(
            "GET / HTTP/1.1\r\nHOST: www." + "\r\n\r\n")

        # 메소드 연결
        self.Address_Edit.textChanged.connect(self.Changed_Address_Edit)
        self.Send_Request_Button.clicked.connect(self.Button_Clicked)
        # self.Header_Checkbox.stateChanged.connect(self.CheckBox_Process)
        # self.Address_Edit.returnPressed.connect(self.Button_Clicked) Enter 버튼

    # 키보드 입력 처리
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter -1:
            self.Button_Clicked()

    def Changed_Address_Edit(self,M):
        if (self.Address_Edit.text().find("www.") == 0) & (self.switch == 0):
            self.switch = 1
            self.Header_Text_Edit.setText(
                "GET / HTTP/1.1\r\nHOST: " + M + "\r\n\r\n")
        elif self.Address_Edit.text().find("/") != -1:
            self.directory = M[self.Address_Edit.text().find("/"):] + " "
            self.Header_Text_Edit.setText(
                "GET " + self.directory + "HTTP/1.1\r\nHOST: " + M[:self.Address_Edit.text().find("/")] + "\r\n\r\n")
        else:
            self.Header_Text_Edit.setText(
            "GET / HTTP/1.1\r\nHOST: www." + M + "\r\n\r\n")
        self.string = ("GET / HTTP/1.1\r\nHOST: www." + M + "\r\n\r\n")

    def Button_Clicked(self):
        self.SOCKET = socket.socket()
        self.SOCKET.settimeout(5)
        self.data = b''
        if self.Address_Edit.text().find("www.") == 0:
            self.HOST = self.Address_Edit.text()
        else:
            self.HOST = "www." + self.Address_Edit.text()

        try:
            self.SOCKET.connect((self.HOST,80))
        except (NameError, socket.gaierror, socket.timeout):
            QtWidgets.QMessageBox.about(self,"ERROR","Cannot connect the Host")
        else:
            self.Header_Text = (self.Header_Text_Edit.toPlainText()).replace("\n","\r\n")
            self.SOCKET.send((self.Header_Text).encode())

            while True:
                self.Buf = self.SOCKET.recv(2048)
                self.data += self.Buf
                if len(self.Buf) < 2048:
                    break
            self.Response_Browser.setText(self.data.decode("unicode_escape"))

            self.data = (self.data.decode("unicode_escape")).split("\r\n\r\n")
        finally:
            self.SOCKET.close()
            for i in range(len(self.data)):
                print(i)
                print(self.data[i])
            self.CheckBox_Process()
    def CheckBox_Process(self):
        if self.Header_Checkbox.isChecked():
            self.Response_Browser.setText(self.data[0])
        elif self.Contects_Checkbox.isChecked():
            self.Response_Browser.setText(self.data[2])
        elif self.Session_Checkbox.isChecked():
            pass
        elif self.Cookie_Checkbox.isChecked():
            pass
        else:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyMain()
    ui.show()
    sys.exit(app.exec_())