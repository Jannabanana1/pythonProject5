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
import sys

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()


""" Suggested helper methods """
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

def findMatch(orderID):
   
    newOrder = g.session.query(Order).filter(Order.id == orderID).first()
    newOrderSellCurrency = newOrder.sell_currency
    newOrderSellAmount = newOrder.sell_amount
    if newOrderSellAmount == 0:
        return
    newOrderBuyCurrency = newOrder.buy_currency
    newOrderBuyAmount = newOrder.buy_amount
    newOrderExchangeRate = newOrderBuyAmount/newOrderSellAmount
    # this means no match at all
    if (g.session.query(Order).filter(Order.filled.is_(None), Order.buy_currency == newOrderSellCurrency, Order.sell_currency == newOrderBuyCurrency,
                                                  ((Order.sell_amount * newOrderSellAmount) >= (Order.buy_amount * newOrderBuyAmount)),
                                                  ((Order.sell_amount/Order.buy_amount) >= newOrderExchangeRate),).count()) == 0:
      return
    else:
        existingOrder = g.session.query(Order).filter(Order.filled.is_(None), Order.buy_currency == newOrderSellCurrency, Order.sell_currency == newOrderBuyCurrency,
                                                  ((Order.sell_amount * newOrderSellAmount) >= (Order.buy_amount * newOrderBuyAmount)),
                                                  ((Order.sell_amount/Order.buy_amount) >= newOrderExchangeRate),).first()
        # this means new order is fulfilled
        if (newOrderBuyAmount <= 0):
            return
       
        if (existingOrder.sell_amount == newOrderBuyAmount) or (existingOrder.buy_amount == newOrderSellAmount):
            mytimestamp = datetime.now()
            newOrder.filled = mytimestamp
            newOrder.counterparty_id = existingOrder.id
            existingOrder.filled = mytimestamp
            existingOrder.counterparty_id = newOrder.id
            newOrderBuyAmount = 0
            g.session.commit()
            return
       
        else:
            g.session.commit()
            #if I
            if (existingOrder.buy_amount <= newOrderSellAmount and newOrderBuyAmount >= existingOrder.sell_amount):
                remain_buy = newOrderBuyAmount - existingOrder.sell_amount
                new_sell_amount = remain_buy/newOrderExchangeRate
                '''
                if (new_sell_amount > int(remain_buy/newOrderExchangeRate)):
                    new_sell_amount = int(remain_buy/newOrderExchangeRate) + 1
                else:
                    new_sell_amount = int(remain_buy/newOrderExchangeRate)
                '''
                child_id = insert_child_order(newOrder.id, newOrder.sender_pk,newOrder.receiver_pk, newOrder.buy_currency,
                                            newOrder.sell_currency,remain_buy, new_sell_amount,newOrder.signature)
                mytimestamp = datetime.now()
                newOrder.filled = mytimestamp
                newOrder.counterparty_id = existingOrder.id
                existingOrder.filled = mytimestamp
                existingOrder.counterparty_id = newOrder.id
                g.session.commit()
                #findMatch(child_id)
                #g.session.commit()
                return
            elif (existingOrder.buy_amount >= newOrderSellAmount and newOrderBuyAmount <= existingOrder.sell_amount):
               
                exist_ex_rate = existingOrder.sell_amount/existingOrder.buy_amount
                remain_buy = existingOrder.buy_amount - newOrderSellAmount

                exist_new_sell_amount = remain_buy * exist_ex_rate
                '''
                if (exist_new_sell_amount > int(remain_buy * exist_ex_rate)):
                    exist_new_sell_amount = int(remain_buy * exist_ex_rate) - 1
                else:
                    exist_new_sell_amount = int(remain_buy * exist_ex_rate)
                '''
                child_id = insert_child_order(existingOrder.id, existingOrder.sender_pk,existingOrder.receiver_pk, existingOrder.buy_currency,
                                            existingOrder.sell_currency,remain_buy, exist_new_sell_amount, existingOrder.signature)
                mytimestamp = datetime.now()
                newOrder.filled = mytimestamp
                newOrder.counterparty_id = existingOrder.id
                existingOrder.filled = mytimestamp
                existingOrder.counterparty_id = newOrder.id
                g.session.commit()
                #findMatch(child_id)
                #g.session.commit()
                return
                 
    return

def check_sig(payload,sig):
    result = False
    #content = request.get_json(silent=True)
    #sig = content['sig']
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


def fill_order(order,txes=[]):
    orderID = insert_order(order)
    findMatch(orderID)
    pass
 
def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    # Hint: use json.dumps or str() to get it in a nice string form
    g.session.add(Log(message = json.dumps(d['payload'])))
    g.session.commit()
    pass

""" End of helper methods """



@app.route('/trade', methods=['POST'])
def trade():
    print("In trade endpoint")
    if request.method == "POST":
        content = request.get_json(silent=True)
        print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]

        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
       
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
           
        #Your code here
        #Note that you can access the database session using g.session
                # TODO: Check the signature
        verify_bool = False
        verify_bool = check_sig(content['payload'],content['sig'])

        # TODO: Add the order to the database
        if verify_bool == False:
            #send the message to the Log table
            log_message(content)
        else:
            # store the signature, as well as all of the fields under the ‘payload’ in the “Order” table EXCEPT for 'platform’
            fill_order(content)
        # TODO: Fill the order
       
        # TODO: Be sure to return jsonify(True) or jsonify(False) depending on if the method was successful
        return jsonify(verify_bool)
       

@app.route('/order_book')
def order_book():
    #Your code here
    #Note that you can access the database session using g.session
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
        instance_list.append(temp_dict)

    result22 = {}
    result22['data'] = instance_list
    result_json = json.dumps(result22)
    #Note that you can access the database session using g.session
    return jsonify(result22)
    #return jsonify(result_json)

if __name__ == '__main__':
    app.run(port='5002')
