import sys,os
import json
from datetime import date
from nsepy import get_history
from flask_cors import cross_origin
from flask import Blueprint, request, Response, make_response, jsonify
# from app import firebase

from app import logger
from app.Utils import get_error_msg
from app.user.auth import Auth
from app.stocks.controller import nse_stock_history_data, nse_stock_current_data, nyse_stock_history_data, nyse_stock_current_data, transaction, \
    get_current_price_of_all_stocks


stocks = Blueprint('stocks', __name__)

@stocks.route("/history", methods=["GET"])
@cross_origin(supports_credentials=True)
# @firebase.jwt_required
# @Auth.auth_required   /
def stock_history():
    try:
        symbol = request.args.get('symbol')
        years = int(request.args.get('years'))
        logger.info("/api/stocks/history => stock history of symbol: {}, years: {}".format(symbol,years))  
        return nyse_stock_history_data(symbol,years)
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 


@stocks.route("/current", methods=["GET"])
@cross_origin(supports_credentials=True)
# @Auth.auth_required
def stock_current():
    try:
        symbol = request.args.get('symbol')
        logger.info("/api/stocks/current => current stock price of symbol: {}".format(symbol)) 
        return nyse_stock_current_data(symbol)
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 
 

@stocks.route("/transaction", methods=["POST"])
@cross_origin(supports_credentials=True)
def stock_transaction():
    try:
        data = request.json
        stock_id = data['stockId']
        stock_price = data['stockPrice']
        num_of_stocks = data['numOfStocks']
        buy = data['buy']
        logger.info("/api/stocks/transaction => stock transaction stock_id: {}, stock_price: {}, num: {}, buy: {}".format(
            stock_id, stock_price, num_of_stocks, buy
        )) 
        return transaction(stock_id,stock_price,num_of_stocks,buy)
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 

@stocks.route("/all", methods=["GET"])
@cross_origin(supports_credentials=True)
def all_stock_current_prices():
    try:
        logger.info("/api/stocks/all => all stock data")
        page = int(request.args.get('page')) 
        return get_current_price_of_all_stocks(page)
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        )  