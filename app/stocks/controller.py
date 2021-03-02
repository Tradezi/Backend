import json
from nsetools import Nse
from datetime import date, datetime
from nsepy import get_history
from flask import request, Response, make_response, jsonify

from app.stocks.model import Stock

def stock_history_data(symbol,years):
    try:
        date_today = date(date.today().year, date.today().month, date.today().day)
        date_start = date(date.today().year-years, date.today().month, date.today().day)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("Collecting Stock Data","-"*80)
        print("date and time =", dt_string)
        history = get_history(symbol=symbol.upper(), start=date_start, end=date_today)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
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

def stock_current_data(symbol):
    try:
        nse = Nse()
        stock = nse.get_quote(symbol)
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