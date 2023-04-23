from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from datetime import datetime
import math
import sys
import traceback
from web3 import Web3

# TODO: make sure you implement connect_to_algo, send_tokens_algo, and send_tokens_eth
from send_tokens import connect_to_algo, connect_to_eth, send_tokens_algo, send_tokens_eth

from gen_keys import get_algo_keys, get_eth_keys

from models import Base, Order, TX, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

""" Pre-defined methods (do not need to change) """

@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()

def connect_to_blockchains():
    try:
        # If g.acl has not been defined yet, then trying to query it fails
        acl_flag = False
        g.acl
    except AttributeError as ae:
        acl_flag = True
    
    try:
        if acl_flag or not g.acl.status():
            # Define Algorand client for the application
            g.acl = connect_to_algo()
    except Exception as e:
        print("Trying to connect to algorand client again")
        print(traceback.format_exc())
        g.acl = connect_to_algo()
    
    try:
        icl_flag = False
        g.icl
    except AttributeError as ae:
        icl_flag = True
    
    try:
        if icl_flag or not g.icl.health():
            # Define the index client
            g.icl = connect_to_algo(connection_type='indexer')
    except Exception as e:
        print("Trying to connect to algorand indexer client again")
        print(traceback.format_exc())
        g.icl = connect_to_algo(connection_type='indexer')

        
    try:
        w3_flag = False
        g.w3
    except AttributeError as ae:
        w3_flag = True
    
    try:
        if w3_flag or not g.w3.isConnected():
            g.w3 = connect_to_eth()
    except Exception as e:
        print("Trying to connect to web3 again")
        print(traceback.format_exc())
        g.w3 = connect_to_eth()
        
""" End of pre-defined methods """
        
""" Helper Methods (skeleton code for you to implement) """

def insert_TX(tx_id):
    this_order = g.session.query(Order).filter(Order.id == tx_id[0]).first()
    platform = this_order.buy_currency
    receiver_pk = this_order.receiver_pk
    order_id = tx_id[0]
    TX_obj = TX(platform = platform, receiver_pk = receiver_pk, order_id = order_id, tx_id = tx_id[1])
    g.session.add(TX_obj)
    g.session.commit()

    pass 

def check_sig(payload,sig):
    result = False
    message = payload
    pk = payload['sender_pk']

    if (payload['platform'] == 'Ethereum'):
        if (eth_account.Account.recover_message(eth_account.messages.encode_defunct(text=json.dumps(message)), signature=sig)) == pk:
            result = True
        else:
            result = False
    elif (payload['platform'] == 'Algorand'):
        if algosdk.util.verify_bytes(json.dumps(message).encode('utf-8'),sig,pk): 
            result = True
        else:
            result = False
    return result


def log_message(message_dict):

    # TODO: Add message to the Log table
    g.session.add(Log(message = json.dumps(message_dict)))
    g.session.commit()
    return

def insert_child_order(thisID,sender_pk, receiver_pk, buy_currency, sell_currency, buy_amount, sell_amount,signature):
    
    order_obj = Order( sender_pk=sender_pk,receiver_pk=receiver_pk, buy_currency=buy_currency, 
                      sell_currency=sell_currency, buy_amount=buy_amount, sell_amount=sell_amount,  
                      creator_id = thisID, signature = signature)
    g.session.add(order_obj)
    g.session.commit()

    myOrder = g.session.query(Order).order_by(Order.id.desc()).first()
    id = myOrder.id
    return 

def insert_order(order):

    order_obj = Order( sender_pk=order['payload']['sender_pk'],receiver_pk=order['payload']['receiver_pk'], buy_currency=order['payload']['buy_currency'], 
                      sell_currency=order['payload']['sell_currency'], buy_amount=order['payload']['buy_amount'], 
                      sell_amount=order['payload']['sell_amount'],signature = order['sig'])
    
    g.session.add(order_obj)
    g.session.commit()
    myOrder = g.session.query(Order).order_by(Order.id.desc()).first()
    id = myOrder.id
    return id

