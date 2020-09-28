# RecyclingMessaging

This repo is a learning environment focused on sentiment analysis of recycling messaging text.

## Project 1: Sentiment analysis of tweets from @NYCzerowaste and  @NYCSanitation and @DsnyColumbia. Add more accounts?
1. Positive words vs. Negative words
    - Create Twitter app
    - Access tweets with Tweepy
        - possible improvement: write loop to pull up to 3200 tweets
    - Parse twees for desired points of analysis
    - Regex to clean tweets prior to sentiment analysis
    - Use textblob to classify tweets by sentiment
        - ~~possible improvement: Assess words for trash-related content, and remove it.~~
2. Sentiments by date.
    - script currently puts tweets into a dataframe and stores their sentiment in a new column.
3. Recycling rates by date.
4. Compare.
5. Add in Wikipedia data??
    - edits by date
    - article sentiments

### Notes on sentiment classification:
- 'en-sentiments.xml' is the source of word valences.
- Can try swapping out analyzer for NaiveBayes model.

#### Limitations:
- Simple analysis of positive and negative words does not necessarily translate to sentiment.



