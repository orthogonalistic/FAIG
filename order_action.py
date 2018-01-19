#!/usr/bin/env python
# -*- coding: utf-8 -*-
import settings
import variables
import requests
import json
import random
import time as systime
import datetime


def action_the_order():
    base_url = settings.REAL_OR_NO_REAL + '/positions/otc'
    # authenticated_headers = {'Content-Type':'application/json; charset=utf-8',
    # 		'Accept':'application/json; charset=utf-8',
    # 		'X-IG-API-KEY':API_KEY,
    # 		'CST':CST_token,
    # 		'X-SECURITY-TOKEN':x_sec_token}

    data = {"direction": variables.DIRECTION_TO_TRADE,
            "epic": settings.epic_id,
            "limitDistance": settings.limitDistance_value,
            "orderType": settings.orderType_value,
            "size": settings.size_value,
            "expiry": settings.expiry_value,
            "guaranteedStop": settings.guaranteedStop_value,
            "currencyCode": settings.currencyCode_value,
            "forceOpen": settings.forceOpen_value,
            "stopDistance": settings.stopDistance_value}

    r = requests.post(base_url,
                      data=json.dumps(data),
                      headers=variables.authenticated_headers)

    print("-----------------DEBUG-----------------")
    print(r.status_code)
    print(r.reason)
    print(r.text)
    print("-----------------DEBUG-----------------")

    d = json.loads(r.text)
    deal_ref = d['dealReference']
    systime.sleep(2)
    # MAKE AN ORDER
    # CONFIRM MARKET ORDER
    base_url = settings.REAL_OR_NO_REAL + '/confirms/' + deal_ref
    auth_r = requests.get(base_url, headers=variables.authenticated_headers)
    d = json.loads(auth_r.text)
    DEAL_ID = d['dealId']
    print("DEAL ID : " + str(d['dealId']))
    print(d['dealStatus'])
    print(d['reason'])

    # the trade will only break even once the price of the asset being traded has surpassed the sell price (for long trades) or buy price (for short trades).
    # READ IN INITIAL PROFIT

    base_url = settings.REAL_OR_NO_REAL + '/positions/' + DEAL_ID
    auth_r = requests.get(base_url, headers=variables.authenticated_headers)
    d = json.loads(auth_r.text)

    print("-----------------DEBUG-----------------")
    print(r.status_code)
    print(r.reason)
    print(r.text)
    print("-----------------DEBUG-----------------")

    if variables.DIRECTION_TO_TRADE == "SELL":
        PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][variables.DIRECTION_TO_COMPARE])
        PROFIT_OR_LOSS = PROFIT_OR_LOSS * float(settings.size_value)
        print("\rDeal Number : " + str(variables.times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS), end="")
    else:
        PROFIT_OR_LOSS = float(d['market'][variables.DIRECTION_TO_COMPARE] - float(d['position']['openLevel']))
        PROFIT_OR_LOSS = PROFIT_OR_LOSS * float(settings.size_value)
        print("\rDeal Number : " + str(variables.times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS), end="")

    # KEEP READING IN FOR PROFIT
    try:
        # while PROFIT_OR_LOSS < float(limitDistance_value):
        while PROFIT_OR_LOSS < float(4.00):  # Take something from the market, Before Take Profit.
            base_url = settings.REAL_OR_NO_REAL + '/positions/' + DEAL_ID
            auth_r = requests.get(base_url, headers=variables.authenticated_headers)
            d = json.loads(auth_r.text)

            while not int(auth_r.status_code) == 200:
                if int(auth_r.status_code) == 400 or int(auth_r.status_code) == 404:
                    break
                # This is a good thing!! It means that It cannot find the Deal ID, Your take profit has been hit.

                # Cannot read from API, Wait and try again
                # Give the Internet/IG 30s to sort it's shit out and try again
                systime.sleep(30)
                print("-----------------DEBUG-----------------")
                print("HTTP API ERROR!! Please check your Internet connection and Try again...")
                print("Check Ping and Latency between you and IG Index Servers")
                # print(auth_r.status_code)
                # print(auth_r.reason)
                # print (auth_r.text)
                print("-----------------DEBUG-----------------")
                # Got some "basic" error checking after all
                base_url = settings.REAL_OR_NO_REAL + '/positions/' + DEAL_ID
                auth_r = requests.get(base_url, headers=variables.authenticated_headers)
                d = json.loads(auth_r.text)

            if variables.DIRECTION_TO_TRADE == "SELL":
                PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][variables.DIRECTION_TO_COMPARE])
                PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][variables.DIRECTION_TO_COMPARE])
                PROFIT_OR_LOSS = float(PROFIT_OR_LOSS * float(settings.size_value))
                print("\rDeal Number : " + str(variables.times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS), end="")
                systime.sleep(2)  # Don't be too keen to read price
            else:
                PROFIT_OR_LOSS = float(d['market'][variables.DIRECTION_TO_COMPARE] - float(d['position']['openLevel']))
                PROFIT_OR_LOSS = float(PROFIT_OR_LOSS * float(settings.size_value))
                print("\rDeal Number : " + str(variables.times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS), end="")
                systime.sleep(2)  # Don't be too keen to read price

        # ARTIFICIAL_STOP_LOSS = int(size_value) * STOP_LOSS_MULTIPLIER
        # ARTIFICIAL_STOP_LOSS = ARTIFICIAL_STOP_LOSS * -1 #Make Negative, DO NOT REMOVE!!
        # print (PROFIT_OR_LOSS)
        # print (ARTIFICIAL_STOP_LOSS)

        # if PROFIT_OR_LOSS < ARTIFICIAL_STOP_LOSS:
        # #CLOSE TRADE/GTFO
        # print ("WARNING!! POTENTIAL DIRECTION CHANGE!!")
        # SIZE = size_value
        # ORDER_TYPE = orderType_value
        # base_url = REAL_OR_NO_REAL + '/positions/otc'
        # data = {"dealId":DEAL_ID,"direction":DIRECTION_TO_CLOSE,"size":SIZE,"orderType":ORDER_TYPE}
        # #authenticated_headers_delete IS HACKY AF WORK AROUND!! AS PER .... https://labs.ig.com/node/36
        # authenticated_headers_delete = {'Content-Type':'application/json; charset=utf-8',
        # 'Accept':'application/json; charset=utf-8',
        # 'X-IG-API-KEY':API_KEY,
        # 'CST':CST_token,
        # 'X-SECURITY-TOKEN':x_sec_token,
        # '_method':"DELETE"}
        # auth_r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers_delete)
        # #DEBUG
        # print(r.status_code)
        # print(r.reason)
        # print (r.text)
        # systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER)) #Obligatory Wait before doing next order

    except Exception as e:
        print(e)  # Yeah, I know now.
        print("ERROR : ORDER MIGHT NOT BE OPEN FOR WHATEVER REASON")
        # WOAH CALM DOWN! WAIT .... STOP LOSS MIGHT HAVE BEEN HIT (Or take Profit)
        systime.sleep(random.randint(1, settings.TIME_WAIT_MULTIPLIER))
        pass

    # systime.sleep(1)

    if PROFIT_OR_LOSS > 0:
        profitable_trade_count = int(variables.profitable_trade_count) + 1
        print("DEBUG : ASSUME PROFIT!! Profitable Trade Count " + str(profitable_trade_count))
        SIZE = settings.size_value
        ORDER_TYPE = settings.orderType_value

        base_url = settings.REAL_OR_NO_REAL + '/positions/otc'
        data = {"dealId": DEAL_ID, "direction": variables.DIRECTION_TO_CLOSE, "size": SIZE, "orderType": ORDER_TYPE}
        # authenticated_headers_delete IS HACKY AF WORK AROUND!! AS PER .... https://labs.ig.com/node/36
        authenticated_headers_delete = {'Content-Type': 'application/json; charset=utf-8',
                                        'Accept': 'application/json; charset=utf-8',
                                        'X-IG-API-KEY': settings.API_KEY,
                                        'CST': variables.CST_token,
                                        'X-SECURITY-TOKEN': variables.x_sec_token,
                                        '_method': "DELETE"}

        auth_r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers_delete)
        # CLOSE TRADE
        print(auth_r.status_code)
        print(auth_r.reason)
        print(auth_r.text)

        # #CONFIRM CLOSE - FUTURE
        # base_url = REAL_OR_NO_REAL + '/confirms/'+ deal_ref
        # auth_r = requests.get(base_url, headers=authenticated_headers)
        # d = json.loads(auth_r.text)
        # DEAL_ID = d['dealId']
        # print("DEAL ID : " + str(d['dealId']))
        # print(d['dealStatus'])
        # print(d['reason'])

        systime.sleep(random.randint(1, settings.TIME_WAIT_MULTIPLIER))  # Obligatory Wait before doing next order
