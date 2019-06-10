#http://127.0.0.1:5000/
#access_token=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRQUkgiLCJzdWIiOiI3SFhNU0giLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTU4NDgyMjA4LCJpYXQiOjE1NTc4Nzc0MDh9.g96TpJm5RT_U9-S54w2x17EJeqgfV2DNMHzT9kMzmNM&user_id=7HXMSH&scope=social+heartrate+profile+settings+activity+weight+nutrition+sleep+location&token_type=Bearer&expires_in=604800
import base64
import urllib
import urllib.parse
import urllib.request
from urllib.parse import urlencode, quote_plus
#These are the secrets etc from Fitbit developer
OAuthTwoClientID = '22DPRH'
ClientOrConsumerSecret = '51e59afa5261d6dd4afad27658f2984f'

#This is the Fitbit URL
TokenURL = "https://api.fitbit.com/oauth2/token"

#I got this from the first verifier part when authorising my application
AuthorisationCode = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRQUkgiLCJzdWIiOiI3SFhNU0giLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTU4NDgyMjA4LCJpYXQiOjE1NTc4Nzc0MDh9.g96TpJm5RT_U9-S54w2x17EJeqgfV2DNMHzT9kMzmNM'


#Form the data payload
BodyText = {'code' : AuthorisationCode,
            'redirect_uri' : 'http://pdwhomeautomation.blogspot.co.uk/',
            'client_id' : OAuthTwoClientID,
            'grant_type' : 'authorization_code'}

BodyURLEncoded = urllib.parse.urlencode(BodyText)
print(BodyURLEncoded)

#Start the request
req = urllib.Request(TokenURL,BodyURLEncoded)

#Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
req.add_header('Authorization', 'Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

#Fire off the request

response = urllib.request.urlopen(req)

FullResponse = response.read()

print("Output >>> " + FullResponse)
'''
except urllib2.URLError as e:
 print(e.code)
 print(e.read())
'''
