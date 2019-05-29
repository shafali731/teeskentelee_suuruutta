import json
import urllib.request as request
import datetime
import random

'''
<script src="https://developer.edamam.com/attribution/badge.js"></script>
<div id="edamam-badge" data-color="white"></div>
'''

headers = {}
app_key = '8b15f0facc2412021d9b6693a2d8f744'
app_id = '9dfcb055'
URL_STUB = 'https://api.edamam.com/api/food-database/parser?'

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

def first(name):
    '''
    {your app_id}&app_key={your app_key}'
    https://api.edamam.com/api/food-database/parser?ingr=50%2B&app_id=9dfcb055&app_key=8b15f0facc2412021d9b6693a2d8f744

    '''
    info = name.split()
    #print(info)
    foods = ""
    for part in info:
        foods += part + "%20"
    #print(foods)
    foods = foods[:-3]
    #print(foods)
    URL = URL_STUB + "ingr=" + foods + '&app_id={}&app_key={}'.format('9dfcb055','8b15f0facc2412021d9b6693a2d8f744')
    #print(URL)
    return access_info(URL)

def second(calories):
    '''
    given calories gives preset
    hi doesnt work
    {your app_id}&app_key={your app_key}'
    https://api.edamam.com/api/food-database/parser?ingr=50%2B&app_id=9dfcb055&app_key=8b15f0facc2412021d9b6693a2d8f744

    '''

    cal = calories

    #print(foods)
    URL = URL_STUB + "cal=" + cal + '&app_id={}&app_key={}'.format('9dfcb055','8b15f0facc2412021d9b6693a2d8f744')
    #print(URL)
    return access_info(URL)

def third(calories1,calories2, name):
    '''
    {your app_id}&app_key={your app_key}'
    https://api.edamam.com/api/food-database/parser?ingr=50%2B&app_id=9dfcb055&app_key=8b15f0facc2412021d9b6693a2d8f744

    '''
    mincal = calories1
    maxcal = calories2
    info = name.split()
    #print(info)
    foods = ""
    for part in info:
        foods += part + "%20"
    #print(foods)
    foods = foods[:-3]
    #print(foods)

    URL = URL_STUB + "ingr=" + foods + "&cal=" + mincal + "-" + maxcal + '&app_id={}&app_key={}'.format('9dfcb055','8b15f0facc2412021d9b6693a2d8f744')
    return access_info(URL)
#print(first(app_key,app_id))

def getFoodDict(min_cal,max_cal):
    letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    dict={} # key= letter val= url
    for i in letters:
        URL = URL_STUB + "ingr=" + i + "&cal=" + min_cal + "-" + max_cal + '&app_id={}&app_key={}'.format('9dfcb055','8b15f0facc2412021d9b6693a2d8f744')
        dict[i]= URL
    #print(dict)
    return dict

def fourth(min_cal,max_cal,meal_num):
    letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    url_dict= getFoodDict(min_cal,max_cal)
    result=[] #len is equal to meal_num

    for i in range(int(meal_num)):
        url = url_dict[random.choice(letters)]
        #print(url)
        result.append(access_info(url)) #returns many entries
        #print("this is the access info"+str(res))
        #print("this is the url"+str(url))
        #print("this is the result"+ str(result))
    #print(result)
    return result
