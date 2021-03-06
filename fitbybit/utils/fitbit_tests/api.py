import json
import urllib.request as request
import datetime
import fitbit
import gather_keys_oauth2 as Oauth2
#import pandas as pd

CLIENT_ID = '22DPT8'
CLIENT_SECRET = '75bdab2bae6505734820d543dee4fb21'
'''
Application registered on https://dev.fitbit.com/apps/details/22DPT8 with akoroza@stuy.edu
Following https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873 tutorial
https://github.com/stephenjhsu/fitbit/blob/master/fitbit.py

OAuth 2.0 Client ID ***
22DPT8

Client Secret ***
75bdab2bae6505734820d543dee4fb21

Callback URL
http://127.0.0.1:8080/
OAuth 2.0: Authorization URI
https://www.fitbit.com/oauth2/authorize
OAuth 2.0: Access/Refresh Token Request URI
https://api.fitbit.com/oauth2/token

Step 2 calls for an unofficial Fitbit API
python-fitbit (a complete python implementation of the Fitbit API.)
docs: https://python-fitbit.readthedocs.io/en/latest/
gh: https://github.com/orcasgit/python-fitbit

Extra requirements:
python-dateutil>=1.5   <-- The dateutil module provides powerful extensions to the datetime module available in the Python standard library.
requests-oauthlib>=0.7 <-- for accessing protected resources from Fitbit

pip3 install fitbit
cherrypy
numpy
pandas
'''

'''
Using the ID and Secret, we can obtain the access and refresh tokens that authorize us to get our data.
'''
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

'''
Formatting dates for api calls
'''
yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))


#fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=yesterday2, detail_level='1sec')


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

    try:
        response = request.urlopen(request_object)
    except:
        return None
    response = response.read()
    info = json.loads(response)
    return info

def get_bored_activity():
'''
    #Fetches an activity and returns that activity.
    #Returns a dict with:
    #- activity: the activity
'''
    data = access_info('https://www.boredapi.com/api/activity')
    result = {}
    result['activity'] = data['activity']
    result['type'] = data['type']
    result['participants'] = data['participants']
    return result

def get_quote():
'''
    #Returns a random quote and the author who said/wrote it.
    #Returns a dict with:
    #- quote: the quote
    #- author: the author
'''
    data = access_info('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback=')
    result = {}

    # strip off HTML and replace special quotes with reg quotes
    content = data[0]['content']
    content = content.replace('&#8217;','\'')
    content = content.strip('\n')
    content = content.strip('<p>')
    content = content.strip('</p>')
    content = content.strip()
    print(content)

    result['author'] = data[0]['title']
    result['quote'] = content
    return result

def get_word(query):
'''
    #Finds 100 possible words using the query parameter.
    #Returns a dict with:
    #- query: the query
    #- words: a list of all possible words
'''
    query = query.strip()

    #modify spacing
    query = query.replace(' ', '+')
    query = query.replace('%20', '+')
    URL = 'https://api.datamuse.com/sug?max=100&s={}'.format(query)
    data = access_info(URL)

    result = {}
    result['query'] = query
    result['words'] = []
    # distill down to necessary words
    for entry in data:
        result['words'].append(entry['word'])

    return result

def get_definition(query):
'''
    #Finds all possible defintions using the query parameter.
    #Returns a dict with:
    #- word: the query
    #- definitions: a list of all possible definitions
'''
    query = query.strip()
    file = open("api/oxford.txt", 'r').read()
    apikey = file.strip()
    if apikey == '':
        return 'No API key found'

    # add headers
    headers = {}
    headers['app_id'] = '1a82131d'
    headers['app_key'] = apikey

    # access info
    URL = 'https://od-api.oxforddictionaries.com/api/v1/entries/en/{}'.format(query)
    try:
        data = access_info(URL, **headers)
    except:
        return {}

    print(data)
    if data == None:
        return {}

    # distill down to necessary words
    result = {}
    result['word'] = query
    result['definitions'] = []

    #MORE FALSE POSITIVE CHECKING WHY ARE YOU LIKE THIS OXFORD
    if 'senses' in data['results'][0]['lexicalEntries'][0]['entries'][0].keys():
        for entry in data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']:
            # false positive handling
            if 'definitions' not in entry.keys():
                print('result:',result)
                return {}
            result['definitions'].append(entry['definitions'][0])
            if 'subsenses' in entry.keys():
                result['definitions'].append(entry['subsenses'][0]['definitions'][0])
    else:
        return {}

    #print('result:',result)
    return result
'''
if __name__ == '__main__':
    data = None
    print(get_word('djkfhnbglrjboierjriorjtotijgoirj'))
    # print(get_definition('Farm Bill'))
    # print(data==None)
