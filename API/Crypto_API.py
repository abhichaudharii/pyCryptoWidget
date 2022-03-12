import os
import sys
import json
import requests
from utils import *
from datetime import datetime
from configparser import ConfigParser

CRYPTO_ICON_URL = "https://www.cryptocompare.com"
CRYPTO_CRNT_PRICE_API_URL = "https://min-api.cryptocompare.com/data/pricemultifull"
ICON_DATA = None

def build_crnt_price_query(fsyms, tsyms, exchange="Coinbase"):
    """Builds the URL for an API request to cryptocompare's coin's current price API.
    Args:
        fsym (str|list): The cryptocurrency symbol of interest [ Min length - 1] [ Max length - 30]
        tsyms (List[str]): Cryptocurrency symbols list to to get current price [ Min length - 1] [ Max length - 500] 
        exchange (str): The exchange to obtain data from [ Min length - 2] [ Max length - 30] [ Default - Coinbase]
    Returns:
        str: URL formatted for a call to cryptocompare's current coin price endpoint
    """

    api_key = _get_api_key()
    url = (
        f"{CRYPTO_CRNT_PRICE_API_URL}?fsyms={fsyms}&tsyms={tsyms}"
        f"&e={exchange}&api={api_key}"
    )

    return url    

def getIconDataFromUrl(icon_url):
    try:
        response = requests.get(icon_url, timeout=3)
        response.raise_for_status()
        ICON_DATA = response.content
        if not response.headers["content-type"] == "image/png":
            print("No icon found for the coin")
        return ICON_DATA
    except:
        print("Icon could not be fetched.")

def _get_api_key():
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:
        [cryptocompare]
        api_key=<YOUR-CRYPTOCOMPARE-API-KEY>
    """
    
    config = ConfigParser()
    config.read('secrets.ini')

    try:
        API_KEY = config["cryptocompare"]["api_key"]
    except KeyError as keyError:
        print("Please enter cryptocompare API key in secrets.ini.\n[cryptocompare]\napi_key=<YOUR-CRYPTOCOMPARE-API-KEY>")
        sys.exit(1)

    return API_KEY

def format_crypto_data(jsonData, currency):
    coinsDataList = []
    for coinName in jsonData:
        coinData = jsonData[coinName][currency]
        coinDataDict = { "FROM_SYMBOL": coinData["FROMSYMBOL"], "TO_SYMBOL" : coinData["TOSYMBOL"], "COIN_NAME" : coinName,
        "MARKET" : coinData["MARKET"], "PRICE" :coinData["PRICE"],  "CHANGE_PCT_24HOUR" : coinData["CHANGEPCT24HOUR"], 
        "TIME" : str(datetime.now().strftime('%H:%M:%S %d-%m-%Y')),"IMAGE_URL" : CRYPTO_ICON_URL+coinData["IMAGEURL"], 
        "MKTCAP" : coinData["MKTCAP"], "HIGH24HOUR" : coinData["LOW24HOUR"], "LOW24HOUR" : coinData["HIGH24HOUR"]}
        coinsDataList.append(coinDataDict)

    return coinsDataList

def saveIcon(coinData):
    """This function saves the new icon in icons folder, It receives icon URL and Icon data to write the icon to a file"""
    
    for coin in coinData:
        iconPath = os.path.join(os.getcwd(), "icons", "cryptoIcons", coin["COIN_NAME"]+".png")
        if isIconLocallyAvail(iconPath):
            return

        iconURL = coin["IMAGE_URL"]
        iconData = getIconDataFromUrl(iconURL)

        with open(iconPath, "wb") as iconFile:
            iconFile.write(iconData)

def get_crypto_details(coinSymbols, currencySymbol, marketSymbol):
    """Makes an API request to a URL and returns the data as a Python object.
    Args:
        coinSymbols (list[str]): A list of Symbols for the crypto like BTC, ETH, BNB, etc.
        currencySymbol (str): Returned crypto price in which exchange like USD, INR, etc.
        marketSymbol (str): The exchange to obtain data from.
    Returns:
        dict: Crypto info for specific crypto coin
    """

    api_url = build_crnt_price_query(coinSymbols, currencySymbol, marketSymbol)

    try:
        response = requests.get(api_url)
        data = response.text
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if requests.exceptions.HTTPErrore == 401:
            return {"error_code" : 401, "message" : "Access denied. Check your API key. Get a new API from www.cryptocompare.com"}
        if requests.exceptions.HTTPError == 404:
            return {"error_code" : 404, "message" : f"Could not find data for {coinSymbols}:{currencySymbol} pair on {marketSymbol}."}
        else:
            return {"error_code" : 0, "message" : f"An error ocured with the code:- {requests.exceptions.HTTPError}\n\nMake sure you are connected to the internet."}
    except Exception as e:
        return {"error_code" : 0, "message" : f"An error ocured with the code:- {requests.exceptions.HTTPError}\n\nMake sure you are connected to the internet."}
    
    try:
        data  = json.loads(data)["DISPLAY"]
    except:
        return {"error_code" : 0, "message" : json.loads(data)["Message"]}

    saveIcon(format_crypto_data(data, currencySymbol))
    return format_crypto_data(data, currencySymbol)