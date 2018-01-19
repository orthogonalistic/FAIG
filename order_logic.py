#!/usr/bin/env python
# -*- coding: utf-8 -*-
import settings
import variables
import requests
import json
import random
import time as systime
import datetime


class Order_logic:

    def what_is_the_order(self):
        base_url = settings.REAL_OR_NO_REAL + '/markets/' + settings.epic_id
        auth_r = requests.get(base_url, headers=variables.authenticated_headers)
        d = json.loads(auth_r.text)

        current_price = d['snapshot']['bid']
        Price_Change_Day = d['snapshot']['netChange']
        variables.price_diff = current_price - variables.price_prediction


        print("STOP LOSS DISTANCE WILL BE SET AT : " + str(settings.stopDistance_value))
        print("Price Difference Away (Point's) : " + str(variables.price_diff))
    # MUST NOTE :- IF THIS PRICE IS - THEN BUY!! i.e NOT HIT TARGET YET, CONVERSELY IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
    # MUST NOTE :- IF THIS PRICE IS - THEN BUY!! i.e NOT HIT TARGET YET, CONVERSELY IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
    # MUST NOTE :- IF THIS PRICE IS - THEN BUY!! i.e NOT HIT TARGET YET, CONVERSELY IF TH

    def determine_trade_direction(self):
        if variables.profitable_trade_count < 15:
            if variables.price_diff < 0 and variables.score > settings.predict_accuracy:
                variables.limitDistance_value = "4"
                variables.DIRECTION_TO_TRADE = "BUY"
                variables.DIRECTION_TO_CLOSE = "SELL"
                variables.DIRECTION_TO_COMPARE = 'bid'
                variables.DO_A_THING = True
            elif variables.price_diff > 0 and variables.score > settings.predict_accuracy:
                # It's OVER the predicted price, Keep going but keep it tight?? Tight limit!! Take small profits
                variables.limitDistance_value = "1"
                variables.DIRECTION_TO_TRADE = "SELL"
                variables.DIRECTION_TO_CLOSE = "BUY"
                variables.DIRECTION_TO_COMPARE = 'offer'
                variables.DO_A_THING = True
        elif variables.profitable_trade_count > 15:  # 15, Trades ... profit. Right???
            variables.profitable_trade_count = 0
            if variables.price_diff < 0 and variables.score > settings.predict_accuracy:
                # Be Extra Sure, Set stop loss very tight???
                variables.limitDistance_value = "1"
                variables.DIRECTION_TO_TRADE = "SELL"
                variables.DIRECTION_TO_CLOSE = "BUY"
                variables.DIRECTION_TO_COMPARE = 'offer'
                variables.DO_A_THING = True
            elif variables.price_diff > 0 and variables.score > settings.predict_accuracy:
                # Be Extra Sure, Set stop loss very tight???
                variables.limitDistance_value = "1"
                variables.DIRECTION_TO_TRADE = "SELL"
                variables.DIRECTION_TO_CLOSE = "BUY"
                variables.DIRECTION_TO_COMPARE = 'offer'
                variables.DO_A_THING = True
                # Be Extra Sure, Set stop loss very tight???
                # this looks wrong - the code below should be before the elif?
                variables.limitDistance_value = "1"
                variables.DIRECTION_TO_TRADE = "BUY"
                variables.DIRECTION_TO_CLOSE = "SELL"
                variables.DIRECTION_TO_COMPARE = 'bid'
                variables.DO_A_THING = True
        print(
            "!!DEBUG TIME!! : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
        ################################################################
        #############Predict Accuracy isn't that great. ################
        #############Predict Accuracy isn't that great. ################
        #############Predict Accuracy isn't that great. ################
        #############Predict Accuracy isn't that great. ################
        ################################################################
        Prediction_Wait_Timer = int(
            1800)  # Wait 30 mins and Try again, Enough data should have changed to make a suitable prediction by then.
        # Be-careful after hours, After 5PM and 9PM GMT, Volumes are low yada yada yada. Less likely to get a decent prediction
        print(
            "!!DEBUG TIME!! : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
        if variables.price_diff < 0 and variables.score < settings.predict_accuracy:
            variables.DO_A_THING = False
            print("!!DEBUG TIME!! Prediction Wait Algo: " + str(
                datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
            systime.sleep(Prediction_Wait_Timer)
            print("!!DEBUG TIME!! Prediction Wait Algo: " + str(
                datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
        elif variables.price_diff > 0 and variables.score < settings.predict_accuracy:
            variables.DO_A_THING = False
            print("!!DEBUG TIME!! Prediction Wait Algo: " + str(
                datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
            systime.sleep(Prediction_Wait_Timer)
            print("!!DEBUG TIME!! Prediction Wait Algo: " + str(
                datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
