# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from mailgun import Mailgun
from saveTweetId import SaveTweetId

#get them working here again without publishing them to git
#figure out scheduling
#open a file called "apikeys" with keys and tokens for Twitter separated by newlines
with open('apikeys.txt', 'r') as keyFile:
    keyFile = open('apikeys.txt', 'r')
    ACCESS_TOKEN = keyFile.readline().rstrip()
    ACCESS_TOKEN_SECRET = keyFile.readline().rstrip()
    CONSUMER_KEY = keyFile.readline().rstrip()
    CONSUMER_SECRET = keyFile.readline().rstrip()
    MAILGUN_KEY = keyFile.readline().rstrip()
keyFile.closed

oauth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)

#this is the text I'm looking for in the tweets
importantWord = "berlin"

#I only care about tweets I haven't seen yet
#read the last tweet ID from the file holding it
#for testing purposes, a few tweets ago is 681658764840140800
with open('lastTweetId.txt', 'r') as f:
    readData = f.read()
f.closed

# Get a particular user's timeline (up to 3,200 of his/her most recent tweets).
# this is for amanda palmer, since I last looked at it, excluding replies and retweets
lastTweets = twitter.statuses.user_timeline.tweets(screen_name="amandapalmer", since_id = int(readData),
                                                   exclude_replies = "true", include_rts = "false")

#step through list of last tweets
for i in lastTweets:
    #strip the text out of the json of the tweet
    thisTweet = i['text']

    #look for the trigger word
    if importantWord in thisTweet.lower():
        #trigger an email with the full text of the tweet
        Mailgun(MAILGUN_KEY, thisTweet)

#get the last tweet's ID and save it out to a file so I only start looking from there
if len(lastTweets)>0:
    SaveTweetId(lastTweets[0]['id'])
