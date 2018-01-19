#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   FOR DEMO ....
REAL_OR_NO_REAL = 'https://demo-api.ig.com/gateway/deal'

API_ENDPOINT = "https://demo-api.ig.com/gateway/deal/session"
API_KEY = "*"
data = {"identifier":"*","password": "*"}


# FOR REAL....

#  REAL_OR_NO_REAL = 'https://api.ig.com/gateway/deal'
#API_ENDPOINT = "https://api.ig.com/gateway/deal/session"
#API_KEY = '*********************************'
#data = {"identifier":"*********************************","password": "*********************************"}


# ---------------------------

#HACKY/Weekend Testing - DO NOT USE!!! UNLESS YOU KNOW WHAT YOU ARE DOING!!
#epic_id = "CS.D.BITCOIN.TODAY.IP" #Bitcoin
#epic_id = "IX.D.SUNFUN.DAILY.IP" #Weekend Trading
#epic_id = "CS.D.ETHUSD.TODAY.IP" #Ether
#epic_id = "CS.D.BCHUSD.TODAY.IP" #Bitcoin Cash

#LIVE TEST
#epic_id = "CS.D.USCGC.TODAY.IP" #Gold - OK, Not Great
#epic_id = "CS.D.USCSI.TODAY.IP" #Silver - NOT RECOMMENDED
#epic_id = "IX.D.FTSE.DAILY.IP" #FTSE 100 - Within Hours only, Profitable
#epic_id = "IX.D.DOW.DAILY.IP" #Wall St - Definitely Profitable between half 6 and half 8 GMT
epic_id = "CS.D.GBPUSD.TODAY.IP" # - Very Profitable

# PROGRAMMABLE VALUES
# UNIT TEST FOR CRYPTO'S
# limitDistance_value = "1"
# orderType_value = "MARKET"
# size_value = "5"
# expiry_value = "DFB"
# guaranteedStop_value = True
# currencyCode_value = "GBP"
# forceOpen_value = True
# stopDistance_value = "150"

#UNIT TEST FOR OTHER STUFF
limitDistance_value = "4"
orderType_value = "MARKET"
size_value = "1"
expiry_value = "DFB"
guaranteedStop_value = True
currencyCode_value = "GBP"
forceOpen_value = True
stopDistance_value = "150" #Initial Stop loss, Worked out later per trade

predict_accuracy = 0.80
TIME_WAIT_MULTIPLIER = 60