def insert_child_order(thisID,sender_pk, receiver_pk, buy_currency, sell_currency, buy_amount, sell_amount,signature):
    
    order_obj = Order( sender_pk=sender_pk,receiver_pk=receiver_pk, buy_currency=buy_currency, 
                      sell_currency=sell_currency, buy_amount=buy_amount, sell_amount=sell_amount,  
                      creator_id = thisID, signature = signature)
    g.session.add(order_obj)
    g.session.commit()

    myOrder = g.session.query(Order).order_by(Order.id.desc()).first()
    id = myOrder.id
    return

def findMatch(orderID, txes_list):
    
    newOrder = g.session.query(Order).filter(Order.id == orderID).first()
    newOrderSellCurrency = newOrder.sell_currency
    newOrderSellAmount = newOrder.sell_amount
    if newOrderSellAmount == 0:
        return txes_list
    
    newOrderBuyCurrency = newOrder.buy_currency
    newOrderBuyAmount = newOrder.buy_amount
    newOrderExchangeRate = newOrderBuyAmount/newOrderSellAmount
    # this means no match at all
    if (g.session.query(Order).filter(Order.filled.is_(None), Order.buy_currency == newOrderSellCurrency, Order.sell_currency == newOrderBuyCurrency, 
                                                  ((Order.sell_amount * newOrderSellAmount) >= (Order.buy_amount * newOrderBuyAmount)),
                                                  ((Order.sell_amount/Order.buy_amount) >= newOrderExchangeRate),).count()) == 0:
      return txes_list
    
    else:
        g.session.commit()
        existingOrder = g.session.query(Order).filter(Order.filled.is_(None), Order.buy_currency == newOrderSellCurrency, Order.sell_currency == newOrderBuyCurrency, 
                                                  ((Order.sell_amount * newOrderSellAmount) >= (Order.buy_amount * newOrderBuyAmount)),
                                                  ((Order.sell_amount/Order.buy_amount) >= newOrderExchangeRate),).first()
        # this means new order is fulfilled
        if (newOrderBuyAmount <= 0):
            return txes_list
        
        if (existingOrder.sell_amount == newOrderBuyAmount) or (existingOrder.buy_amount == newOrderSellAmount):
            mytimestamp = datetime.now()
            newOrder.filled = mytimestamp
            newOrder.counterparty_id = existingOrder.id
            existingOrder.filled = mytimestamp
            existingOrder.counterparty_id = newOrder.id
            newOrderBuyAmount = 0

            temp_dict = {}
            temp_dict['order_id'] = existingOrder.id
            temp_dict['platform'] = existingOrder.buy_currency
            temp_dict['receiver_pk'] = existingOrder.receiver_pk
            temp_dict['amount'] = min(existingOrder.buy_amount, newOrder.sell_amount)
            txes_list.append(temp_dict)

            temp_dict = {}
            temp_dict['order_id'] = newOrder.id
            temp_dict['platform'] = newOrder.buy_currency
            temp_dict['receiver_pk'] = newOrder.receiver_pk
            temp_dict['amount'] = min(existingOrder.sell_amount, newOrder.buy_amount)
            txes_list.append(temp_dict)

            g.session.commit()
            return txes_list
        
        else:
            if (existingOrder.buy_amount <= newOrderSellAmount and newOrderBuyAmount >= existingOrder.sell_amount):
                remain_buy = newOrderBuyAmount - existingOrder.sell_amount
                new_sell_amount = remain_buy/newOrderExchangeRate
                child_id = insert_child_order(newOrder.id, newOrder.sender_pk,newOrder.receiver_pk, newOrder.buy_currency, 
                                            newOrder.sell_currency,remain_buy, new_sell_amount,newOrder.signature)
                mytimestamp = datetime.now()
                newOrder.filled = mytimestamp
                newOrder.counterparty_id = existingOrder.id
                existingOrder.filled = mytimestamp
                existingOrder.counterparty_id = newOrder.id

                temp_dict = {}
                temp_dict['order_id'] = existingOrder.id
                temp_dict['platform'] = existingOrder.buy_currency
                temp_dict['receiver_pk'] = existingOrder.receiver_pk
                temp_dict['amount'] = min(existingOrder.buy_amount, newOrder.sell_amount)
                txes_list.append(temp_dict)

                temp_dict = {}
                temp_dict['order_id'] = newOrder.id
                temp_dict['platform'] = newOrder.buy_currency
                temp_dict['receiver_pk'] = newOrder.receiver_pk
                temp_dict['amount'] = min(existingOrder.sell_amount, newOrder.buy_amount)
                txes_list.append(temp_dict)

                g.session.commit()
                #counter, txes_list = findMatch(child_id, counter, txes_list)
                #g.session.commit()
                return txes_list
            
            elif (existingOrder.buy_amount >= newOrderSellAmount and newOrderBuyAmount <= existingOrder.sell_amount):
                exist_ex_rate = existingOrder.sell_amount/existingOrder.buy_amount
                remain_buy = existingOrder.buy_amount - newOrderSellAmount
                exist_new_sell_amount = remain_buy * exist_ex_rate
                child_id = insert_child_order(existingOrder.id, existingOrder.sender_pk,existingOrder.receiver_pk, existingOrder.buy_currency, 
                                            existingOrder.sell_currency,remain_buy, exist_new_sell_amount, existingOrder.signature)
                mytimestamp = datetime.now()
                newOrder.filled = mytimestamp
                newOrder.counterparty_id = existingOrder.id
                existingOrder.filled = mytimestamp
                existingOrder.counterparty_id = newOrder.id

                temp_dict = {}
                temp_dict['order_id'] = existingOrder.id
                temp_dict['platform'] = existingOrder.buy_currency
                temp_dict['receiver_pk'] = existingOrder.receiver_pk
                temp_dict['amount'] = min(existingOrder.buy_amount, newOrder.sell_amount)
                txes_list.append(temp_dict)

                temp_dict = {}
                temp_dict['order_id'] = newOrder.id
                temp_dict['platform'] = newOrder.buy_currency
                temp_dict['receiver_pk'] = newOrder.receiver_pk
                temp_dict['amount'] = min(existingOrder.sell_amount, newOrder.buy_amount)
                txes_list.append(temp_dict)

                g.session.commit()
                #counter, txes_list = findMatch(child_id, counter, txes_list)
                #g.session.commit()
                return txes_list
                  
    return txes_list

def fill_order(order, txes=[]):# add order_id into payload for txes
    # TODO: 
    # Match orders (same as Exchange Server II)
    # Validate the order has a payment to back it (make sure the counterparty also made a payment)
    # Make sure that you end up executing all resulting transactions!
    orderID = insert_order(order)
    txes_list = findMatch(orderID, txes)
    return txes_list
  
def execute_txes(txes):
    if txes is None:
        return True
    if len(txes) == 0:
        return True
    print( f"Trying to execute {len(txes)} transactions" )
    print( f"IDs = {[tx['order_id'] for tx in txes]}" )
    eth_sk, eth_pk = get_eth_keys()
    algo_sk, algo_pk = get_algo_keys()
    
    if not all( tx['platform'] in ["Algorand","Ethereum"] for tx in txes ):
        print( "Error: execute_txes got an invalid platform!" )
        print( tx['platform'] for tx in txes )

    algo_txes = [tx for tx in txes if tx['platform'] == "Algorand" ]
    eth_txes = [tx for tx in txes if tx['platform'] == "Ethereum" ]

    # TODO: 
    #       1. Send tokens on the Algorand and eth testnets, appropriately
    #          We've provided the send_tokens_algo and send_tokens_eth skeleton methods in send_tokens.py
    #       2. Add all transactions to the TX table
    if len(algo_txes) > 0:
        tx_id_algo_list = send_tokens_algo(g.acl, algo_sk, txes)
        # adding transaction to TX table
        for i in tx_id_algo_list:
            insert_TX(i)

    if len(eth_txes) > 0:
        tx_id_eth_list = send_tokens_eth(g.w3,eth_sk,txes)
        for i in tx_id_eth_list:
            insert_TX(i)

    return True

