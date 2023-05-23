# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sensor_create.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SensorCreate(object):
    def setupUi(self, SensorCreate):
        if not SensorCreate.objectName():
            SensorCreate.setObjectName(u"SensorCreate")
        SensorCreate.resize(543, 207)
        self.context = QVBoxLayout(SensorCreate)
        self.context.setSpacing(10)
        self.context.setObjectName(u"context")
        self.context.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(SensorCreate)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(400, 20))
        self.title.setMaximumSize(QSize(400, 20))
        font = QFont()
        font.setBold(True)
        self.title.setFont(font)

        self.context.addWidget(self.title)

        self.form = QWidget(SensorCreate)
        self.form.setObjectName(u"form")
        self.gridLayout = QGridLayout(self.form)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.name = QLineEdit(self.form)
        self.name.setObjectName(u"name")

        self.gridLayout.addWidget(self.name, 1, 0, 1, 2)

        self.title_port = QLabel(self.form)
        self.title_port.setObjectName(u"title_port")

        self.gridLayout.addWidget(self.title_port, 2, 1, 1, 1)

        self.model = QComboBox(self.form)
        self.model.setObjectName(u"model")

        self.gridLayout.addWidget(self.model, 3, 0, 1, 1)

        self.title_name = QLabel(self.form)
        self.title_name.setObjectName(u"title_name")

        self.gridLayout.addWidget(self.title_name, 0, 0, 1, 1)

        self.title_model = QLabel(self.form)
        self.title_model.setObjectName(u"title_model")

        self.gridLayout.addWidget(self.title_model, 2, 0, 1, 1)

        self.port = QComboBox(self.form)
        self.port.setObjectName(u"port")

        self.gridLayout.addWidget(self.port, 3, 1, 1, 1)

        self.confirm = QPushButton(self.form)
        self.confirm.setObjectName(u"confirm")

        self.gridLayout.addWidget(self.confirm, 4, 0, 1, 1)

        self.cancel = QPushButton(self.form)
        self.cancel.setObjectName(u"cancel")
        self.cancel.setFlat(True)

        self.gridLayout.addWidget(self.cancel, 4, 1, 1, 1)


        self.context.addWidget(self.form)


        self.retranslateUi(SensorCreate)

        QMetaObject.connectSlotsByName(SensorCreate)
    # setupUi

    def retranslateUi(self, SensorCreate):
        SensorCreate.setWindowTitle(QCoreApplication.translate("SensorCreate", u"\u6dfb\u52a0\u4f20\u611f\u5668", None))
        self.title.setText(QCoreApplication.translate("SensorCreate", u"\u6dfb\u52a0\u4f20\u611f\u5668", None))
        self.title_port.setText(QCoreApplication.translate("SensorCreate", u"\u7aef\u53e3", None))
        self.title_name.setText(QCoreApplication.translate("SensorCreate", u"\u540d\u79f0", None))
        self.title_model.setText(QCoreApplication.translate("SensorCreate", u"\u578b\u53f7", None))
        self.confirm.setText(QCoreApplication.translate("SensorCreate", u"\u786e\u5b9a", None))
        self.cancel.setText(QCoreApplication.translate("SensorCreate", u"\u53d6\u6d88", None))
    # retranslateUi

