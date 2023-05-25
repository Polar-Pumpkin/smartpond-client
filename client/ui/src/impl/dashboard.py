# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
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
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        if not Dashboard.objectName():
            Dashboard.setObjectName(u"Dashboard")
        Dashboard.resize(640, 480)
        self.verticalLayout_2 = QVBoxLayout(Dashboard)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.header = QWidget(Dashboard)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 60))
        self.header.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.profile = QVBoxLayout()
        self.profile.setSpacing(0)
        self.profile.setObjectName(u"profile")
        self.profile.setContentsMargins(10, 10, 10, 10)
        self.node_name = QLabel(self.header)
        self.node_name.setObjectName(u"node_name")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.node_name.setFont(font)

        self.profile.addWidget(self.node_name)

        self.pond_name = QLabel(self.header)
        self.pond_name.setObjectName(u"pond_name")

        self.profile.addWidget(self.pond_name)


        self.horizontalLayout.addLayout(self.profile)

        self.header_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.header_spacer)

        self.user = QVBoxLayout()
        self.user.setSpacing(0)
        self.user.setObjectName(u"user")
        self.user.setContentsMargins(10, 10, 10, 10)
        self.logged = QLabel(self.header)
        self.logged.setObjectName(u"logged")
        self.logged.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.user.addWidget(self.logged)

        self.username = QLabel(self.header)
        self.username.setObjectName(u"username")
        self.username.setFont(font)
        self.username.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.user.addWidget(self.username)


        self.horizontalLayout.addLayout(self.user)


        self.verticalLayout_2.addWidget(self.header)

        self.context = QVBoxLayout()
        self.context.setSpacing(10)
        self.context.setObjectName(u"context")
        self.context.setContentsMargins(10, 10, 10, 10)
        self.new_senser_area = QWidget(Dashboard)
        self.new_senser_area.setObjectName(u"new_senser_area")
        self.new_senser_area.setMinimumSize(QSize(0, 40))
        self.new_senser_area.setMaximumSize(QSize(16777215, 40))
        self.add = QHBoxLayout(self.new_senser_area)
        self.add.setSpacing(10)
        self.add.setObjectName(u"add")
        self.ns_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.add.addItem(self.ns_left)

        self.new_senser = QPushButton(self.new_senser_area)
        self.new_senser.setObjectName(u"new_senser")
        font1 = QFont()
        font1.setBold(True)
        self.new_senser.setFont(font1)
        self.new_senser.setFlat(True)

        self.add.addWidget(self.new_senser)

        self.ns_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.add.addItem(self.ns_right)


        self.context.addWidget(self.new_senser_area)


        self.verticalLayout_2.addLayout(self.context)


        self.retranslateUi(Dashboard)

        QMetaObject.connectSlotsByName(Dashboard)
    # setupUi

    def retranslateUi(self, Dashboard):
        Dashboard.setWindowTitle(QCoreApplication.translate("Dashboard", u"\u4eea\u8868\u76d8", None))
        self.node_name.setText(QCoreApplication.translate("Dashboard", u"\u8282\u70b9\u540d\u79f0", None))
        self.pond_name.setText(QCoreApplication.translate("Dashboard", u"\u9c7c\u5858\u540d\u79f0", None))
        self.logged.setText(QCoreApplication.translate("Dashboard", u"\u5df2\u767b\u5f55\u4e3a", None))
        self.username.setText(QCoreApplication.translate("Dashboard", u"\u7528\u6237\u540d", None))
        self.new_senser.setText(QCoreApplication.translate("Dashboard", u"\u6dfb\u52a0\u65b0\u4f20\u611f\u5668", None))
    # retranslateUi

