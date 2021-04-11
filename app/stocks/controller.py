import json
import pandas as pd
from sqlalchemy import and_
from nsetools import Nse
from datetime import date, datetime
from nsepy import get_history
import yfinance as yf
from flask import request, Response, make_response, jsonify

from app.stocks.model import Stock, Transaction

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
        print("date and time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("Current Stock Data Collected","-"*80)

        stock_price = {
            "date": "{}-{}-{}".format(date.today().day, date.today().month, date.today().year),
            "price": stock.Close.values[:-1][0]
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
        trans = Transaction.query.filter(and_(Transaction.user_id==user_id, Transaction.stock_id==stock_id)).first()
        price = stock_price*num_of_stocks
        if(buy):
            if not trans:
                new_trans = Transaction(
                    user_id=user_id,
                    stock_id=stock_id,
                    stock_price=price,
                    num_of_stocks=num_of_stocks
                )
                new_trans.save()
            else:
                price += trans.stock_price
                num_of_stocks += trans.num_of_stocks
                trans.num_of_stocks = num_of_stocks
                trans.stock_price = price
                trans.commit()

                # ADD: Subract user funds
        else:
            if(num_of_stocks == trans.num_of_stocks):
                # ADD: add user funds
                db.session.delete(trans)
                db.session.commit()
            elif(num_of_stocks < trans.num_of_stocks):
                price = trans.stock_price - price
                num_of_stocks = trans.num_of_stocks - num_of_stocks
                trans.num_of_stocks = num_of_stocks
                trans.stock_price = price
                trans.commit()


        return Response(
            mimetype="application/json",
            response=json.dumps({'success': "Transaction successful"}),
            status=201
        )
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )