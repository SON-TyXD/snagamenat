from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import client
from map import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

defalutport = 9918
defalutname = "Player"
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.c = client.ClientSocket(self)

        self.initUI()

    def __del__(self):
        self.c.stop()

    def initUI(self):
        self.setWindowTitle('스네이크 게임 클라이언트')

        ipbox = QHBoxLayout()

        gb = QGroupBox('서버 입력')
        ipbox.addWidget(gb)

        box = QHBoxLayout()

        label = QLabel('Server IP')
        self.ip = QLineEdit()
        self.ip.setInputMask('000.000.000.000;_')
        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(defalutport))
        box.addWidget(label)
        box.addWidget(self.port)

        label = QLabel('ID')
        self.name = QLineEdit(str(defalutname))
        box.addWidget(label)
        box.addWidget(self.name)

        self.btn = QPushButton('접속')
        self.btn.clicked.connect(self.connectClicked)
        box.addWidget(self.btn)

        gb.setLayout(box)

        infobox = QHBoxLayout()
        gb = QGroupBox('')
        infobox.addWidget(gb)

        box = QVBoxLayout()

        label = QLabel('채팅방')
        box.addWidget(label)

        self.recvmsg = QListWidget()
        box.addWidget(self.recvmsg)

        label = QLabel('메시지 입력')
        box.addWidget(label)

        self.sendmsg = QTextEdit()
        self.sendmsg.setFixedHeight(50)
        box.addWidget(self.sendmsg)

        hbox = QHBoxLayout()

        box.addLayout(hbox)
        self.sendbtn = QPushButton('보내기')
        self.sendbtn.setAutoDefault(True)
        self.sendbtn.clicked.connect(self.sendMsg)

        self.clearbtn = QPushButton('초기화')
        self.clearbtn.clicked.connect(self.clearMsg)

        hbox.addWidget(self.sendbtn)
        hbox.addWidget(self.clearbtn)
        gb.setLayout(box)

        # 클라이언트 설정 부분
        gamebox = QHBoxLayout()

        gb = QGroupBox('스네이크 게임')
        gamebox.addWidget(gb)

        box = QHBoxLayout()

        self.gamebtn = QPushButton('게임 플레이')
        self.gamebtn.clicked.connect(self.openGameClass)
        box.addWidget(self.gamebtn)
        self.gamebtn.setFont(QFont('Times', 80))
        self.gamebtn.setFixedHeight(200)
        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(infobox)
        vbox.addLayout(gamebox)
        self.setLayout(vbox)

        self.show()

    def connectClicked(self):
        if self.c.bConnect == False:
            ip = self.ip.text()
            port = self.port.text()
            if self.c.connectServer(ip, int(port)):
                self.btn.setText(self.name.text() + ' 접속 종료')
                playermsg = "System : " + self.name.text() + "님이 입장하셨습니다."
                self.c.send(playermsg)
            else:
                self.c.stop()
                self.sendmsg.clear()
                self.recvmsg.clear()
                self.btn.setText('접속')
                playermsg = "System : " + self.name.text() + "님이 퇴장하셨습니다."
                self.c.send(playermsg)
        else:
            self.c.stop()
            self.sendmsg.clear()
            self.recvmsg.clear()
            self.btn.setText('접속')
            playermsg = "System : " + self.name.text() + "님이 퇴장하셨습니다."
            self.c.send(playermsg)

    def updateMsg(self, msg):
        self.recvmsg.addItem(QListWidgetItem(msg))

    def updateDisconnect(self):
        self.btn.setText('접속')

    def sendMsg(self):
        sendmsg = self.name.text() + " : " + self.sendmsg.toPlainText()
        self.c.send(sendmsg)
        self.sendmsg.clear()

    def clearMsg(self):
        self.recvmsg.clear()


    def closeEvent(self, e):
        self.c.stop()

    def openGameClass(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class SnakeWidget(QWidget):
    endSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.initUI()

    def __del__(self):
        pass

    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('스네이크 게임')
        self.setFixedSize(self.rect().size())

        self.map = CMap(self)

        self.endSignal.connect(self.ExitGame)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.map.draw(qp)
        qp.end()

    def keyPressEvent(self, e):
        self.map.keydown(e.key())

    def ExitGame(self):
        result = QMessageBox.information(self
                                         , '게임 종료'
                                         , '다시 시작 : Yes\n메인 메뉴로 돌아가기 : No'
                                         , QMessageBox.Yes | QMessageBox.No)

        if result == QMessageBox.Yes:
            self.map.reStart()
        else:
            self.map.reStart()
            widget.setCurrentIndex(widget.currentIndex()-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QStackedWidget()

    mw = MainWidget()
    sw = SnakeWidget()

    widget.addWidget(mw)
    widget.addWidget(sw)

    widget.show()

    sys.exit(app.exec_())