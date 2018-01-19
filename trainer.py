#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
import settings
import variables


class Trainer:

    def train_data(self):

        resolutions = ["MINUTE", "MINUTE_2", "MINUTE_3", "MINUTE_5", "MINUTE_10", "MINUTE_15", "MINUTE_30", "HOUR", "HOUR_2",
                   "HOUR_3", "HOUR_4", "DAY"]
        price_compare = "bid"

        for res in resolutions:
            base_url = settings.REAL_OR_NO_REAL + '/prices/' + settings.epic_id + '/' + res + '/10'
            auth_r = requests.get(base_url, headers=variables.authenticated_headers)
            d = json.loads(auth_r.text)

            # print ("-----------------DEBUG-----------------")
            # print(base_url)
            # print(auth_r.status_code)
            # print(auth_r.reason)
            # print (auth_r.text)
            # print ("-----------------DEBUG-----------------")

            for i in d['prices']:
                tmp_list = []
                high_price = i['highPrice'][price_compare]
                low_price = i['lowPrice'][price_compare]
                volume = i['lastTradedVolume']
                # ---------------------------------
                tmp_list.append(float(low_price))
                tmp_list.append(float(volume))
                variables.x.append(tmp_list)
                # x is Low Price and Volume
                variables.y.append(float(high_price))
                # y = High Prices


        base_url = settings.REAL_OR_NO_REAL + '/prices/' + settings.epic_id + '/DAY/1'
        # Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
        auth_r = requests.get(base_url, headers=variables.authenticated_headers)
        d = json.loads(auth_r.text)
        # I only need this API call for real world values
        remaining_allowance = d['allowance']['remainingAllowance']

        print("-----------------DEBUG-----------------")
        print("Remaining API Calls left : " + str(remaining_allowance))
        print("-----------------DEBUG-----------------")

        # print ("-----------------DEBUG-----------------")
        # print(auth_r.status_code)
        # print(auth_r.reason)
        # print (auth_r.text)
        # print ("-----------------DEBUG-----------------")

        for i in d['prices']:
            self.low_price = i['lowPrice'][price_compare]
            self.volume = i['lastTradedVolume']

    def predict(self):

        x = np.asarray(variables.x)
        y = np.asarray(variables.y)
        # Initialize the model then train it on the data
        genius_regression_model = LinearRegression()
        genius_regression_model.fit(x, y)
        # Predict the corresponding value of Y for X
        pred_ict = [self.low_price, self.volume]
        pred_ict = np.asarray(pred_ict)  # To Numpy Array, hacky but good!!
        pred_ict = pred_ict.reshape(1, -1)
        variables.price_prediction = genius_regression_model.predict(pred_ict)
        print("PRICE PREDICTION FOR PRICE " + settings.epic_id + " IS : " + str(variables.price_prediction))

        variables.score = genius_regression_model.score(x, y)
        variables.predictions = {'intercept': genius_regression_model.intercept_, 'coefficient': genius_regression_model.coef_,
                       'predicted_value': variables.price_prediction, 'accuracy': variables.score}

        print("-----------------DEBUG-----------------")
        print(variables.score)
        print(variables.predictions)
        print("-----------------DEBUG-----------------")


