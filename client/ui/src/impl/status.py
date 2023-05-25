# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'status.ui'
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
from PyQt5.QtWidgets import (QApplication, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Status(object):
    def setupUi(self, Status):
        if not Status.objectName():
            Status.setObjectName(u"Status")
        Status.resize(400, 89)
        self.verticalLayout = QVBoxLayout(Status)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.bar = QProgressBar(Status)
        self.bar.setObjectName(u"bar")
        self.bar.setMinimumSize(QSize(0, 20))
        self.bar.setMaximumSize(QSize(16777215, 20))
        self.bar.setMaximum(0)
        self.bar.setValue(-1)

        self.verticalLayout.addWidget(self.bar)

        self.message = QLabel(Status)
        self.message.setObjectName(u"message")

        self.verticalLayout.addWidget(self.message)

        self.action = QPushButton(Status)
        self.action.setObjectName(u"action")
        self.action.setMinimumSize(QSize(0, 40))
        self.action.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.action)


        self.retranslateUi(Status)

        QMetaObject.connectSlotsByName(Status)
    # setupUi

    def retranslateUi(self, Status):
        Status.setWindowTitle(QCoreApplication.translate("Status", u"\u5904\u7406\u72b6\u6001", None))
        self.message.setText(QCoreApplication.translate("Status", u"\u9519\u8bef\u4fe1\u606f", None))
        self.action.setText(QCoreApplication.translate("Status", u"\u64cd\u4f5c", None))
    # retranslateUi

