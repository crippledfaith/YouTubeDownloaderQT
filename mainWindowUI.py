# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowUI.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
import os
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 200)
        MainWindow.setMinimumSize(QSize(500, 200))
        MainWindow.setMaximumSize(QSize(500, 200))
        MainWindow.setSizeIncrement(QSize(500, 200))

        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        elif __file__:
            application_path = os.path.dirname(__file__)
        iconFile = 'icon.ico'
        iconPath = os.path.join(application_path, iconFile)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)

        self.clipBoardTimer = QtCore. QTimer()

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 0, 481, 31))
        self.linkLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.linkLayout.setObjectName(u"linkLayout")
        self.linkLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.linkLayout.setContentsMargins(0, 0, 0, 0)
        self.linkLabel = QLabel(self.horizontalLayoutWidget)
        self.linkLabel.setObjectName(u"linkLabel")

        self.linkLayout.addWidget(self.linkLabel)

        self.linkTextBox = QLineEdit(self.horizontalLayoutWidget)
        self.linkTextBox.setObjectName(u"linkTextBox")

        self.linkLayout.addWidget(self.linkTextBox)

        self.linkAddButton = QPushButton(self.horizontalLayoutWidget)
        self.linkAddButton.setObjectName(u"linkAddButton")

        self.linkLayout.addWidget(self.linkAddButton)

        self.linkAutoStartCheckBox = QCheckBox(self.horizontalLayoutWidget)
        self.linkAutoStartCheckBox.setObjectName(u"linkAutoStartCheckBox")

        self.linkLayout.addWidget(self.linkAutoStartCheckBox)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 30, 481, 101))
        self.mediaInfoLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.mediaInfoLayout.setObjectName(u"mediaInfoLayout")
        self.mediaInfoLayout.setContentsMargins(0, 0, 0, 0)
        self.mediaInfoGraphicsView = QLabel(self.horizontalLayoutWidget_2)
        self.mediaInfoGraphicsView.setObjectName(u"mediaInfoGraphicsView")
        self.mediaInfoGraphicsView.setScaledContents(True)
        self.mediaInfoGraphicsView.setMaximumSize(QSize(99, 99))
        self.mediaInfoLayout.addWidget(self.mediaInfoGraphicsView)

        self.mediaInfoInnerLayout1 = QVBoxLayout()
        self.mediaInfoInnerLayout1.setObjectName(u"mediaInfoInnerLayout1")
        self.mediaInfoInnerLayout2 = QVBoxLayout()
        self.mediaInfoInnerLayout2.setObjectName(u"mediaInfoInnerLayout2")
        self.mediaInfoTitleLabel = QLabel(self.horizontalLayoutWidget_2)
        self.mediaInfoTitleLabel.setObjectName(u"mediaInfoTitleLabel")

        self.mediaInfoInnerLayout2.addWidget(self.mediaInfoTitleLabel)

        self.mediaInfoAuthorLabel = QLabel(self.horizontalLayoutWidget_2)
        self.mediaInfoAuthorLabel.setObjectName(u"mediaInfoAuthorLabel")

        self.mediaInfoInnerLayout2.addWidget(self.mediaInfoAuthorLabel)

        self.mediaInfoViewLabel = QLabel(self.horizontalLayoutWidget_2)
        self.mediaInfoViewLabel.setObjectName(u"mediaInfoViewLabel")

        self.mediaInfoInnerLayout2.addWidget(self.mediaInfoViewLabel)

        self.mediaInfoOtherLabel = QLabel(self.horizontalLayoutWidget_2)
        self.mediaInfoOtherLabel.setObjectName(u"mediaInfoOtherLabel")

        self.mediaInfoInnerLayout2.addWidget(self.mediaInfoOtherLabel)


        self.mediaInfoInnerLayout1.addLayout(self.mediaInfoInnerLayout2)


        self.mediaInfoLayout.addLayout(self.mediaInfoInnerLayout1)

        self.line1 = QFrame(self.centralwidget)
        self.line1.setObjectName(u"line1")
        self.line1.setGeometry(QRect(-10, 20, 511, 20))
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line2 = QFrame(self.centralwidget)
        self.line2.setObjectName(u"line2")
        self.line2.setGeometry(QRect(-30, 130, 541, 20))
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 140, 481, 31))
        
        self.downloadSettingsLayout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.downloadSettingsLayout.setObjectName(u"downloadSettingsLayout")
        self.downloadSettingsLayout.setContentsMargins(0, 0, 0, 0)

        self.downloadControlLayout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.downloadControlLayout.setObjectName(u"downloadControlLayout")
        self.downloadControlLayout.setContentsMargins(0, 0, 0, 0)

        self.downloadSettingsLayout.addLayout(self.downloadControlLayout)

        self.downloadButtonLayout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.downloadButtonLayout.setObjectName(u"downloadButtonLayout")
        self.downloadButtonLayout.setContentsMargins(0, 0, 0, 0)

        self.downloadSettingsLayout.addLayout(self.downloadButtonLayout)

        self.downloadSettingsVideoCheckBox = QCheckBox(self.horizontalLayoutWidget_3)
        self.downloadSettingsVideoCheckBox.setObjectName(u"downloadSettingsVideoCheckBox")
        self.downloadSettingsVideoCheckBox.setMaximumWidth(55)
        self.downloadSettingsVideoCheckBox.setChecked(True)
        self.downloadControlLayout.addWidget(self.downloadSettingsVideoCheckBox)

        self.downloadSettingsVideoComboBox = QComboBox(self.horizontalLayoutWidget_3)
        self.downloadSettingsVideoComboBox.setObjectName(u"downloadSettingsVideoComboBox")

        self.downloadControlLayout.addWidget(self.downloadSettingsVideoComboBox)

        self.downloadSettingsAudioCheckBox = QCheckBox(self.horizontalLayoutWidget_3)
        self.downloadSettingsAudioCheckBox.setObjectName(u"downloadSettingsAudioCheckBox")
        self.downloadSettingsAudioCheckBox.setMaximumWidth(55)
        self.downloadSettingsAudioCheckBox.setChecked(True)
        self.downloadControlLayout.addWidget(self.downloadSettingsAudioCheckBox)

        self.downloadSettingsAudioComboBox = QComboBox(self.horizontalLayoutWidget_3)
        self.downloadSettingsAudioComboBox.setObjectName(u"downloadSettingsAudioComboBox")

        self.downloadControlLayout.addWidget(self.downloadSettingsAudioComboBox)

        self.downloadSettingsDownloadButton = QPushButton(self.horizontalLayoutWidget_3)
        self.downloadSettingsDownloadButton.setObjectName(u"downloadSettingsDownloadButton")
        self.downloadSettingsDownloadButton.setMaximumWidth(70)
        self.downloadButtonLayout.addWidget(self.downloadSettingsDownloadButton)

        self.downloadSettingsCancelButton = QPushButton(self.horizontalLayoutWidget_3)
        self.downloadSettingsCancelButton.setObjectName(u"downloadSettingsCancelButton")
        self.downloadSettingsCancelButton.setMaximumWidth(50)
        self.downloadButtonLayout.addWidget(self.downloadSettingsCancelButton)

        self.downloadSettingsLayout.setStretch(0, 10)
        self.downloadSettingsLayout.setStretch(1, 100)
        self.downloadSettingsLayout.setStretch(2, 10)
        self.downloadSettingsLayout.setStretch(3, 100)
        self.downloadSettingsLayout.setStretch(4, 10)
        self.downloadSettingsLayout.setStretch(5, 10)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 170, 481, 23))
        self.progressBar.setValue(0)
        self.line3 = QFrame(self.centralwidget)
        self.line3.setObjectName(u"line3")
        self.line3.setGeometry(QRect(-10, 160, 521, 20))
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"YouTube Downloader QT", None))
        self.linkLabel.setText(QCoreApplication.translate("MainWindow", u"Link: ", None))
        self.linkAddButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.linkAutoStartCheckBox.setText(QCoreApplication.translate("MainWindow", u"Auto Start", None))
        self.mediaInfoTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Title: ", None))
        self.mediaInfoAuthorLabel.setText(QCoreApplication.translate("MainWindow", u"Author: ", None))
        self.mediaInfoViewLabel.setText(QCoreApplication.translate("MainWindow", u"Veiw: 0", None))
        self.mediaInfoOtherLabel.setText(QCoreApplication.translate("MainWindow", u"Lenght: 0s", None))
        self.downloadSettingsVideoCheckBox.setText(QCoreApplication.translate("MainWindow", u"Video:", None))
        self.downloadSettingsAudioCheckBox.setText(QCoreApplication.translate("MainWindow", u"Audio:", None))
        self.downloadSettingsDownloadButton.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.downloadSettingsCancelButton.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    # retranslateUi

