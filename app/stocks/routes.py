import json
from datetime import date
from nsepy import get_history
from flask_cors import cross_origin
from flask import Blueprint, request, Response, make_response, jsonify
# from app import firebase
from app.user.auth import Auth
from app.stocks.controller import nse_stock_history_data, nse_stock_current_data, nyse_stock_history_data, nyse_stock_current_data


stocks = Blueprint('stocks', __name__)

@stocks.route("/history", methods=["GET"])
@cross_origin(supports_credentials=True)
# @firebase.jwt_required
# @Auth.auth_required   /
def stock_history():
    try:
        print("=*"*80)
        print(f"Hello {request.jwt_payload['email']}!")
        symbol = request.args.get('symbol')
        years = int(request.args.get('years'))  
        return nyse_stock_history_data(symbol,years)
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        ) 


@stocks.route("/current", methods=["GET"])
@cross_origin(supports_credentials=True)
# @Auth.auth_required
def stock_current():
    try:
        symbol = request.args.get('symbol')
        return nyse_stock_current_data(symbol)
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
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
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )