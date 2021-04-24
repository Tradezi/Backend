import json
from flask import jsonify, Response, make_response, g

from app import db, ts, logger
from app.user.model import User
from app.user.auth import Auth
from app.stocks.model import Stock, Transaction
from app.stocks.controller import get_current_stock_price
from app.Utils import get_error_msg

def user_sign_up(data):
    try:        
        if User.username_exists(data["username"]):
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': "Username already exists"}),
                status=403
            )
        if User.email_exists(data["email"]):
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': "email already exists"}),
                status=403
            )
        password_hash = User.generate_hash_password(data["password"])
        new_user = User(
            username=data["username"],
            name=data["name"],
            email=data["email"],
            password=password_hash
        )
        new_user.save()
        
        # # Now we'll send the email confirmation link
        # subject = "Confirm your email"

        # token = ts.dumps(self.email, salt='email-confirm-key')

        # confirm_url = url_for(
        #     'confirm_email',
        #     token=token,
        #     _external=True)

        # html = render_template(
        #     'email/activate.html',
        #     confirm_url=confirm_url)

        # # We'll assume that send_email has been defined in myapp/util.py
        # send_email(user.email, subject, html)

        return Response(
            mimetype="application/json",
            response=json.dumps({'success': "User created successfully"}),
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

def user_sign_in(data):
    try:
        # print("1-"*80)
        user = User.query.filter_by(email=data["email"]).first()
        # print(user)
        # print("5-"*80)
        # print(user.id)
        if not user:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'User Does not exsists'}),
                status=403
            )
        password_verified = user.check_hash_password(data["password"])
        # print("2-"*80)
        
        if password_verified:
            data = {
                "sucess": "signed in successflly"
            }
            # user.increment_sign_in_count()
            res = make_response(json.dumps(data))
            token = Auth.generate_token(user.id)
            print(token)
            # res.set_cookie(key="session", value=token, domain=".webboard.in", max_age=None, samesite='Strict', secure=True)
            res.set_cookie(key="token", value=token, max_age=None)
            return  res, 200, {'Content-Type': 'application/json'}
            # return res
        else:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'There was an error with your e-mail/password combination'}),
                status=403
            ) 
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 

def user_email_verification(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_verified = True
            db.session.commit()
            return # ask arvind what all data does he require after verification
        else:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'User not found'}),
                status=404
            )
    except Exception as e:
        error_msg = get_error_msg(e)
        logger.error(error_msg)
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': error_msg}),
            status=400
        ) 

@Auth.auth_required
def get_user_details():
    user_id = g.user['id']
    try:
        user = User.query.get(user_id)
        data = {
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "funds": user.funds,
            "sign_in_count": user.sign_in_count,
            "created_on": user.get_created_on()
        }
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

@Auth.auth_required
def get_user_stock_detials():
    user_id = g.user['id']
    try:
        trans = Transaction.query.filter_by(user_id=user_id)
        stocks_purchased = {}
        for tran in trans:
            stock = stocks_purchased.get(tran.stock_id, {})
            stock['cost'] = stock.get('cost',0) + (tran.num_of_stocks*tran.stock_price)
            stock['num'] = stock.get('num',0) + tran.num_of_stocks
            stocks_purchased[tran.stock_id] = stock
        data = []
        for stock_id, val in stocks_purchased.items():
            stock = Stock.query.get(stock_id)
            price = get_current_stock_price(stock)
            profit = price*val['num'] - val['cost']
            data.append(
                {
                    'symbol': stock.symbol,
                    'company': stock.company_name,
                    'price': price,
                    'num_purchased': val['num'],
                    'profit': profit

                }
            )
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

def update_user_details(data):
    pass
