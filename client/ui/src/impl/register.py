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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Register(object):
    def setupUi(self, Register):
        if not Register.objectName():
            Register.setObjectName(u"Register")
        Register.resize(414, 270)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Register.sizePolicy().hasHeightForWidth())
        Register.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Register)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(Register)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout.addWidget(self.title)

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


        self.verticalLayout.addLayout(self.area_login)

        self.area_register = QVBoxLayout()
        self.area_register.setSpacing(10)
        self.area_register.setObjectName(u"area_register")
        self.username = QLineEdit(Register)
        self.username.setObjectName(u"username")
        self.username.setMinimumSize(QSize(0, 40))
        self.username.setMaximumSize(QSize(16777215, 40))
        self.username.setClearButtonEnabled(True)

        self.area_register.addWidget(self.username)

        self.password = QLineEdit(Register)
        self.password.setObjectName(u"password")
        self.password.setMinimumSize(QSize(0, 40))
        self.password.setMaximumSize(QSize(16777215, 40))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setClearButtonEnabled(True)

        self.area_register.addWidget(self.password)


        self.verticalLayout.addLayout(self.area_register)

        self.reg = QPushButton(Register)
        self.reg.setObjectName(u"reg")
        self.reg.setMinimumSize(QSize(0, 40))
        self.reg.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.reg)


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

