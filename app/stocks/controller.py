import json
import pandas as pd
import yfinance as yf
from nsetools import Nse
from sqlalchemy import and_
from nsepy import get_history
from datetime import date, datetime
from flask import request, Response, make_response, jsonify

from app.stocks.model import Stock, Transaction
from app.user.model import User
from app import db

def get_current_stock_price(symbol):
    date_today = "{}-{}-{}".format(date.today().year, date.today().month, date.today().day)
    stock = yf.download(symbol.upper(),date_today,date_today)
    return stock.Close.values[:-1][0]

def nse_stock_history_data(symbol,years):
    try:
        date_today = date(date.today().year, date.today().month, date.today().day)
        date_start = date(date.today().year-years, date.today().month, date.today().day)

        print("Collecting Stock Data","-"*80)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        history = get_history(symbol=symbol.upper(), start=date_start, end=date_today)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("Stock Data Collected","-"*80)

        data = []
        for i in range(len(history.Close.values)):
            stock_price = {
                "date": history.Close.index.values[i].strftime("%m-%d-%Y"),
                "price": history.Close.values[i],
            }
            data.append(stock_price)
        del history

        return Response(
            mimetype="application/json",        
            response=json.dumps(data),
            status=200
        )
    except Exception as e:
        print("Error: {}".format(e))
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )


def nyse_stock_history_data(symbol,years):
    try:
        date_today = "{}-{}-{}".format(date.today().year, date.today().month, date.today().day)
        date_start = "{}-{}-{}".format(date.today().year-years, date.today().month, date.today().day)

        print("Collecting Stock Data","-"*80)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        history = yf.download(symbol.upper(),date_start,date_today)
        # data = yf.download(tickers='UBER', period='5d', interval='5m')
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("Stock Data Collected","-"*80)

        data = []
        for i in range(len(history.Close.values)):
            stock_price = {
                "date":  pd.to_datetime(str(history.Close.index.values[i])).strftime("%m-%d-%Y"),
                "price": history.Close.values[i],
            }
            data.append(stock_price)
        del history

        return Response(
            mimetype="application/json",        
            response=json.dumps(data),
            status=200
        )
    except Exception as e:
        print("Error: {}".format(e))
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )

def nse_stock_current_data(symbol):
    try:
        nse = Nse()

        print("Collecting Current Stock Data","-"*80)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        stock = nse.get_quote(symbol)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("Current Stock Data Collected","-"*80)

        stock_price = {
            "date": "{}-{}-{}".format(date.today().day, date.today().month, date.today().year),
            "price": stock['lastPrice'],
        }
        return Response(
            mimetype="application/json",
            response=json.dumps(stock_price),
            status=200
        )
    except Exception as e:
        print("Error: {}".format(e))
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )

def nyse_stock_current_data(symbol):
    try:
        date_today = "{}-{}-{}".format(date.today().year, date.today().month, date.today().day)
        print("Collecting Current Stock Data","-"*80)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        stock = yf.download(symbol.upper(),date_today,date_today)
        print(stock)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("Current Stock Data Collected","-"*80)
        print("{},   {}".format(stock.Close.values[-1],stock.Close.values))
        stock_price = {
            "date": "{}-{}-{}".format(date.today().day, date.today().month, date.today().year),
            "price": stock.Close.values[-1]
        }
        return Response(
            mimetype="application/json",
            response=json.dumps(stock_price),
            status=200
        )
    except Exception as e:
        print("Error: {}".format(e))
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )

def transaction(stock_id,stock_price,num_of_stocks,buy):
    user_id=1
    try:
        user = User.query.get(user_id)
        if(buy):
            if((num_of_stocks*stock_price)>user.funds):
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': "Not enough funds to buy stocks"}),
                    status=403
                )           
            funds = user.funds - (num_of_stocks*stock_price)
            user.funds = funds
            user.commit()
            new_transaction = Transaction(
                user_id=user_id,
                stock_id=stock_id,
                stock_price=stock_price,
                num_of_stocks=num_of_stocks
            )
            new_transaction.save()
        else:
            trans = Transaction.get_user_stock_trans(user_id,stock_id)
            num_stocks_holded = 0
            for tran in trans:
                # print(tran)
                num_stocks_holded += tran.num_of_stocks
            if(num_of_stocks>num_stocks_holded):
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': "Not enough stocks to sell"}),
                    status=403
                )
            funds = user.funds + (num_of_stocks*stock_price)
            user.funds = funds
            user.commit()
            # print("%"*80)
            # print(num_of_stocks)
            for tran in trans:
                # print("%"*80)
                # print(tran.id)
                if(tran.num_of_stocks <= num_of_stocks):
                    num_of_stocks -= tran.num_of_stocks
                    db.session.delete(tran)
                    db.session.commit()
                else:
                    num = tran.num_of_stocks - num_of_stocks
                    # print("^^"*80)
                    # print(tran.num_of_stocks)
                    # print(num_of_stocks)
                    # print(num)
                    tran.num_of_stocks = num
                    tran.commit()

    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )