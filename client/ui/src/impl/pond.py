# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pond.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Pond(object):
    def setupUi(self, Pond):
        if not Pond.objectName():
            Pond.setObjectName(u"Pond")
        Pond.resize(400, 62)
        self.context = QVBoxLayout(Pond)
        self.context.setSpacing(10)
        self.context.setObjectName(u"context")
        self.context.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(Pond)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(400, 20))
        self.title.setMaximumSize(QSize(400, 20))
        font = QFont()
        font.setBold(True)
        self.title.setFont(font)

        self.context.addWidget(self.title)

        self.description = QLabel(Pond)
        self.description.setObjectName(u"description")

        self.context.addWidget(self.description)


        self.retranslateUi(Pond)

        QMetaObject.connectSlotsByName(Pond)
    # setupUi

    def retranslateUi(self, Pond):
        Pond.setWindowTitle(QCoreApplication.translate("Pond", u"\u9009\u62e9\u9c7c\u5858", None))
        self.title.setText(QCoreApplication.translate("Pond", u"\u9009\u62e9\u9c7c\u5858", None))
        self.description.setText(QCoreApplication.translate("Pond", u"\u9c7c\u5858\u662f\u4e00\u4e2a\u865a\u6784\u7684\u8282\u70b9\u96c6\u5408\n"
"\u60a8\u53ef\u4ee5\u5c06\u76f8\u8fd1\u7684\u8282\u70b9\u5f52\u4e8e\u540c\u4e00\u4e2a\u9c7c\u5858\u5185\u4fbf\u4e8e\u7ba1\u7406", None))
    # retranslateUi

