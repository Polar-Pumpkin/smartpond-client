# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(414, 266)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Login)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(Login)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout.addWidget(self.title)

        self.area_register = QHBoxLayout()
        self.area_register.setSpacing(0)
        self.area_register.setObjectName(u"area_register")
        self.title_register = QLabel(Login)
        self.title_register.setObjectName(u"title_register")

        self.area_register.addWidget(self.title_register)

        self.reg = QPushButton(Login)
        self.reg.setObjectName(u"reg")
        font1 = QFont()
        font1.setUnderline(True)
        self.reg.setFont(font1)
        self.reg.setStyleSheet(u"margin: 0;")
        self.reg.setFlat(True)

        self.area_register.addWidget(self.reg)

        self.space_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.area_register.addItem(self.space_right)


        self.verticalLayout.addLayout(self.area_register)

        self.area_login = QVBoxLayout()
        self.area_login.setSpacing(10)
        self.area_login.setObjectName(u"area_login")
        self.username = QLineEdit(Login)
        self.username.setObjectName(u"username")
        self.username.setMinimumSize(QSize(400, 40))
        self.username.setMaximumSize(QSize(400, 40))
        self.username.setClearButtonEnabled(True)

        self.area_login.addWidget(self.username)

        self.password = QLineEdit(Login)
        self.password.setObjectName(u"password")
        self.password.setMinimumSize(QSize(400, 40))
        self.password.setMaximumSize(QSize(400, 40))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setClearButtonEnabled(True)

        self.area_login.addWidget(self.password)


        self.verticalLayout.addLayout(self.area_login)

        self.login = QPushButton(Login)
        self.login.setObjectName(u"login")
        self.login.setMinimumSize(QSize(400, 40))
        self.login.setMaximumSize(QSize(400, 40))

        self.verticalLayout.addWidget(self.login)


        self.retranslateUi(Login)

        self.login.setDefault(True)


        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"\u767b\u5f55\u5230\u667a\u6167\u9c7c\u5858", None))
        self.title.setText(QCoreApplication.translate("Login", u"\u767b\u5f55\u5230\n"
"\u667a\u6167\u9c7c\u5858", None))
        self.title_register.setText(QCoreApplication.translate("Login", u"\u6ca1\u6709\u8d26\u53f7\u5417\uff1f", None))
        self.reg.setText(QCoreApplication.translate("Login", u"\u6ce8\u518c\u65b0\u8d26\u53f7", None))
        self.username.setPlaceholderText(QCoreApplication.translate("Login", u"\u7528\u6237\u540d", None))
        self.password.setPlaceholderText(QCoreApplication.translate("Login", u"\u5bc6\u7801", None))
        self.login.setText(QCoreApplication.translate("Login", u"\u767b\u5f55", None))
#if QT_CONFIG(shortcut)
        self.login.setShortcut(QCoreApplication.translate("Login", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

