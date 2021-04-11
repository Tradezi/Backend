from flask import Blueprint, jsonify, Response, request
from flask_cors import cross_origin
import json


from app import db
from app.user.auth import Auth
from app.user.controller import user_sign_up, user_sign_in, user_email_verification, update_user_details, \
    get_user_details

user = Blueprint('user', __name__)

@user.route('/sign_up', methods=["POST"])
@cross_origin(supports_credentials=True)
def sign_up():
    try:
        '''
        data = {
            "username": "abc",
            "name": "abc abc",
            "email": "abc@gmail.com",
            "password" : "abcabc"
        }
        '''
        data = request.json
        if data:
            return user_sign_up(data)
        else:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': "No Json object recieved"}),
                status=400
            ) 
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )

@user.route('/sign_in', methods=["POST"])
@cross_origin(supports_credentials=True)
def sign_in():
    try:
        '''
        data = {
            "email": "abc@gmail.com",
            "password": "abcabc"
        }
        '''
        data = request.json
        if data:
            print("0-"*80)
            print(data)
            return user_sign_in(data)
        else:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': "No Json object recieved"}),
                status=400
            )
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )


@user.route('/sign_out', methods=["POST"])
@cross_origin(supports_credentials=True)
def sign_out():
    pass

@user.route('/forgot_password', methods=["POST"])
def forgot_password():
    pass

@user.route('/deactivate_account')
def deavtivate():
    pass

@user.route('/reset_password', methods=["POST"])
def reset_password():
    pass

@user.route('/details', methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
@Auth.auth_required
def user_details():
    try:
        # print ("=-"*80)
        # print (request.cookies)
        # print("=-"*80)
        if(request.method == 'POST'):
            data = request.json
            if data:
                return update_user_details(data)
            else:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': "No Json object recieved"}),
                    status=400
                )
        return get_user_details()
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )
    

@user.route('/email_verification/<token>', methods=["GET"])
def email_verification(token):
    try:
        return user_email_verification(token)
    except Exception as e:
        return Response(
            mimetype="application/json",
            response=json.dumps({'error': str(e)}),
            status=400
        )




