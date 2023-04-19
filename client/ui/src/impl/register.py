# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Register(object):
    def setupUi(self, Register):
        if not Register.objectName():
            Register.setObjectName(u"Register")
        Register.resize(723, 508)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Register.sizePolicy().hasHeightForWidth())
        Register.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Register)
        self.gridLayout.setObjectName(u"gridLayout")
        self.vert_base = QVBoxLayout()
        self.vert_base.setObjectName(u"vert_base")
        self.vert_base.setContentsMargins(10, 10, 10, 10)
        self.vert_space_up = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vert_base.addItem(self.vert_space_up)

        self.hori_base = QHBoxLayout()
        self.hori_base.setObjectName(u"hori_base")
        self.hori_base.setContentsMargins(10, 10, 10, 10)
        self.hori_space_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hori_base.addItem(self.hori_space_left)

        self.central = QVBoxLayout()
        self.central.setObjectName(u"central")
        self.central.setContentsMargins(10, 10, 10, 10)
        self.title = QLabel(Register)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.title.setFont(font)

        self.central.addWidget(self.title)

        self.area_login = QHBoxLayout()
        self.area_login.setSpacing(0)
        self.area_login.setObjectName(u"area_login")
        self.title_register = QLabel(Register)
        self.title_register.setObjectName(u"title_register")

        self.area_login.addWidget(self.title_register)

        self.login = QPushButton(Register)
        self.login.setObjectName(u"login")
        font1 = QFont()
        font1.setUnderline(True)
        self.login.setFont(font1)
        self.login.setStyleSheet(u"margin: 0;")
        self.login.setFlat(True)

        self.area_login.addWidget(self.login)

        self.space_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.area_login.addItem(self.space_right)


        self.central.addLayout(self.area_login)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.central.addItem(self.verticalSpacer_2)

        self.area_register = QVBoxLayout()
        self.area_register.setSpacing(10)
        self.area_register.setObjectName(u"area_register")
        self.username = QLineEdit(Register)
        self.username.setObjectName(u"username")
        self.username.setMinimumSize(QSize(400, 40))
        self.username.setMaximumSize(QSize(400, 40))
        self.username.setClearButtonEnabled(True)

        self.area_register.addWidget(self.username)

        self.password = QLineEdit(Register)
        self.password.setObjectName(u"password")
        self.password.setMinimumSize(QSize(400, 40))
        self.password.setMaximumSize(QSize(400, 40))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setClearButtonEnabled(True)

        self.area_register.addWidget(self.password)


        self.central.addLayout(self.area_register)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.central.addItem(self.verticalSpacer)

        self.reg = QPushButton(Register)
        self.reg.setObjectName(u"reg")
        self.reg.setMinimumSize(QSize(400, 40))
        self.reg.setMaximumSize(QSize(400, 40))

        self.central.addWidget(self.reg)


        self.hori_base.addLayout(self.central)

        self.hori_space_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hori_base.addItem(self.hori_space_right)


        self.vert_base.addLayout(self.hori_base)

        self.vert_space_down = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vert_base.addItem(self.vert_space_down)


        self.gridLayout.addLayout(self.vert_base, 0, 0, 1, 1)


        self.retranslateUi(Register)

        self.reg.setDefault(True)


        QMetaObject.connectSlotsByName(Register)
    # setupUi

    def retranslateUi(self, Register):
        Register.setWindowTitle(QCoreApplication.translate("Register", u"\u6b22\u8fce\u6765\u5230\u667a\u6167\u9c7c\u5858", None))
        self.title.setText(QCoreApplication.translate("Register", u"\u6b22\u8fce\u6765\u5230\n"
"\u667a\u6167\u9c7c\u5858", None))
        self.title_register.setText(QCoreApplication.translate("Register", u"\u5df2\u6709\u8d26\u53f7\uff1f", None))
        self.login.setText(QCoreApplication.translate("Register", u"\u767b\u5f55", None))
        self.username.setPlaceholderText(QCoreApplication.translate("Register", u"\u7528\u6237\u540d", None))
        self.password.setPlaceholderText(QCoreApplication.translate("Register", u"\u5bc6\u7801", None))
        self.reg.setText(QCoreApplication.translate("Register", u"\u6ce8\u518c", None))
#if QT_CONFIG(shortcut)
        self.reg.setShortcut(QCoreApplication.translate("Register", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

