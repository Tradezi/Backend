import sys
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
from app.Utils import get_error_msg
from app import db, logger

def get_current_stock_price(stock_details):
    symbol = stock_details.symbol
    date_today = "{}-{}-{}".format(date.today().year, date.today().month, date.today().day)
    date_last_month = "{}-{}-{}".format(date.today().year, date.today().month-1, date.today().day)
    if(date.today().month==1):
        date_last_month = "{}-{}-{}".format(date.today().year-1, 12, date.today().day)
    stock = yf.download(symbol.upper(),date_last_month,date_today)
    if(stock.Close.values.shape[0]==0):
        # db.session.delete(stock_details)
        # db.session.commit()
        return -1
    return stock.Close.values[-1]

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
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
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
                "close": history.Close.values[i],
                "open": history.Open.values[i],
                "high": history.High.values[i],
                "low": history.Low.values[i]
            }
            data.append(stock_price)
        del history

        return Response(
            mimetype="application/json",        
            response=json.dumps(data),
            status=200
        )
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
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
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 

def nyse_stock_current_data(symbol):
    try:
        # date_today = "{}-{}-{}".format(date.today().year, date.today().month, date.today().day)
        # date_last_month = "{}-{}-{}".format(date.today().year, date.today().month-1, date.today().day)
        # if(date.today().month==1):
        #     date_last_month = "{}-{}-{}".format(date.today().year-1, 12, date.today().day)
        print("Collecting Current Stock Data","-"*80)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        stock = Stock.query.filter_by(symbol=symbol.upper()).first()
        # stock = yf.download(symbol.upper(),date_last_month,date_today)
        stock_price = get_current_stock_price(stock)
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("Current Stock Data Collected","-"*80)
        stock_price = {
            # "date": "{}-{}-{}".format(date.today().day, date.today().month, date.today().year),
            "price": stock_price,
            "company": stock.company_name,
            "symbol": symbol
        }
        return Response(
            mimetype="application/json",
            response=json.dumps(stock_price),
            status=200
        )
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 

def transaction(stock_symbol,stock_price,num_of_stocks,buy):
    user_id=1
    try:
        user = User.query.get(user_id)
        stock = Stock.stock_via_symbol(stock_symbol.upper())
        stock_id = stock.id
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
        return Response(
            mimetype="application/json",
            response=json.dumps({'success': "Transaction successfully"}),
            status=201
        )

    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 



def get_current_price_of_all_stocks(page):
    try:
        stocks = Stock.query.all()
        data = []
        i = page*20
        n=20
        while(n and i<len(stocks)):
            stock = stocks[i]
            symbol = stock.symbol
            price = get_current_stock_price(stock)
            if(price==-1):
                i+=1
                continue
            data.append(
                {
                    'symbol': symbol,
                    'company': stock.company_name,
                    'price': price
                }
            )
            i+=1
            n-=1
        return Response(
            mimetype="application/json",
            response=json.dumps(data),
            status=200
        )
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        )     
        