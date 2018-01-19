#IF YOU FOUND THIS USEFUL, Please Donate some Bitcoin .... 1FWt366i5PdrxCC6ydyhD8iywUHQ2C7BWC

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import time
import datetime
import requests
import json
import logging
import sys
import urllib
from time import time, sleep
import random
import time as systime
from statistics import mean, median
import numpy as np
# We are gonna use Scikit's LinearRegression model
from sklearn.linear_model import LinearRegression

import trainer
import settings
import variables
import order_logic
import order_action


headers = {'Content-Type':'application/json; charset=utf-8',
        'Accept':'application/json; charset=utf-8',
        'X-IG-API-KEY':settings.API_KEY,
        'Version':'2'
		}

r = requests.post(settings.API_ENDPOINT, data=json.dumps(settings.data), headers=headers)
 
headers_json = dict(r.headers)
variables.CST_token = headers_json["CST"]
print (R"CST : " + variables.CST_token)
variables.x_sec_token = headers_json["X-SECURITY-TOKEN"]
print (R"X-SECURITY-TOKEN : " + variables.x_sec_token)

#GET ACCOUNTS
base_url = settings.REAL_OR_NO_REAL + '/accounts'
variables.authenticated_headers = {
		'Content-Type':'application/json; charset=utf-8',
        'Accept':'application/json; charset=utf-8',
        'X-IG-API-KEY':settings.API_KEY,
        'CST':variables.CST_token,
		'X-SECURITY-TOKEN':variables.x_sec_token
}

authenticated_headers = variables.authenticated_headers

auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)

for i in d['accounts']:
	if str(i['accountType']) == "SPREADBET":
		print ("Spreadbet Account ID is : " + str(i['accountId']))
		spreadbet_acc_id = str(i['accountId'])

#SET SPREAD BET ACCOUNT AS DEFAULT
base_url = settings.REAL_OR_NO_REAL + '/session'
data = {"accountId":spreadbet_acc_id,"defaultAccount": "True"}
auth_r = requests.put(base_url, data=json.dumps(data), headers=authenticated_headers)

# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)
#ERROR about account ID been the same, Ignore! 

###################################################################################
##########################END OF LOGIN CODE########################################
##########################END OF LOGIN CODE########################################
##########################END OF LOGIN CODE########################################
##########################END OF LOGIN CODE########################################
###################################################################################


base_url = settings.REAL_OR_NO_REAL + '/markets/' + settings.epic_id
auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

# print ("-----------------DEBUG-----------------")
# print(r.status_code)
# print(r.reason)
# print (r.text)
# print ("-----------------DEBUG-----------------")

MARKET_ID = d['instrument']['marketId']

#*******************************************************************
#*******************************************************************
#*******************************************************************
#*******************************************************************

#STOP_LOSS_MULTIPLIER = 4 #Not currently in use, 13th Jan


print ("START TIME : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))

for variables.times_round_loop in range(1, 9999):

#*******************************************************************
#*******************************************************************
#*******************************************************************
#*******************************************************************
	variables.DO_A_THING = False
	while not variables.DO_A_THING:
		print ("!!Internal Notes only - Top of Loop!! : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
		systime.sleep(random.randint(1, settings.TIME_WAIT_MULTIPLIER))
		low_price_list = []
		high_price_list = []
		close_price_list = []
		volume_list = []
		# Your input data, X and Y are lists (or Numpy Arrays)
		#THIS IS YOUR TRAINING DATA

		obj_trainer = trainer.Trainer()	#gets the training data
		obj_trainer.train_data()

		x = variables.x
		y = variables.y

		# Run predictor
		obj_trainer.predict()

		# Run order calculator
		obj_order_logic = order_logic.Order_logic()
		obj_order_logic.what_is_the_order()
		obj_order_logic.determine_trade_direction()

	# Run order action

	order_action.action_the_order()
		
