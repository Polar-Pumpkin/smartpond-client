# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sensor_field.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_SensorField(object):
    def setupUi(self, SensorField):
        if not SensorField.objectName():
            SensorField.setObjectName(u"SensorField")
        SensorField.resize(400, 200)
        self.horizontalLayout = QHBoxLayout(SensorField)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.view = QVBoxLayout()
        self.view.setSpacing(0)
        self.view.setObjectName(u"view")
        self.name = QLabel(SensorField)
        self.name.setObjectName(u"name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setPointSize(20)
        self.name.setFont(font)

        self.view.addWidget(self.name)

        self.value = QLabel(SensorField)
        self.value.setObjectName(u"value")
        self.value.setMinimumSize(QSize(100, 0))
        font1 = QFont()
        font1.setPointSize(32)
        font1.setBold(True)
        self.value.setFont(font1)
        self.value.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.view.addWidget(self.value)

        self.unit = QLabel(SensorField)
        self.unit.setObjectName(u"unit")
        sizePolicy.setHeightForWidth(self.unit.sizePolicy().hasHeightForWidth())
        self.unit.setSizePolicy(sizePolicy)
        self.unit.setMinimumSize(QSize(100, 0))

        self.view.addWidget(self.unit)


        self.horizontalLayout.addLayout(self.view)

        self.trend = QVBoxLayout()
        self.trend.setObjectName(u"trend")
        self.status = QLabel(SensorField)
        self.status.setObjectName(u"status")
        font2 = QFont()
        font2.setBold(True)
        self.status.setFont(font2)
        self.status.setAlignment(Qt.AlignCenter)

        self.trend.addWidget(self.status)


        self.horizontalLayout.addLayout(self.trend)


        self.retranslateUi(SensorField)

        QMetaObject.connectSlotsByName(SensorField)
    # setupUi

    def retranslateUi(self, SensorField):
        SensorField.setWindowTitle(QCoreApplication.translate("SensorField", u"\u4f20\u611f\u5668\u6307\u6807", None))
        self.name.setText(QCoreApplication.translate("SensorField", u"\u540d\u79f0", None))
        self.value.setText(QCoreApplication.translate("SensorField", u"0.00", None))
        self.unit.setText(QCoreApplication.translate("SensorField", u"\u5355\u4f4d", None))
        self.status.setText(QCoreApplication.translate("SensorField", u"\u72b6\u6001", None))
    # retranslateUi

