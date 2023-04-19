from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    context = Signal(QWidget)

    def __init__(self):
        super(MainWindow, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('智慧鱼塘')

        # self.stacks = QStackedWidget(self)
        # self.stacks.addWidget(LoginWidget())
        self.context.connect(self.setCentralWidget)

        from client.ui.widget.login import LoginWidget
        self.setCentralWidget(LoginWidget(self))
