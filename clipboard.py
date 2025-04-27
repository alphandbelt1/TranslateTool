import sys
import os 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# pyqt5
#

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, QFrame, QRadioButton, QVBoxLayout, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer

from Baidu_Text_transAPI import trans
import os
import datetime

app = QApplication([])


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainWindow")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.initUI()
        self.word_box_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        self.word_box_file = open(os.path.join(self.word_box_path, "word_box.txt"), 'a+')
        self.words = []

        # 添加阴影
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QtGui.QColor(0, 0, 0, 180))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        # 居中显示
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle("翻译小工具 by @陶欤冰")
        self.resize(360, 220)

        # 主部件和布局
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # 顶部时间和单选
        top_layout = QHBoxLayout()
        self.is_word_box = QRadioButton('记录到单词本')
        self.is_word_box.setStyleSheet("color: #00BFFF; font-weight: bold;")
        self.label_time = QLabel(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.label_time.setStyleSheet("color: #aaa; font-size: 12px;")
        top_layout.addWidget(self.is_word_box)
        top_layout.addStretch()
        top_layout.addWidget(self.label_time)
        layout.addLayout(top_layout)

        # 翻译显示区域
        self.label = QLabel("请复制文本以翻译", self)
        self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        font = QtGui.QFont('微软雅黑', 16, QtGui.QFont.Bold)
        self.label.setFont(font)
        self.label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #232526, stop:1 #414345);
            color: #fff;
            border-radius: 12px;
            padding: 18px;
            border: 2px solid #00BFFF;
        """)
        layout.addWidget(self.label)

        # 状态栏美化
        self.statusBar().setStyleSheet("color: #00BFFF; background: #232526; border-top: 1px solid #444;")

        # 自定义按钮（可选）
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        copy_btn = QPushButton("复制翻译结果")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BFFF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E90FF;
            }
        """)
        copy_btn.clicked.connect(self.copy_result)
        btn_layout.addWidget(copy_btn)
        layout.addLayout(btn_layout)

        # 定时器
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start(1000)

    def showtime(self):
        text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_time.setText(text)

    def copy_result(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.label.text())
        self.statusBar().showMessage("翻译结果已复制", 2000)

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
