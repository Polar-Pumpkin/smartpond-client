# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'namespace_create.ui'
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
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_NamespaceCreate(object):
    def setupUi(self, NamespaceCreate):
        if not NamespaceCreate.objectName():
            NamespaceCreate.setObjectName(u"NamespaceCreate")
        NamespaceCreate.resize(400, 136)
        self.verticalLayout = QVBoxLayout(NamespaceCreate)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(NamespaceCreate)
        self.title.setObjectName(u"title")

        self.verticalLayout.addWidget(self.title)

        self.name = QLineEdit(NamespaceCreate)
        self.name.setObjectName(u"name")
        self.name.setMinimumSize(QSize(0, 40))
        self.name.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.name)

        self.footer = QHBoxLayout()
        self.footer.setSpacing(10)
        self.footer.setObjectName(u"footer")
        self.footer.setContentsMargins(10, 10, 10, 10)
        self.confirm = QPushButton(NamespaceCreate)
        self.confirm.setObjectName(u"confirm")
        self.confirm.setMinimumSize(QSize(0, 40))
        self.confirm.setMaximumSize(QSize(16777215, 40))

        self.footer.addWidget(self.confirm)

        self.hori_space = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footer.addItem(self.hori_space)

        self.secondary = QPushButton(NamespaceCreate)
        self.secondary.setObjectName(u"secondary")
        self.secondary.setMinimumSize(QSize(0, 40))
        self.secondary.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setUnderline(True)
        self.secondary.setFont(font)
        self.secondary.setFlat(True)

        self.footer.addWidget(self.secondary)


        self.verticalLayout.addLayout(self.footer)


        self.retranslateUi(NamespaceCreate)

        self.confirm.setDefault(True)


        QMetaObject.connectSlotsByName(NamespaceCreate)
    # setupUi

    def retranslateUi(self, NamespaceCreate):
        NamespaceCreate.setWindowTitle(QCoreApplication.translate("NamespaceCreate", u"\u521b\u5efa\u547d\u540d\u7a7a\u95f4", None))
        self.title.setText(QCoreApplication.translate("NamespaceCreate", u"\u6807\u9898", None))
        self.name.setPlaceholderText(QCoreApplication.translate("NamespaceCreate", u"\u547d\u540d\u7a7a\u95f4\u540d\u79f0", None))
        self.confirm.setText(QCoreApplication.translate("NamespaceCreate", u"\u786e\u8ba4\u64cd\u4f5c", None))
        self.secondary.setText(QCoreApplication.translate("NamespaceCreate", u"\u5907\u9009\u64cd\u4f5c", None))
    # retranslateUi

