import sys
import time

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, QFrame, QRadioButton
from PyQt5.QtCore import Qt, QTimer

from Baidu_Text_transAPI import trans
import os
import datetime

app = QApplication([])


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("mainWindow")
        qss = "QWidget#mainWindow{background-color:black;}"
        self.setStyleSheet(qss)
        self.initUI()
        self.word_box_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        self.word_box_file = open(os.path.join(self.word_box_path, "word_box.txt"), 'a+')
        self.words = []

    def initUI(self):

        self.setWindowTitle("翻译小工具by@Alphandbelt")
        self.setStyleSheet("#MainWindow{background-color: black}")
        self.setCentralWidget(QWidget())  # 指定主窗口中心部件
        self.statusBar().showMessage("ready")  # 状态栏显示信息
        # 单选按钮，是否需要记录到单词本

        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()
        self.is_word_box = QRadioButton('记录到单词本', self)
        self.label_time = QLabel(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self)
        self.label_time.setGeometry(170, 1, 120, 30)

        self.resize(300, 150)
        self.label = QLabel(self)
        self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(QtCore.QRect(51, 25, 201, 81))
        self.label.setWordWrap(True)

        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)

    def showtime(self):
        text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_time.setText(text)

    # 重新实现各事件处理程序
    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key_A <= key <= Qt.Key_Z:
            if event.modifiers() & Qt.ShiftModifier:  # Shift 键被按下
                self.statusBar().showMessage('"Shift+%s" pressed' % chr(key), 500)
            elif event.modifiers() & Qt.ControlModifier:  # Ctrl 键被按下
                self.statusBar().showMessage('"Control+%s" pressed' % chr(key), 500)
            elif event.modifiers() & Qt.AltModifier:  # Alt 键被按下
                self.statusBar().showMessage('"Alt+%s" pressed' % chr(key), 500)
            else:
                self.statusBar().showMessage('"%s" pressed' % chr(key), 500)

        elif key == Qt.Key_Home:
            self.statusBar().showMessage('"Home" pressed', 500)
        elif key == Qt.Key_End:
            self.statusBar().showMessage('"End" pressed', 500)
        elif key == Qt.Key_PageUp:
            self.statusBar().showMessage('"PageUp" pressed', 500)
        elif key == Qt.Key_PageDown:
            self.statusBar().showMessage('"PageDown" pressed', 500)
        else:  # 其它未设定的情况
            QWidget.keyPressEvent(self, event)  # 留给基类处理
        '''
        其它常用按键：
        Qt.Key_Escape,Qt.Key_Tab,Qt.Key_Backspace,Qt.Key_Return,Qt.Key_Enter,
        Qt.Key_Insert,Qt.Key_Delete,Qt.Key_Pause,Qt.Key_Print,Qt.Key_F1...Qt.Key_F12,
        Qt.Key_Space,Qt.Key_0...Qt.Key_9,Qt.Key_Colon,Qt.Key_Semicolon,Qt.Key_Equal
        ...
        '''

    def mousePressEvent(self, event):  # 鼠标按下事件
        pos = event.pos()  # 返回鼠标所在点QPoint
        self.statusBar().showMessage('Mouse is pressed at (%d,%d) of widget ' % (pos.x(), pos.y()), 500)
        globalPos = self.mapToGlobal(pos)
        print('Mouse is pressed at (%d,%d) of screen ' % (globalPos.x(), globalPos.y()))

    def mouseReleaseEvent(self, event):  # 鼠标释放事件
        pos = event.pos()  # 返回鼠标所在点QPoint
        self.statusBar().showMessage('Mouse is released at (%d,%d) of widget ' % (pos.x(), pos.y()), 500)
        if event.button() == Qt.LeftButton:
            print("左键")
        elif event.button() == Qt.MidButton:
            print("中键")
        elif event.button() == Qt.RightButton:
            print("右键")

    def mouseDoubleClickEvent(self, event):  # 鼠标双击事件
        pos = event.pos()  # 返回鼠标所在点QPoint
        self.statusBar().showMessage('Mouse is double-clicked at (%d,%d) of widget ' % (pos.x(), pos.y()), 500)

    def mouseMoveEvent(self, event):  # 鼠标移动事件
        pos = event.pos()  # 返回鼠标所在点QPoint
        self.statusBar().showMessage('Mouse is moving at (%d,%d) of widget ' % (pos.x(), pos.y()), 500)

    def change_deal(self):
        data = clipboard.mimeData()
        # 获取剪切板内容格式
        print(data.formats())
        self.statusBar().showMessage("翻译中...", 5000)
        # 如果是文本格式，把内容打印出来
        if "text/plain" in data.formats():
            # print(data.text())
            ms = trans(data.text())
            print(ms)
            self.statusBar().showMessage(data.text(), 5000)
            self.label.setText(ms)

            if self.is_word_box.isChecked():
                self.words.extend(data.text())
                # 将单词和翻译结果写入文件
                info = "原文:" + data.text() + '| 翻译:' + ms + "\n"
                if data.text() not in self.words:
                    self.word_box_file.write(info)
                    self.word_box_file.flush()
                    self.statusBar().showMessage(data.text(), 5000)
                    # time.sleep(1)
                    self.statusBar().showMessage("保存到词汇表成功!", 5000)
                    # time.sleep(1)
                    self.statusBar().showMessage(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 5000)
        else:
            print(f"data not text:{data.formats()}")
            self.statusBar().showMessage("data not text!")


if __name__ == '__main__':
    clipboard = app.clipboard()
    mw = MainWindow()

    clipboard.dataChanged.connect(mw.change_deal)
    mw.activateWindow()
    mw.setWindowState(mw.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    mw.setWindowFlags(
        QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
    # mw.setStyleSheet("#MainWindow{background-color: black}")

    mw.showNormal()

    # mw.show()
    sys.exit(app.exec_())

#
# clipboard.dataChanged.connect(change_deal)
# app.exec_()
