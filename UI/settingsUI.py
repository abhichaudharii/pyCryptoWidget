from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 280)
        Dialog.setMinimumSize(QtCore.QSize(240, 280))
        Dialog.setMaximumSize(QtCore.QSize(240, 280))
        Dialog.setStyleSheet("*{\n"
"    color:#000;\n"
"    background:none;\n"
"    background-color:;\n"
"    border:none;\n"
"    padding:0px;\n"
"    margin:0px;\n"
"}\n"
"\n"
"#marketSubLabel{\n"
"    color:gray;\n"
"}\n"
"\n"
"#coinsPairSubLabel{\n"
"    color:gray;\n"
"}\n"
"\n"
"#saveButton{\n"
"    background-color:#FFF;\n"
"    border-radius:5px;\n"
"    color:#000;\n"
"    padding:3px 10px 3px 10px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.settingsMainFrame = QtWidgets.QFrame(Dialog)
        self.settingsMainFrame.setStyleSheet("background-color:#dfe6e9;")
        self.settingsMainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settingsMainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settingsMainFrame.setObjectName("settingsMainFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.settingsMainFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.mainHeadingLabel = QtWidgets.QLabel(self.settingsMainFrame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mainHeadingLabel.setFont(font)
        self.mainHeadingLabel.setObjectName("mainHeadingLabel")
        self.verticalLayout_2.addWidget(self.mainHeadingLabel, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.settingsSubFrame = QtWidgets.QFrame(self.settingsMainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsSubFrame.sizePolicy().hasHeightForWidth())
        self.settingsSubFrame.setSizePolicy(sizePolicy)
        self.settingsSubFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settingsSubFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settingsSubFrame.setObjectName("settingsSubFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.settingsSubFrame)
        self.verticalLayout_3.setContentsMargins(-1, 5, -1, 15)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.coinPairsLabel = QtWidgets.QLabel(self.settingsSubFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.coinPairsLabel.setFont(font)
        self.coinPairsLabel.setObjectName("coinPairsLabel")
        self.verticalLayout_3.addWidget(self.coinPairsLabel, 0, QtCore.Qt.AlignTop)
        self.coinPairsValueLabel = QtWidgets.QLineEdit(self.settingsSubFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.coinPairsValueLabel.setFont(font)
        self.coinPairsValueLabel.setStyleSheet("background-color:#FFF;")
        self.coinPairsValueLabel.setObjectName("coinPairsValueLabel")
        self.verticalLayout_3.addWidget(self.coinPairsValueLabel, 0, QtCore.Qt.AlignTop)
        self.coinsPairSubLabel = QtWidgets.QLabel(self.settingsSubFrame)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.coinsPairSubLabel.setFont(font)
        self.coinsPairSubLabel.setToolTip("")
        self.coinsPairSubLabel.setWordWrap(True)
        self.coinsPairSubLabel.setObjectName("coinsPairSubLabel")
        self.verticalLayout_3.addWidget(self.coinsPairSubLabel)
        self.label = QtWidgets.QLabel(self.settingsSubFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.settingsSubFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setStyleSheet("background-color:#FFF;")
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.marketLabel = QtWidgets.QLabel(self.settingsSubFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.marketLabel.setFont(font)
        self.marketLabel.setObjectName("marketLabel")
        self.verticalLayout_3.addWidget(self.marketLabel)
        self.marketLineEdit = QtWidgets.QLineEdit(self.settingsSubFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.marketLineEdit.setFont(font)
        self.marketLineEdit.setStyleSheet("background-color:#FFF;")
        self.marketLineEdit.setObjectName("marketLineEdit")
        self.verticalLayout_3.addWidget(self.marketLineEdit)
        self.verticalLayout_2.addWidget(self.settingsSubFrame, 0, QtCore.Qt.AlignTop)
        self.saveButton = QtWidgets.QPushButton(self.settingsMainFrame)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout_2.addWidget(self.saveButton, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.settingsMainFrame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.mainHeadingLabel.setText(_translate("Dialog", "Crypto Widget Settings"))
        self.coinPairsLabel.setText(_translate("Dialog", "Enter Coin Pairs"))
        self.coinPairsValueLabel.setToolTip(_translate("Dialog", "Add multiple coin names using comma."))
        self.coinPairsValueLabel.setPlaceholderText(_translate("Dialog", "BTC, ETH, DOGE"))
        self.coinsPairSubLabel.setText(_translate("Dialog", "Add multiple coin names using comma."))
        self.label.setText(_translate("Dialog", "Enter Currency"))
        self.lineEdit.setToolTip(_translate("Dialog", "Enter currency in which you want the coin price."))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "USD"))
        self.marketLabel.setText(_translate("Dialog", "Enter Market"))
        self.marketLineEdit.setToolTip(_translate("Dialog", "Enter market from which you want get coin prices"))
        self.marketLineEdit.setPlaceholderText(_translate("Dialog", "Coinbase"))
        self.saveButton.setToolTip(_translate("Dialog", "Save widget settings"))
        self.saveButton.setText(_translate("Dialog", "Save"))