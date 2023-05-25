# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'centralize.ui'
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
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Centralize(object):
    def setupUi(self, Centralize):
        if not Centralize.objectName():
            Centralize.setObjectName(u"Centralize")
        Centralize.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Centralize)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.vert_space_up = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.vert_space_up)

        self.row = QHBoxLayout()
        self.row.setObjectName(u"row")
        self.row.setContentsMargins(10, 10, 10, 10)
        self.hori_space_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.row.addItem(self.hori_space_left)

        self.context = QVBoxLayout()
        self.context.setSpacing(10)
        self.context.setObjectName(u"context")
        self.context.setContentsMargins(10, 10, 10, 10)

        self.row.addLayout(self.context)

        self.hori_space_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.row.addItem(self.hori_space_right)


        self.verticalLayout.addLayout(self.row)

        self.vert_space_down = QSpacerItem(20, 105, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.vert_space_down)


        self.retranslateUi(Centralize)

        QMetaObject.connectSlotsByName(Centralize)
    # setupUi

    def retranslateUi(self, Centralize):
        Centralize.setWindowTitle(QCoreApplication.translate("Centralize", u"\u5c45\u4e2d\u663e\u793a", None))
    # retranslateUi

