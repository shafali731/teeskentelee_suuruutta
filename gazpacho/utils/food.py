import json
import urllib.request as request
import datetime

'''
<script src="https://developer.edamam.com/attribution/badge.js"></script>
<div id="edamam-badge" data-color="white"></div>
'''

headers = {}
app_key = '8b15f0facc2412021d9b6693a2d8f744'
app_id = '9dfcb055'
URL_STUB = 'https://api.edamam.com/api/food-database/parser?ingr=red%20apple&app_id='

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Loading ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
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

def first(key,id):
    '''
    {your app_id}&app_key={your app_key}'
    https://api.edamam.com/api/food-database/parser?ingr=50%2B&app_id=9dfcb055&app_key=8b15f0facc2412021d9b6693a2d8f744
    
    '''

    URL = URL_STUB + '{}&app_key={}'.format(id,key)
    return access_info(URL);

print(first(app_key,app_id))
