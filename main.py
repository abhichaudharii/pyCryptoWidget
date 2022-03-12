import os
from utils import *
from UI.interface import *
from API.Crypto_API import *
from UI.settingsUI import *
from datetime import datetime
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt, QSettings

ICON_COLOR = (255, 255, 255)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()

        self.currentCoinSymbol, self.coinPairs, self.currencySymbol, self.marketSymbol, self.coinSymbols = "", "", "", "", []
        self.appSettings = QSettings("cryptoApp", "Settings") #to save widget settings

        self.ui.setupUi(self)
        self.initSetup()
        self.show()

    def initSetup(self):

        if self.appSettings.value("windowPosition"):
            self.move(self.appSettings.value("windowPosition"))

        # this gets data from the server
        self.refreshCoinsData()

        def moveWindow(event):
            """IF LEFT USER CLICKED & MOVED THE WINDOW"""
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
                self.appSettings.setValue("windowPosition", self.pos())

        self.ui.topFrameContainer.mouseMoveEvent = moveWindow
        self.ui.bottomFrameContainer.mouseMoveEvent = moveWindow
        self.hideTitleBar()

    def mousePressEvent(self, event):
        """Detect mouse press on the topbar frame and allow to move the window"""

        self.dragPos = event.globalPos()

    def getSettings(self, key):
        """Reads the value from the apps settings file and return
        
        :type key: str
        :rtype : any
        """

        return self.appSettings.value(key)

    def writeSettings(self, key, value):
        """Writes the value to the apps settings file and return
        
        :type key: str
        :type value: any
        """

        self.appSettings.setValue(key, value)

    def saveSettings(self):
        """Saves the app settings and refresh the coin data"""

        coinPairs = str(self.dialog.ui.coinPairsValueLabel.text()).replace(" ", "")
        if not coinPairs:
            self.showMsg("Error", "Please enter a valid coin symbol like BTC, ETH, DOGE, SHIB", True)
            return
        else:
            self.writeSettings("coinSymbols", coinPairs)
       
        marketValue = self.dialog.ui.marketLineEdit.text()
        if not marketValue:
            self.showMsg("Error", "Please enter a valid market name like Coinbase", True)
            return
        else:
            self.writeSettings("marketSymbol", marketValue)
        
        currencyValue = self.dialog.ui.lineEdit.text()
        if not currencyValue:
            self.showMsg("Error", "Please enter a valid currency symbol like USD.", True)
            return
        else:
            self.writeSettings("currencySymbol", currencyValue)

        coinPairList = []
        self.currentCoinSymbol = coinPairs

        if "," in coinPairs:
            coinPairList = coinPairs.split(",")
            self.currentCoinSymbol = coinPairList[0]

        self.writeSettings("currentCoinSymbol", self.currentCoinSymbol)
        self.refreshCoinsData()
        self.dialog.reject()

    def refreshCoinsData(self):
        """This method gets called when Refresh action is called or when user makes changes in Widget Settings"""

        coinPairs = self.getSettings("coinSymbols")
        currencySymbol = self.getSettings("currencySymbol")
        marketSymbol = self.getSettings("marketSymbol")

        self.coinPairs =  coinPairs if coinPairs else "BTC,ETH,DOGE"
        self.marketSymbol = marketSymbol if marketSymbol else "Coinbase"
        self.currencySymbol = currencySymbol if currencySymbol else "USD"

        self.getLatestCoinsDataFromURL(self.coinPairs, self.currencySymbol, self.marketSymbol)

    def showSettingsDaloge(self):
        """Shows settings dialoge view for Widget Settings"""

        self.dialog = QtWidgets.QDialog() #to show widget settings dialog
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.saveButton.clicked.connect(self.saveSettings)

        self.marketSymbol = self.getSettings("marketSymbol")
        self.currencySymbol = self.getSettings("currencySymbol")
        self.coinSymbols = self.getSettings("coinSymbols")

        #get the saved values from settings file and show on dialog
        if self.getSettings("coinSymbols"):
            self.dialog.ui.coinPairsValueLabel.setText(str(self.coinSymbols))
        else:
            self.dialog.ui.coinPairsValueLabel.setText("BTC,ETH,DOGE")

        if self.getSettings("currencySymbol"):
            self.dialog.ui.lineEdit.setText(str(self.currencySymbol))
        else:
            self.dialog.ui.lineEdit.setText("USD")

        if self.getSettings("marketSymbol"):
            self.dialog.ui.marketLineEdit.setText(str(self.marketSymbol))
        else:
            self.dialog.ui.marketLineEdit.setText("Coinbase")
            
        self.dialog.exec_()

    def showMsg(self, title, text, error=False):
        """Shows Information/Error message pop
        
            :type title: str
            :type text: str
            :type error: bool
        """

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        if error:
            msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.setStyleSheet("QMessageBox { background-color:; } QMessageBox QLabel {color: #000;}")
        msg.exec_()

    def changeCoin(self, isNext):
        """Changes the current coin data with the next/previous coin
        
            :type isNext: bool
        """

        self.currentCoinSymbol = self.getSettings("currentCoinSymbol")
        self.coinSymbols = self.getSettings("coinSymbols")
        if "," in self.coinSymbols:
            self.coinSymbols = self.coinSymbols.split(",")
        else:
            print("There is not next/previous coin")
            return

        # getting next coin index using the self.currentCoinSymbol index + 1
        currentCoinIndex = self.coinSymbols.index(self.currentCoinSymbol)

        if isNext:
            nextCoinIndex = currentCoinIndex  + 1
            if nextCoinIndex <= len(self.coinSymbols) -1:
                nextCoinSymbol = self.coinSymbols[nextCoinIndex]
                self.currentCoinSymbol = nextCoinSymbol
            else:
                print("There is not next coin")
                return
        else:
            preCoinIndex = currentCoinIndex  - 1
            if preCoinIndex <= len(self.coinSymbols) and preCoinIndex >= 0:
                nextCoinSymbol = self.coinSymbols[preCoinIndex]
                self.currentCoinSymbol = nextCoinSymbol
            else:
                print("There is not previous coin")
                return

        self.writeSettings("currentCoinSymbol", self.currentCoinSymbol)
        self.setCoinData()

    def contextMenuEvent(self, event):
        """Creates a context menu to allow closing the widget, refreshing coin data, next coin, previous and setting the settings"""

        contextMenu = QMenu(self)
        refreshAct = contextMenu.addAction("Refresh")
        nextAct = contextMenu.addAction("Next")
        previousAct = contextMenu.addAction("Previous")
        settinsgAct = contextMenu.addAction("Settings")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        
        if action == quitAct:
            self.close()
        
        if action == refreshAct:
            self.refreshCoinsData()

        if action == settinsgAct:
            self.showSettingsDaloge()

        if action == nextAct:
            self.changeCoin(isNext=True)
        
        if action == previousAct:
            self.changeCoin(isNext=False)

    def hideTitleBar(self):
        """Removes default window title bar so we can add our own"""

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setCoinIcon(self, iconURL):
        """Receives the coin from local file also calls the getDominantColor method to get most used color in the icon to set widget BG
        
            :type iconURL: str
        """

        iconPath = os.getcwd() + "/icons/cryptoIcons/" + os.path.basename(iconURL) # ./icons/cryptoIcons/btc.png
        iconData = getIconData(iconPath)

        iconImg = QtGui.QImage()
        iconImg.loadFromData(iconData)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconImg), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.coinImage.setIcon(icon)

        #Lets call change theme color here as setCoinIcon gets called on app launch
        ICON_COLOR = getDominantColor(iconPath)
        self.changeThemeColor(ICON_COLOR)

    def changeThemeColor(self, color):
        """Changes the widget BG color using getDominantColor method which find most used color in the icon

            :type color: str
        """

        self.ui.topFrameContainer.setStyleSheet(f"background-color:{color};")

    def saveCoinsData(self, coinDataList):
        """This method goes through a list of coinData and store that data to the app's settings file
        
            :type coinDataList: list
        """

        for coinData in coinDataList:
            self.writeSettings(coinData["COIN_NAME"], coinData)

    def getLatestCoinsDataFromURL(self, coinSymbols, currencySymbol, marketSymbol):
        """Gets the latest coin data from the cryptocompare API
            This method also `saveCoinsData` to save the received coin(s) data to the widget settings, Then it call setCoinData to
            set the received coin data to the Widget

        Args:
            coinSymbols (list[str]): Coin symbol to receive coinData, BTC, ETH
            currencySymbol (str): Currency symbol in which user whats the coin price
            marketSymbol (str): coin symbol to receive coinData, BTC, ETH
        """

        COIN_DATA = get_crypto_details(coinSymbols, currencySymbol, marketSymbol)

        if "error_code" not in COIN_DATA:
            COIN_DATA = COIN_DATA
        else:
            error_msg = str(COIN_DATA['message'])
            self.showMsg("Error", error_msg[:61], True)
            return

        self.currentCoinSymbol = "BTC" if not self.getSettings("currentCoinSymbol") else self.getSettings("currentCoinSymbol")
        self.saveCoinsData(COIN_DATA)
        self.writeSettings("currentCoinSymbol", self.currentCoinSymbol)
        self.setCoinData()

    def getCoinsDataFromSettings(self, coinSymbols):
        """Retrives coinSymbols data from the saved settings
        
            :type coinSymbols: str
            :rtype : dict
        """

        COIN_DATA_DICT = self.getSettings(coinSymbols)
        return COIN_DATA_DICT

    def setCoinData(self):
        """Sets the coin data to the widget"""

        self.currentCoinSymbol = self.getSettings("currentCoinSymbol")
        COIN_DATA = self.getCoinsDataFromSettings(self.currentCoinSymbol)

        if isinstance(COIN_DATA, dict):
            COIN_DATA = COIN_DATA
        else:
            print(f"{self.currentCoinSymbol} Coin data could not be fetched. Please remove it from the settings.")
            return

        if(COIN_DATA["IMAGE_URL"]):
            self.setCoinIcon(COIN_DATA["IMAGE_URL"])
        else:
            print("No icon found from the server.")

        self.ui.coinNameLabel.setText(COIN_DATA["COIN_NAME"])
        self.ui.marketNameLabel.setText(COIN_DATA["MARKET"])
        self.ui.coinPrice.setText(COIN_DATA["PRICE"])
        self.ui.up24hValue.setText(COIN_DATA["HIGH24HOUR"])
        self.ui.down24hValue.setText(COIN_DATA["LOW24HOUR"])
        self.ui.timeLabel.setText(COIN_DATA["TIME"])
        self.ui.coinOtherPrice.setText("MCAP " + COIN_DATA["MKTCAP"])

        if float(COIN_DATA["CHANGE_PCT_24HOUR"]) < 0:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-sort-down-30.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.change24h.setIcon(icon1)

        self.ui.change24h.setText(COIN_DATA["CHANGE_PCT_24HOUR"] + "%")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())