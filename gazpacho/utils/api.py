import json
import urllib.request as request
import datetime
#import fitbit
#import gather_keys_oauth2 as Oauth2
#import pandas as pd

'''
following steps in guide.txt
akoroza@stuy.edu acct
'''
CLIENT_ID = '22DPCR'
CLIENT_SECRET = 'ad8ebc98651e30248f2ed723e9c4af74'
#user_id = '7JMR78'
user_id = '7HXMSH'
#access_token= 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRQQ1IiLCJzdWIiOiI3Sk1SNzgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTg5NTk1NTU4LCJpYXQiOjE1NTgwNTk1NTh9.mqwXb8hqENji9FDEsFztYsqpvmqfrrLOZx5FTKAD4ms'
access_token= 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRQQ1IiLCJzdWIiOiI3SFhNU0giLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTU4OTI0OTQzLCJpYXQiOjE1NTgzMjAxNDN9.2ounGhrbS1IIs463TOkV1kDAGnEsJ3eR1QPECeNe_44'
def access_info(URL_STUB, API_KEY = None, **kwargs):
    '''
    #Helper to access the info for a URL. Returns the JSON.
    #Params: URL_STUB, API_KEY = None, **kwargs for applying headers to requests
    # API_KEY should only be used if the key can be put in the URL. Otherwise, use **kwargs.
    '''
    # if there's an API key that is not a header
    if API_KEY:
        URL = URL_STUB + API_KEY
    else:
        URL = URL_STUB
    request_object = request.Request(URL)
    # iterate through, adding headers if needed
    for key, value in kwargs.items():
        request_object.add_header(key, value)
    '''
    try:
        response = request.urlopen(request_object)
    except:
        print("oogabooga")
        return None
    '''
    response = request.urlopen(request_object)
    response = response.read()
    info = json.loads(response)
    return info

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ API FUNCS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

headers = {}
headers['Authorization'] = "Bearer " + access_token
URL_STUB= 'https://api.fitbit.com/1/user/'

def fetchProfile(user_id):
    '''
    Fetches general profile information, expects string inputs
    '''
    URL= URL_STUB+ '{}/profile.json'.format(user_id)
    return access_info(URL,**headers)

def fetchHeartRateDP(user_id,date,period):
    '''
    Fetches user Heart Rate data in the /1/user/[user-id]/activities/heart/date/[date]/[period].json format
    date: The end date of the period specified in the format yyyy-MM-dd or today.
    period: The range for which data will be returned. Options are 1d, 7d, 30d, 1w, 1m.
    Returns dicts with time and associated heart rate values
    '''
    URL= URL_STUB+ '{}/activities/heart/date/{}/{}.json'.format(user_id,date,period)
    return access_info(URL,**headers)

def fetchHeartRateBE(user_id,base_date,end_date):
    '''
    Fetches user Heart Rate data in the /1/user/[user-id]/activities/heart/date/[base-date]/[end-date].json format
    base-date: The range start date, in the format yyyy-MM-dd or today.
    end-date: The end date of the range.
    Returns dicts with time and associated heart rate values
    '''
    URL= URL_STUB+ '{}/activities/heart/date/{}/{}.json'.format(user_id,base_date,end_date)
    return access_info(URL,**headers)

def getFaveFood(user_id):
    '''
    GET https://api.fitbit.com/1/user/[user-id]/foods/log/favorite.json
    '''
    URL= URL_STUB+'{}/foods/log/favorite.json'.format(user_id)
    return access_info(URL,**headers)

def getFoodInfo(food_id):
    '''
    GET https://api.fitbit.com/1/foods/[food-id].json
    '''
    URL= 'https://api.fitbit.com/1/foods/{}.json'.format(food_id)
    return access_info(URL,**headers)

'''
TESTING
'''
#fetchProfile(user_id)
#fetchHeartRateDP(user_id,'today','1d')
#fetchHeartRateBE(user_id,'today','today')
#print(getFaveFood(user_id))
print(getFoodInfo(12323))
