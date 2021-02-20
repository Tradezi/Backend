import json
from datetime import date
from nsepy import get_history
from flask import Blueprint, request, Response, make_response, jsonify

from app.stocks.controller import stock_history_data, stock_current_data

stocks = Blueprint('stocks', __name__)

@stocks.route("/history", methods=["GET"])
def stock_history():
    try:
        symbol = request.args.get('symbol')
        return stock_history_data(symbol)
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        ) 


@stocks.route("/current", methods=["GET"])
def stock_current():
    try:
        symbol = request.args.get('symbol')
        return stock_current_data(symbol)
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )


