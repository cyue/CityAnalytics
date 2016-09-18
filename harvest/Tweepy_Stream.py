# encoding=utf8  

import tweepy
import socket
import requests
import time
from authentication import authentication  # Consumer and access token/key
import sys 
import json
import googlemaps
import couchdb
import smtplib
from textblob import TextBlob
reload(sys)  
sys.setdefaultencoding('utf8')

def notification(msg):
    FROM ="professional.bigdata@hotmail.com"
    TO =["edwardgao46@yahoo.com.au"]

    SUBJECT = "Google API is reaching the limit!!"
    TEXT = msg
    message = """Subject: %s\n
        %s
        """%(SUBJECT,TEXT)
#smtp.live.com
    server = smtplib.SMTP('smtp-mail.outlook.com',port = 587)
    server.starttls()
    server.login('professional.bigdata@hotmail.com','professional@bigdata')
    server.sendmail(FROM,TO,message)
    server.quit()

def add_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

class TwitterStreamListener(tweepy.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, api=None):
        super(TwitterStreamListener, self).__init__()
        self.num_tweets = 0
        self.total = 0

    def on_status(self, status):
        
        if self.num_tweets < 2500:
            if status.user.name != None and status.user.profile_image_url_https != None and status.text != None and status.place != None and status.place.full_name == "Melbourne, Victoria":
                if status.id_str not in data_base:
                    self.total += 1
                    print self.total, ':', status.id
                    json_result = status._json
                    first_name = status.user.name.split(' ', 1)[0]
                    text = status.text
                    status._json['sentiment_score'] = add_sentiment(text)
                    if status.coordinates != None:
                        self.num_tweets += 1

                        print(status.coordinates["coordinates"])
                        lat = status.coordinates["coordinates"][1]
                        lon = status.coordinates["coordinates"][0]
                        suburb = ""
                        postal_code = ""
                        reverse_geocode_result = gmaps.reverse_geocode((lat,lon))
                        for each in reverse_geocode_result:
                            for one in each['address_components']:
                                if suburb == "" or postal_code == "":
                                    if one['types'] == ['locality', 'political']:
                                        print(one['long_name'])
                                        suburb = one['long_name']
                                    if one['types'] == ['postal_code']:
                                        print(one['long_name'])
                                        postal_code = one['long_name']
                        if suburb != "" and postal_code != "":
                            json_result['suburb'] = suburb
                            json_result['postal_code'] = postal_code
                            json_result['has_coor'] = 'True'
                        # print(json_result)
                        else:
                            json_result['suburb'] = ""
                            json_result['postal_code'] = '0000'
                            json_result['has_coor'] = 'False'
                    else:
                        json_result['suburb'] = ""
                        json_result['postal_code'] = '0000'
                        json_result['has_coor'] = 'False'

                    data_base[status.id_str] = json_result  #adding json to database
                    return True  
        else:
            notification('Google API is reaching the limit')
            return False

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes
    
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            print('out of limit')
    
    
if __name__ == '__main__':
    print('begin')

    # Get access and key from another class
    auth = authentication()

    consumer_key = auth.getconsumer_key()
    consumer_secret = auth.getconsumer_secret()

    access_token = auth.getaccess_token()
    access_token_secret = auth.getaccess_token_secret()
 
 # create and connect to database
    couch = couchdb.Server('http://115.146.89.121:5984/')
    try:
        data_base = couch.create('melbourne_tweets')
    except couchdb.http.PreconditionFailed as e:
        data_base = couch['melbourne_tweets']

    gmaps = googlemaps.Client(key='AIzaSyDoYjw_LY3nG43wpnulJbLyuK2NcUXVsvo')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
    # terms = ['Melbourne']
    myStream.filter(locations = [144.593742, -38.433859,145.512529, -37.511274], async=True)
    
    #144.593742, -37.972567, 144.900004, -37.511274
