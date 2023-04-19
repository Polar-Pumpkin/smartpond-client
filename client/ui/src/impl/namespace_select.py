# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'namespace_select.ui'
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
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_NamespaceSelect(object):
    def setupUi(self, NamespaceSelect):
        if not NamespaceSelect.objectName():
            NamespaceSelect.setObjectName(u"NamespaceSelect")
        NamespaceSelect.resize(400, 276)
        self.gridLayout = QGridLayout(NamespaceSelect)
        self.gridLayout.setObjectName(u"gridLayout")
        self.central = QVBoxLayout()
        self.central.setSpacing(10)
        self.central.setObjectName(u"central")
        self.header = QHBoxLayout()
        self.header.setSpacing(10)
        self.header.setObjectName(u"header")
        self.header.setContentsMargins(10, 10, 10, 10)
        self.header_preferred = QPushButton(NamespaceSelect)
        self.header_preferred.setObjectName(u"header_preferred")
        self.header_preferred.setMinimumSize(QSize(0, 40))
        self.header_preferred.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setUnderline(True)
        self.header_preferred.setFont(font)
        self.header_preferred.setFlat(True)

        self.header.addWidget(self.header_preferred)

        self.header_space = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.header.addItem(self.header_space)

        self.header_secondary = QPushButton(NamespaceSelect)
        self.header_secondary.setObjectName(u"header_secondary")
        self.header_secondary.setMinimumSize(QSize(0, 40))
        self.header_secondary.setMaximumSize(QSize(16777215, 40))
        self.header_secondary.setFont(font)
        self.header_secondary.setFlat(True)

        self.header.addWidget(self.header_secondary)


        self.central.addLayout(self.header)

        self.namespaces = QListWidget(NamespaceSelect)
        self.namespaces.setObjectName(u"namespaces")

        self.central.addWidget(self.namespaces)

        self.footer = QHBoxLayout()
        self.footer.setSpacing(10)
        self.footer.setObjectName(u"footer")
        self.footer.setContentsMargins(10, 10, 10, 10)
        self.confirm = QPushButton(NamespaceSelect)
        self.confirm.setObjectName(u"confirm")
        self.confirm.setMinimumSize(QSize(0, 40))
        self.confirm.setMaximumSize(QSize(16777215, 40))

        self.footer.addWidget(self.confirm)

        self.selected = QLabel(NamespaceSelect)
        self.selected.setObjectName(u"selected")

        self.footer.addWidget(self.selected)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footer.addItem(self.horizontalSpacer)


        self.central.addLayout(self.footer)


        self.gridLayout.addLayout(self.central, 0, 0, 1, 1)


        self.retranslateUi(NamespaceSelect)

        self.confirm.setDefault(True)


        QMetaObject.connectSlotsByName(NamespaceSelect)
    # setupUi

    def retranslateUi(self, NamespaceSelect):
        NamespaceSelect.setWindowTitle(QCoreApplication.translate("NamespaceSelect", u"\u9009\u62e9\u547d\u540d\u7a7a\u95f4", None))
        self.header_preferred.setText(QCoreApplication.translate("NamespaceSelect", u"\u9996\u9009\u64cd\u4f5c", None))
        self.header_secondary.setText(QCoreApplication.translate("NamespaceSelect", u"\u5907\u9009\u64cd\u4f5c", None))
        self.confirm.setText(QCoreApplication.translate("NamespaceSelect", u"\u786e\u8ba4\u64cd\u4f5c", None))
        self.selected.setText(QCoreApplication.translate("NamespaceSelect", u"\u5df2\u9009\u62e9\n"
"\u547d\u540d\u7a7a\u95f4", None))
    # retranslateUi

