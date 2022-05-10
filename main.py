from binance import Client
import datetime, time
import requests
import math

# CHECKPOINT FOR SELL POSITION

def buy(amount, price):
    order = client.order_limit_buy(
        symbol='ADABUSD',
        quantity=math.floor(amount),
        price=str(price))

def sell(amount, price):
    order = client.order_limit_sell(
        symbol='ADABUSD',
        quantity=math.floor(amount),
        price=str(price))


api_key = '<YOUR API KEY>'
api_secret = 'YOUR SECRET API KEY'

client = Client(api_key, api_secret)

price = 0
got_position = False
n = 0
k = False
l = True

if __name__ == '__main__':
    while True:
        rand_bool = True
        while rand_bool:
            try:
                prices = client.get_all_tickers()
                rand_bool = False
            except requests.exceptions.RequestException:
                if l:
                    timeVar = datetime.datetime.now()
                    print(timeVar.strftime("%X") + ':\tRestoring internet connection...')
                    l = False
                k = True
                time.sleep(10)
                rand_bool = True
            if k:
                timeVar = datetime.datetime.now()
                print(timeVar.strftime("%X") + ':\tConnection restored!')
                k = False
                l = True
        for i in prices:
            if i['symbol'] == 'ADABUSD':
                price = i.get('price')
        rand_bool = True
        while rand_bool:
            try:
                if got_position:
                    balance_dict = client.get_asset_balance(asset='ADA')
                else:
                    balance_dict = client.get_asset_balance(asset='BUSD')
                rand_bool = False
            except requests.exceptions.RequestException:
                if l:
                    timeVar = datetime.datetime.now()
                    print(timeVar.strftime("%X") + ':\tRestoring internet connection...')
                    l = False
                k = True
                time.sleep(10)
                rand_bool = True
            if k:
                timeVar = datetime.datetime.now()
                print(timeVar.strftime("%X") + ':\tConnection restored!')
                k = False
                l = True
        balance = balance_dict['free']
        if n == 0:
            timeVar = datetime.datetime.now()
            print(timeVar.strftime("%X") + ':\tBalance:', balance, '\n\t\t\tPrice:', price)
            n += 1
        if got_position:
            if float(price) <= 2.695:
                sell(float(balance), price)
                got_position = False
                timeVar = datetime.datetime.now()
                print(timeVar.strftime("%X") + ': Sold ADA at price', price)
                n = 0
                time.sleep(120)
        else:
            if float(price) >= 2.705:
                qty = math.floor(float(balance)/float(price))
                buy(qty, price)
                got_position = True
                timeVar = datetime.datetime.now()
                print(timeVar.strftime("%X") + ':\tBought', qty, 'ADA at price', price)
                n = 0
                time.sleep(120)

        if not got_position and float(balance) < 1.0 and float(price) >= 2.655:
            qty = math.floor(float(balance) / float(price))
            buy(qty, price)
            timeVar = datetime.datetime.now()
            print(timeVar.strftime("%X") + ':\tSome shit happened but got restored at price', price)
            n = 0
            time.sleep(120)
        time.sleep(10)