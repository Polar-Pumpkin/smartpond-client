# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'node.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Node(object):
    def setupUi(self, Node):
        if not Node.objectName():
            Node.setObjectName(u"Node")
        Node.resize(400, 62)
        self.context = QVBoxLayout(Node)
        self.context.setSpacing(10)
        self.context.setObjectName(u"context")
        self.context.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(Node)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(400, 20))
        self.title.setMaximumSize(QSize(400, 20))
        font = QFont()
        font.setBold(True)
        self.title.setFont(font)

        self.context.addWidget(self.title)

        self.description = QLabel(Node)
        self.description.setObjectName(u"description")

        self.context.addWidget(self.description)


        self.retranslateUi(Node)

        QMetaObject.connectSlotsByName(Node)
    # setupUi

    def retranslateUi(self, Node):
        Node.setWindowTitle(QCoreApplication.translate("Node", u"\u9009\u62e9\u8282\u70b9", None))
        self.title.setText(QCoreApplication.translate("Node", u"\u9009\u62e9\u8282\u70b9", None))
        self.description.setText(QCoreApplication.translate("Node", u"\u8282\u70b9\u662f\u6b63\u5728\u8fd0\u884c\u5f53\u524d\u7a0b\u5e8f\u7684\u8bbe\u5907\n"
"\u4e3a\u8be5\u8bbe\u5907\u547d\u540d\u4ee5\u4fbf\u4e8e\u540e\u7eed\u7ba1\u7406", None))
    # retranslateUi

