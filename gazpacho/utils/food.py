import json
import urllib.request as request
import datetime
import random

'''
<script src="https://developer.edamam.com/attribution/badge.js"></script>
<div id="edamam-badge" data-color="white"></div>
'''

headers = {}
'''
food API keys
'''
app_key = '8b15f0facc2412021d9b6693a2d8f744'
app_id = '9dfcb055'

key= 'ac3c302313ac7a9b7e2a6db8f9d782c4'
id= '90447ece'
URL_STUB = 'https://api.edamam.com/api/food-database/parser?'

'''
recipe API keys
'''
rec_key= '6e6d04afe39d8c384edc55ecb1ca836b'
rec_id= 'a554df2b'
URL_STUB2= 'https://api.edamam.com/search?'
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

'''
Note that first(), second(), and third(), are functions
'''
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
    '''
    Cycles through foods and returns dict where key= letter value= foods within min_ca && max_cal range
    '''
    letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    dict={} # key= letter val= url
    for i in letters:
        URL = URL_STUB + "ingr=" + i + "&cal=" + min_cal + "-" + max_cal + '&app_id={}&app_key={}'.format(id,key)
        dict[i]= URL
    #print(dict)
    return dict

def getMealDictResults(min_cal,max_cal,meal_num):
    '''
    Uses dict of possible foods to return a list of dicts of meal_num random letters
    Within user-set min and max cals
    '''
    letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    url_dict= getFoodDict(min_cal,max_cal)
    result=[] #len is equal to meal_num

    for i in range(int(meal_num)): #need to add a check to make sure input.type == int
        url = url_dict[random.choice(letters)]
        result.append(access_info(url))
        #result is three big different dictionaries
    return result

def getRandomMeals(min_cal,max_cal, meal_num):
    '''
    Uses list of dicts from getMealDictResults() to return list of only <meal_num> food items (label only)
    Broken up from getMealDictResults() for clarity
    '''
    dict_lst= getMealDictResults(min_cal,max_cal,meal_num)
    result=[]
    for dct in dict_lst:
        hint_lst= dct['hints']
        food= random.choice(hint_lst)['food']
        food_lbl=food['label']
        food_cal= ''
        if 'ENERC_KCAL' in food['nutrients'].keys(): #safegaurding against faulty entries
            food_cal=food['nutrients']['ENERC_KCAL']
        result.append([food_lbl,food_cal]) #lst of lists
    return result

def getRecipeDict(min_cal,max_cal):
    '''
    Cycles through foods and returns dict where key= letter and value= foods within min_ca && max_cal range
    q=chicken&app_id=${YOUR_APP_ID}&app_key=${YOUR_APP_KEY}&from=0&to=3&calories=591-722&health=alcohol-free
    ^^ the rest of functioning url stub
    https://api.edamam.com/search?q=S&app_id=$a554df2b&app_key=$6e6d04afe39d8c384edc55ecb1ca836b&from=0&to=10&calories=0-500&health=alcohol-free
    '''
    letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    dict={} # key= letter val= url
    for i in letters:
        auth_str= '&app_id={}&app_key={}'.format(rec_id,rec_key)
        URL = URL_STUB2 + "q=" + i + auth_str + '&from=0&to=10' + "&calories=" + min_cal + "-" + max_cal + '&health=alcohol-free'
        dict[i]= URL

    return dict

def getRecipeDictResults(min_cal,max_cal,meal_num):
    '''
    Uses dict of possible recipes to return a list of dicts of meal_num random letters
    Within user-set min and max cals
    '''
    letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    url_dict= getRecipeDict(min_cal,max_cal)
    result=[] #len is equal to meal_num

    for i in range(int(meal_num)): #need to add a check to make sure input.type == int
        url = url_dict[random.choice(letters)]
        result.append(access_info(url))
        #result is three big different dictionaries
    return result

def getRandomRecipes(min_cal,max_cal,meal_num):
    '''
    Uses list of dicts from getRecipeDictResults() to return list of only <meal_num> food items (label only)
    Broken up from getRecipeDictResults() for clarity
    '''
    dict_lst= getRecipeDictResults(min_cal,max_cal,meal_num)
    result=[]
    for dct in dict_lst:
        hit_lst= dct['hits']
        food= random.choice(hit_lst)['recipe']
        food_lbl=food['label']
        food_cal= int(food['calories']) / int(food['yield'])
        ingr_lst= food['ingredientLines']
        result.append([food_lbl,food_cal, ingr_lst]) #lst of lists
    return result

'''
Testing recipe
'''
#print(str(getFoodDict('0','500')))
#print(str(getRecipeDict('0','500')))
#print(str(getRecipeDictResults('0','500','1')))
#print(str(getRandomRecipes('400','500','1')))
