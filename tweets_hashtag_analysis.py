import tweepy
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt



load_dotenv()

# Twitter API credentials
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Define function to perform sentiment analysis on a tweet
def get_tweet_sentiment(tweet):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(tweet)
    return scores["compound"]

# Define function to get tweets containing a given hashtag or list of hashtags
def get_tweets(hashtags):
    tweets = []
    for hashtag in hashtags:
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag, lang="en", tweet_mode="extended").items(200):
            tweets.append([tweet.created_at, tweet.full_text, get_tweet_sentiment(tweet.full_text)])
    return pd.DataFrame(tweets, columns=["created_at", "text", "sentiment"])

# Example usage
hashtags = ["#hatespeech", "#anger"]
df = get_tweets(hashtags)
print(df)

# Group tweets by sentiment score and count the number of tweets in each group
sentiment_counts = df.groupby("sentiment").size()

# Create a bar chart of the sentiment counts
plt.bar(sentiment_counts.index, sentiment_counts.values)
plt.xlabel("Sentiment Score")
plt.ylabel("Number of Tweets")
plt.title("Sentiment Analysis of Tweets Containing Hashtags: {}".format(", ".join(hashtags)))
plt.show()

def get_sentiment_category(score):
    if score > 0.05:
        return "positive"
    elif score < -0.05:
        return "negative"
    else:
        return "neutral"

# Apply the function to create a new column with the sentiment category
df["sentiment_category"] = df["sentiment"].apply(get_sentiment_category)
sentiment_counts = df.groupby("sentiment_category").size()
colors = ["red", "green", "blue"]
plt.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
plt.xlabel("Sentiment Category")
plt.ylabel("Number of Tweets")
plt.title("Sentiment Analysis of Tweets Containing Hashtags: {}".format(", ".join(hashtags)))
plt.legend(sentiment_counts.index, loc="best")
plt.show()

# Create a pie chart of the sentiment counts
plt.pie(sentiment_counts.values, labels=sentiment_counts.index, colors=colors)
plt.title("Sentiment Analysis of Tweets Containing Hashtags: {}".format(", ".join(hashtags)))
plt.legend(sentiment_counts.index, loc="best")
plt.show()