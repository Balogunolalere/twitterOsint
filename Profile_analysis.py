import re
import tweepy
import pandas as pd
from gensim import corpora, models
from collections import Counter
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

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
api = tweepy.API(auth, wait_on_rate_limit=True)




def analyze_user(username):
    # Get user profile details
    
    # Get user tweets
    tweets = api.user_timeline(screen_name=username, count=200, tweet_mode='extended')

    # Find the hour of day for each tweet
    hours = [tweet.created_at.hour for tweet in tweets]

    # Count the frequency of each hour
    hour_counts = Counter(hours)

    # Print the most active hour of the day
    most_active_hour = hour_counts.most_common(1)[0][0]

    user = api.get_user(screen_name=username)
    print(f"Name: {user.name}")
    print(f"User Description: {user.description}")
    print(f"Location: {user.location}")
    print(f"Following: {user.friends_count}")
    print(f"Followers: {user.followers_count}")
    print(f"Total tweets: {user.statuses_count}")
    print(f"Account created at: {user.created_at}")
    print(f"Most active hour of the day: {most_active_hour}:00 - {most_active_hour+1}:00")

    # Find the most common location for the user's tweets
    locations = [tweet.place.full_name for tweet in tweets if tweet.place is not None]
    if locations:
        most_common_location = Counter(locations).most_common(1)[0][0]
        print(f"Most common location for tweets: {most_common_location}")
    else:
        print("No location data found in the latest tweets.")

    # Find most retweeted/replied to users
    interactions = []
    tweet_count = 0
    retweet_count = 0
    for tweet in tweets:
        if hasattr(tweet, 'retweeted_status'):
            interactions.append(tweet.retweeted_status.user.screen_name)
            retweet_count += 1
        elif tweet.in_reply_to_screen_name:
            interactions.append(tweet.in_reply_to_screen_name)
        tweet_count += 1

    most_common_interactions = Counter(interactions).most_common(1)
    if most_common_interactions:
        print(f"Most interacted user: {most_common_interactions[0][0]} with {most_common_interactions[0][1]} interactions")
    else:
        print("No interactions found in the latest tweets.")

    # Convert datetime objects to UTC timezone
    utc = pytz.UTC
    tweetx = [(tweet.created_at.replace(tzinfo=utc), tweet.full_text) for tweet in tweets]

    # Calculate average tweets and retweets per day
    days = (datetime.now(tz=utc) - tweetx[-1][0]).days
    print(f"Average tweets per day: {tweet_count/days}")
    print(f"Average retweets per day: {retweet_count/days}")

    # Use Gensim to identify main topics in tweets
    texts = [tweet.full_text for tweet in tweets]
    texts = [text.lower().split() for text in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    topics = lda.print_topics(num_words=5)
    print("Main topics in tweets:")
    for topic in topics:
        print(topic)

    # Extract hashtags and mentions from tweets
    hashtags = []
    mentions = []
    for tweet in tweets:
        hashtags += re.findall(r"#(\w+)", tweet.full_text)
        mentions += re.findall(r"@(\w+)", tweet.full_text)

    # Count frequency of hashtags and mentions
    hashtag_counts = Counter(hashtags).most_common(5)
    mention_counts = Counter(mentions).most_common(5)

    # Print most frequent hashtags and mentions
    print("Most frequent hashtags:")
    for hashtag in hashtag_counts:
        print(f"#{hashtag[0]}: {hashtag[1]}")
    print("Most frequent mentions:")
    for mention in mention_counts:
        print(f"@{mention[0]}: {mention[1]}")

    data = [[tweet.created_at, tweet.full_text, tweet.in_reply_to_screen_name] for tweet in tweets]
    df = pd.DataFrame(data, columns=['Date', 'Text', 'ReplyTo'])
    return df

# Replace 'username' with the Twitter handle you want to analyze
df = analyze_user('elonmusk')
df