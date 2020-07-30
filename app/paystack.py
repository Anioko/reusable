import string
import requests
import json
import random
from flask import abort, jsonify, redirect, render_template, request, url_for, flash, session, make_response
from common import app, db, security
from config import DefaultConfig
app.config.from_object(DefaultConfig)

def create_transaction_ref(transaction_type, stringlength):
    """ 
    Generate unique random transaction Id with length 'stringlength + 2'

    param transaction_type: string identifier per transaction
    param stringlength: length or ramdomly generated string. First two letters from 
    transaction_type are automatically prepended(as a prefix) to the generated Id
    return: string random Id

    """
    prefix          =     transaction_type[:2].upper()
    random_chars    =     "".join([random.choice(string.ascii_letters + string.digits) for n in range(stringlength)])
    trx_id          =     prefix + str(random_chars)
    return trx_id


class Paystack():
    """
        Provides methods for initiating and verifying payment collection 
        using the Paystack API
    """
    secret_key  = 'Bearer ' + str(app.config.get('PAYSTACK_SECRET_KEY')) # Given by paystack
   
    def ___init__(self):
       pass
    
    def initiate_transaction(self, reference, amount, email, callback_url):
        url      =   'https://api.paystack.co/transaction/initialize'
        headers  =   {'Authorization': self.secret_key, 'Content-Type': 'application/json'}
        data     =   {'reference': reference, 'amount': amount, 'email': email, 'callback_url':callback_url }
        j_data   =   json.dumps(data)
        response =   requests.post(url, data = j_data, headers = headers, verify = True)
        r_json   =   response.json()
        if  r_json['status']    ==    True:
            r_json_data         =     r_json['data']
            authorization_url   =     r_json_data['authorization_url']
            return {'status': "success", 'auth_url':authorization_url}
        else:
            return {'status':"failed",'error_response':r_json['message']}
           

    def verify_transaction(self, txn_ref):
        """
        Requeries Paystack to verify payment transaction, redirects to referrer page on success 
        param txn_ref: unique transaction reference number per transaction
        return: boolean
        """
        url = 'https://api.paystack.co/transaction/verify/%s' %txn_ref
        headers = {'Authorization': self.secret_key, 'Content-Type': 'application/json'}
        response = requests.get(url, headers = headers, verify = True)
        r_json = response.json()
        rjson_data = r_json['data']
        return rjson_data['status']








