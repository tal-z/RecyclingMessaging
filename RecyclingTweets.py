import tweepy
import re
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob

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
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


# Grab Tweets.
# max of 200 per page. Max of 5 pages.
NYCZeroWaste_tweets = api.user_timeline('NYCzerowaste', count=200, page=2, include_rts=False)
NYCSanitation_tweets = api.user_timeline('NYCSanitation', count=200, page=2, include_rts=False)


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