def check_amount(content):
    sell_amount = content['payload']['sell_amount']
    the_tx_id = content['payload']['tx_id']
    if (content['payload']['sell_currency'] == 'Algorand'):
        try:
            result = g.acl.transactions.get(the_tx_id)
            if (result['amount'] >= sell_amount):
                return True
            else:
                return False
        except Exception as e:
            return False
    elif (content['payload']['sell_currency'] == 'Ethereum'):
        try:
            result = g.w3.get_transaction(the_tx_id)
            if (result['value'] >= sell_amount):
                return True
            else:
                return False
        except Exception as e:
            try:
                result = g.w3.get_raw_transaction(the_tx_id)
                if (result['value'] >= sell_amount):
                    return True
            except Exception as e:
                return False
    else:
        return False

""" End of Helper methods"""
  
@app.route('/address', methods=['POST'])
def address():
    eth_sk, eth_pk = get_eth_keys()
    algo_sk, algo_pk = get_algo_keys()
    if request.method == "POST":
        content = request.get_json(silent=True)
        if 'platform' not in content.keys():
            print( f"Error: no platform provided" )
            return jsonify( "Error: no platform provided" )
        if not content['platform'] in ["Ethereum", "Algorand"]:
            print( f"Error: {content['platform']} is an invalid platform" )
            return jsonify( f"Error: invalid platform provided: {content['platform']}"  )
        
        if content['platform'] == "Ethereum":
            #Your code here
            return jsonify( eth_pk ) #my public key
        if content['platform'] == "Algorand":
            #Your code here
            return jsonify( algo_pk )

@app.route('/trade', methods=['POST'])
def trade():
    print( "In trade", file=sys.stderr )
    connect_to_blockchains()
    #get_keys()
    eth_sk, eth_pk = get_eth_keys()
    algo_sk, algo_pk = get_algo_keys()
    if request.method == "POST":
        content = request.get_json(silent=True)
        columns = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform", "tx_id", "receiver_pk"]
        fields = [ "sig", "payload" ]
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            return jsonify( False )
        
        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            return jsonify( False )
        
        # Your code here
        
        # 1. Check the signature
        verify_bool = False
        verify_bool = check_sig(content['payload'],content['sig'])

        # 2. Add the order to the table
        if verify_bool == False:
            #send the message to the Log table
            log_message(content)
            return jsonify(False)
        else:
            
            
        # 3a. Check if the order is backed by a transaction equal to the sell_amount (this is new)
            if(check_amount(content)):

        # 3b. Fill the order (as in Exchange Server II) if the order is valid
                txes_list = fill_order(content)
                if execute_txes(txes_list) == False:
                    return jsonify(False)

        # 4. Execute the transactions
            else:
                 return jsonify(False)
        # If all goes well, return jsonify(True). else return jsonify(False)
        return jsonify(True)

@app.route('/order_book')
def order_book():
    fields = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "signature", "tx_id", "receiver_pk", "sender_pk" ,"order_id"]
    
    All_existingOrder = g.session.query(Order).all()
    instance_list = []
    for i in All_existingOrder:
        temp_dict = {}
        temp_dict['sender_pk'] = i.sender_pk
        temp_dict['receiver_pk'] = i.receiver_pk
        temp_dict['buy_currency'] = i.buy_currency
        temp_dict['sell_currency'] = i.sell_currency
        temp_dict['buy_amount'] = i.buy_amount
        temp_dict['sell_amount'] = i.sell_amount
        temp_dict['signature'] = i.signature
        temp_dict['tx_id'] = i.tx_id
        temp_dict['order_id'] = i.order_id
        instance_list.append(temp_dict)

    result22 = {}
    result22['data'] = instance_list
    result_json = json.dumps(result22)
    #Note that you can access the database session using g.session
    return jsonify(result22)

if __name__ == '__main__':
    app.run(port='5002')
