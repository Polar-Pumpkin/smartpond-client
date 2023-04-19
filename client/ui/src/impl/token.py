# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'token.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Token(object):
    def setupUi(self, Token):
        if not Token.objectName():
            Token.setObjectName(u"Token")
        Token.resize(680, 590)
        self.gridLayout = QGridLayout(Token)
        self.gridLayout.setObjectName(u"gridLayout")
        self.base_vert = QVBoxLayout()
        self.base_vert.setObjectName(u"base_vert")
        self.base_vert.setContentsMargins(10, 10, 10, 10)
        self.vert_space_up = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.base_vert.addItem(self.vert_space_up)

        self.base_hori = QHBoxLayout()
        self.base_hori.setObjectName(u"base_hori")
        self.base_hori.setContentsMargins(10, 10, 10, 10)
        self.hori_space_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.base_hori.addItem(self.hori_space_left)

        self.central = QVBoxLayout()
        self.central.setSpacing(10)
        self.central.setObjectName(u"central")
        self.central.setContentsMargins(10, 10, 10, 10)
        self.title = QLabel(Token)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(400, 20))
        self.title.setMaximumSize(QSize(400, 20))
        font = QFont()
        font.setBold(True)
        self.title.setFont(font)

        self.central.addWidget(self.title)

        self.description = QLabel(Token)
        self.description.setObjectName(u"description")

        self.central.addWidget(self.description)

        self.context = QVBoxLayout()
        self.context.setObjectName(u"context")

        self.central.addLayout(self.context)

        self.footer = QVBoxLayout()
        self.footer.setObjectName(u"footer")

        self.central.addLayout(self.footer)


        self.base_hori.addLayout(self.central)

        self.hori_space_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.base_hori.addItem(self.hori_space_right)


        self.base_vert.addLayout(self.base_hori)

        self.vert_space_down = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.base_vert.addItem(self.vert_space_down)


        self.gridLayout.addLayout(self.base_vert, 0, 0, 1, 1)


        self.retranslateUi(Token)

        QMetaObject.connectSlotsByName(Token)
    # setupUi

    def retranslateUi(self, Token):
        Token.setWindowTitle(QCoreApplication.translate("Token", u"\u9009\u62e9\u767b\u5f55\u51ed\u8bc1", None))
        self.title.setText(QCoreApplication.translate("Token", u"\u9009\u62e9\u767b\u5f55\u51ed\u8bc1", None))
        self.description.setText(QCoreApplication.translate("Token", u"\u767b\u5f55\u51ed\u8bc1\u662f\u8be5\u8282\u70b9\u4e0e\u670d\u52a1\u5668\u901a\u4fe1\u65f6\u7684\u8eab\u4efd\u8bc1\u660e\n"
"\u901a\u8fc7\u767b\u5f55\u51ed\u8bc1\u53ef\u8ffd\u6eaf\u901a\u4fe1\u6570\u636e\u7684\u6765\u6e90\n"
"\u5728\u767b\u5f55\u51ed\u8bc1\u6cc4\u9732\u88ab\u7528\u4e8e\u8fdb\u884c\u5f02\u5e38\u6d3b\u52a8\u65f6\n"
"\u53ef\u8ffd\u6eaf\u54ea\u4e9b\u8282\u70b9\u53ef\u80fd\u5b58\u5728\u5b89\u5168\u95ee\u9898", None))
    # retranslateUi

