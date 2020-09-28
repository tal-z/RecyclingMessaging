# RecyclingMessaging

This repo is a learning environment focused on sentiment analysis of recycling messaging text.

## Project 1: Sentiment analysis of tweets from @NYCzerowaste and  @NYCSanitation and @DsnyColumbia. 
1. Add more accounts?
2. Positive words vs. Negative words
    - [x] Create Twitter app  
    - [x] Access tweets with Tweepy
        - [ ] possible improvement: write loop to pull up to 3200 tweets
    - [x] Parse tweets for desired points of analysis and store to dataframe.
    - [x] Regex to clean tweets prior to sentiment analysis
    - [x] Use textblob to classify tweets by sentiment
    - [x] Assess and adjust sentiment cutoffs 
        - [x] ~~possible improvement: Assess valence words for trash-related content, and remove it.~~
    - [x] Print results
3. Sentiments by date.
    - [x] Assess #tweets/day
    - [x] Graph # tweets by day (bar chart)
    - [ ] Graph sentiments by day
        - bar chart/line chart (1 = negative, 2 = neutral, 3 = positive)
        - In addition to polarity, utilize sentiment subjectivity and intensity to generate overall sentiment score
    - script currently puts tweets into a dataframe and stores their date and sentiment in new columns.
4. Overall sentiment of tweets related to 'Recycling'. 
5. Recycling rates by date.
6. Compare.
7. Add in Wikipedia data??
    - edits by date
    - article sentiments

### Notes on sentiment classification:
- 'en-sentiments.xml' is the source of word valences.
- Can try swapping out analyzer for NaiveBayes model.

#### Limitations:
- Simple analysis of positive and negative words does not necessarily translate to sentiment.



