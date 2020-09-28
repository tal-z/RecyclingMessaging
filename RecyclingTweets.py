import tweepy
import re
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Enter twitter app authentication info
consumer_key = 'u1h94WxNaGCfQG21aU1rlRzTx'
consumer_secret = 'aX5IRBORH4xdWS3I2JthnBRr7JjGPuV6yIhWF5PjdmXTWkVynk'
access_token = '1309924410363703296-5o4y0i4kYKNwk9XoqRYERDt4vRWU0s'
access_token_secret = 'FucMOTNVF4aU02E5ppqzLUKDjn1ONgN3xgBOrxEUo6oWL'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Functions to clean tweets and assess tweets for sentiments
def clean_tweet(tweet):
    '''Utility function to clean tweet text by removing links, special characters
    using simple regex statements.'''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''Utility function to classify sentiment of passed tweet
    using textblob's sentiment method.'''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity >= 0.25:
        return 'positive'
    elif -0.25 < analysis.sentiment.polarity < 0.25:
        return 'neutral'
    else:
        return 'negative'


# Grab Tweets.
# Max of 200 per page. Max of 5 pages while include_rts=False (retweets)
# These API calls could be placed into a loop where page is an increasing variable (offset) until 16 is reached.
# Or, until <200 tweets are returned.
page_num = 1
NYCZeroWaste_tweets = []
NYCSanitation_tweets = []
DsnyColumbia_tweets = []
while page_num < 16:
    ZW_page = api.user_timeline('NYCzerowaste', count=200, page=page_num, include_rts=True)
    NYCZeroWaste_tweets.append(ZW_page)
    SAN_page = api.user_timeline('NYCSanitation', count=200, page=page_num, include_rts=True)
    NYCSanitation_tweets.append(SAN_page)
    DC_page = api.user_timeline('DsnyColumbia', count=200, page=page_num, include_rts=True)
    DsnyColumbia_tweets.append(DC_page)
    page_num += 1


# For each tweet object:
#   parse for desired info,
#   classify the sentiment of tweet's text,
#   and store the results to a dictionary.
#   Then, add the dictionary to a list
parsed_tweets = []
for page in NYCZeroWaste_tweets:
    for tweet in page:
        d = {}
        d['source'] = '@NYCZeroWaste'
        d['id'] = tweet.id
        d['created_at'] = tweet.created_at
        d['date'] = datetime.date(d['created_at'])
        d['text'] = tweet.text
        d['sentiment'] = get_tweet_sentiment(clean_tweet(tweet.text))
        parsed_tweets.append(d)

for page in NYCSanitation_tweets:
    for tweet in page:
        d = {}
        d['source'] = '@NYCSanitation'
        d['id'] = tweet.id
        d['created_at'] = tweet.created_at
        d['date'] = datetime.date(d['created_at'])
        d['text'] = tweet.text
        d['sentiment'] = get_tweet_sentiment(clean_tweet(tweet.text))
        parsed_tweets.append(d)

for page in DsnyColumbia_tweets:
    for tweet in page:
        d = {}
        d['source'] = '@DsnyColumbia'
        d['id'] = tweet.id
        d['created_at'] = tweet.created_at
        d['date'] = datetime.date(d['created_at'])
        d['text'] = tweet.text
        d['sentiment'] = get_tweet_sentiment(clean_tweet(tweet.text))
        parsed_tweets.append(d)
    

# Throw the list of tweet dictionaries into a dataframe
tweets_df = pd.DataFrame(parsed_tweets).set_index(keys=['date']).sort_index()

tweets_per_date = tweets_df.groupby(['date', 'source', 'sentiment']).count()


print(tweets_df)
print(tweets_per_date)


### Plot the number of tweets per date from all three twitter accounts. Includes responses to comments.
fig, ax = plt.subplots()
fig.autofmt_xdate(rotation=40)
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.tick_params(axis='both', which='major', labelsize=5)
plt.bar([tup[0] for tup in tweets_per_date.index], tweets_per_date['id'])

plt.show()

"""
ZW_tweets = []
for tweet in NYCZeroWaste_tweets:
    parsed_tweet = {}

    # saving text of tweet
    parsed_tweet['text'] = tweet.text
    # saving sentiment of tweet
    parsed_tweet['sentiment'] = get_tweet_sentiment(clean_tweet(tweet.text))

    # appending parsed tweet to ZW_tweets list
    if tweet.retweet_count > 0:
        # if tweet has retweets, ensure that it is appended only once
        if parsed_tweet not in ZW_tweets:
            ZW_tweets.append(parsed_tweet)
    else:
        ZW_tweets.append(parsed_tweet)

SAN_tweets = []
for tweet in NYCSanitation_tweets:
    parsed_tweet = {}

    # saving text of tweet
    parsed_tweet['text'] = tweet.text
    # saving sentiment of tweet
    parsed_tweet['sentiment'] = get_tweet_sentiment(clean_tweet(tweet.text))

    # appending parsed tweet to ZW_tweets list
    if tweet.retweet_count > 0:
        # if tweet has retweets, ensure that it is appended only once
        if parsed_tweet not in SAN_tweets:
            SAN_tweets.append(parsed_tweet)
    else:
        SAN_tweets.append(parsed_tweet)


ZW_ptweets = [tweet for tweet in ZW_tweets if tweet['sentiment'] == 'positive']
ZW_ntweets = [tweet for tweet in ZW_tweets if tweet['sentiment'] == 'negative']

SAN_ptweets = [tweet for tweet in SAN_tweets if tweet['sentiment'] == 'positive']
SAN_ntweets = [tweet for tweet in SAN_tweets if tweet['sentiment'] == 'negative']


print("@NYCZeroWaste")
print("_____________")
print(f"Positive tweets percentage: {(100 * (len(ZW_ptweets) / len(ZW_tweets)))}%")
print(f"Negative tweets percentage: {(100 * (len(ZW_ntweets) / len(ZW_tweets)))}%")
print(f"Neutral tweets percentage: {(100 * (len(ZW_tweets) - (len(ZW_ntweets) + len(ZW_ptweets))) / len(ZW_tweets))}%")

print()
print()

print("@NYCSanitation")
print("_____________")
print(f"Positive tweets percentage: {(100 * (len(SAN_ptweets) / len(SAN_tweets)))}%")
print(f"Negative tweets percentage: {(100 * (len(SAN_ntweets) / len(SAN_tweets)))}%")
print(f"Neutral tweets percentage: {(100 * (len(SAN_tweets) - (len(SAN_ntweets) + len(SAN_ptweets))) / len(SAN_tweets))}%")

"""
