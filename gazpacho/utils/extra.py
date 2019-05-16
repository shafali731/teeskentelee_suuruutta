import json
import urllib.request as request
import datetime
#import fitbit
#import gather_keys_oauth2 as Oauth2
#import pandas as pd

'''
following steps in guide.txt
'''

CLIENT_ID = '22DPF8'
CLIENT_SECRET = 'fabb64e3960d30cf59578121653b8ad4'
user_id = '7HXMSH'
access_token= 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRQRjgiLCJzdWIiOiI3SFhNU0giLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTU4NTMzMTEzLCJpYXQiOjE1NTc5NzExNzJ9.2TYsRsmgj5T5J6C5-LCGJnSj37sPiyxOQoRr2CNlIII'



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

# add headers
headers = {}
headers['Authorization'] = "Bearer " + access_token
print(access_info('https://api.fitbit.com/1/user/7HXMSH/profile.json',**headers))

#omg wow it works lol i can sleep


#def
