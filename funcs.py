import datetime
import json

def changePerc(open, close):
    open = float(open)
    close = float(close)
    change = close - open
    changePercent = (change/open)*100
    return changePercent

def getBalance():
    with open('balance.json', 'r') as log:
        f = json.load(log)
    for i in f['balance']:
        return i['bal']


def buy(balance, buyPrice):
    balance = float(balance)
    buyPrice = float(buyPrice)
    amount = balance
    balance -= amount
    buyTime = datetime.datetime.now()
    coins = amount/buyPrice
    recordTransaction(buyTime, buyPrice, coins, balance)
    args = {"stopLoss": [{
        "price": "0"
        }
    ]}
    with open('stopLoss.json', 'w') as sl:
        json.dump(args, sl)
    print(buyTime.strftime("%X")+': Bought ENJ! info:', '\nBuy Price:', buyPrice)
pass

def isBalanceEnough():
    return float(getBalance()) >= 100



def findColor(open, close):
    open = float(open)
    close = float(close)
    return float(close) > float(open)

def recordTransaction(buyTime, buyPrice, coins, balance):
    args = {"trade": [{
        "buyTime": buyTime.strftime("%X"),
        "buyPrice": str(buyPrice),
        "amount": str(coins)
        }
    ]}
    with open('log.json', 'w') as log:
        json.dump(args, log, indent=2)
    args = {"balance": [{
        "bal": str(balance)
        }
    ]}
    with open('balance.json', 'w+') as bal:
        json.dump(args, bal, indent=2)
pass

def isLogEmpty():
    with open('log.json', 'r') as log:
        data = json.load(log)
    for i in data['trade']:
        ans = i['buyPrice']
    return ans == ""

def fetchLogInfo():
    with open('log.json', 'r') as log:
        data = json.load(log)
    for i in data['trade']:
        ans = [i['buyTime'], i['buyPrice'], i['amount']]
    if not ans[0]:
        return False
    else:
        return ans

def profitMet(info, priceNow):
    buy = float(info)
    priceNow = float(priceNow)
    return changePerc(buy, priceNow) >= 1

def sell(buyP, coinsB, sellP):
    coins = float(coinsB)
    buyPrice = float(buyP)
    timeVar = datetime.datetime.now()
    sellP = float(sellP)
    balance = coins * sellP
    args = {
        "trade": [
            {
            "buyTime": "",
            "buyPrice": "",
            "amount": ""
        }
        ]
    }
    with open('log.json', 'w+') as log:
        json.dump(args, log, indent=2)
    args = {"balance": [{
        "bal": str(balance)
        }
    ]}
    with open('balance.json', 'w+') as bal:
        json.dump(args, bal, indent=2)
    print(timeVar.strftime("%X") + ': Sold ENJEUR that was bought at price', buyPrice, 'at price', sellP)
pass

def stopLossEmpty():
    with open('stopLoss.json', 'r') as sl:
        data = json.load(sl)
    for i in data['stopLoss']:
        ans = i['price']
    return not ans
pass

def getStopLoss():
    with open('stopLoss.json', 'r') as sl:
        data = json.load(sl)
    for i in data['stopLoss']:
        ans = float(i['price'])
    return ans

def updateStopLoss(candle):
    args = {"stopLoss": [{
        "price": str(candle),
        }
    ]}
    with open('stopLoss.json', 'w') as sl:
        json.dump(args, sl, indent=2)
pass

def clearStopLoss():
    args = {"stopLoss": [{
        "price": "0"
        }
    ]}
    with open('stopLoss.json', 'w') as sl:
        json.dump(args, sl, indent=2)
pass

def calcStopLoss(candle, info):
    buyPrice = float(info[1])
    if stopLossEmpty() and isLogEmpty():
        return False
    elif not isLogEmpty():
        if changePerc(buyPrice, candle[-1][4]) <= -1.5:
            updateStopLoss(candle[-1][4])
            return 'sell'
    elif not stopLossEmpty() and not isLogEmpty():
        sl = getStopLoss()
        if float(candle[-1][4]) >= sl:
            clearStopLoss()
            return 'buy'
    return False


def check_5m(candleList):
    if isLogEmpty():
        return findColor(candleList[-1][1], candleList[-1][4]) and float(candleList[-6][1]) > float(candleList[-1][4]) and findColor(candleList[-6][1], candleList[-6][4])
    return False

def checkSell_5m(candleList):
    return not findColor(candleList[-1][1], candleList[-1][4])

def initFiles():
    args = {
        "trade": [
            {
                "buyTime": "",
                "buyPrice": "",
                "amount": ""
            }
        ]
    }
    with open('log.json', 'w') as log:
        json.dump(args, log, indent=2)
    args = {
        "stopLoss": [
            {
                "price": "0"
            }
        ]
    }
    with open('stopLoss.json', 'w') as sl:
        json.dump(args, sl, indent=2)
    args = {
        "balance": [
            {
                "bal": "100"
            }
        ]
    }
    with open('balance.json', 'w') as bal:
        json.dump(args, bal, indent=2)
pass