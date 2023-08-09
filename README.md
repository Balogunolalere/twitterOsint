Twitter Sentiment Analysis
==========================

This project performs sentiment analysis on tweets containing specified hashtags using the tweepy and textblob Python libraries.

Description
-----------

The project has the following features:

*   Authenticates with the Twitter API using API keys
*   Defines a function to get tweets containing given hashtags using tweepy
*   Defines a function to analyze the sentiment of tweets using TextBlob
*   Gets example tweets containing specified hashtags
*   Analyzes the sentiment of the tweets and adds a "sentiment" column
*   Groups the tweets by sentiment score and plots a bar chart
*   Defines a function to categorize sentiment as positive, negative or neutral
*   Adds a "sentiment\_category" column using the categorization function
*   Plots various charts of the sentiment categories
*   User profile information (name, description, location, followers, etc)
*   Tweet activity patterns (most active hours, locations, interactions)
*   Tweet content analysis (topics, hashtags, mentions)


Installation
------------

Clone the repository:

Copy code

`git clone hhttps://github.com/Balogunolalere/twitterOsint.git`

Install dependencies:

Copy code

`pip install -r requirements.txt`

Usage
-----

1.  Sign up for a Twitter developer account and get your API keys
2.  Add your API keys to the .env file
3.  Run the script: `python Profile_analysis.py` or `tweets_hashtag_analysis.py`
4.  Specify hashtags to analyze when calling `get_tweets()`
5.  Call the analyze_user() function, passing the Twitter username to analyze: `df = analyze_user("elonmusk")`

Contributing
------------

Pull requests are welcome. Please open an issue first to discuss what changes you would like to make.

Credits
-------

*   [tweepy](https://www.tweepy.org/) - API for accessing Twitter data
*   [textblob](https://textblob.readthedocs.io/en/dev/) - Library for processing textual data
*   [vaderSentiment](https://github.com/cjhutto/vaderSentiment) - Sentiment analysis tool
*   [Python Dotenv](https://github.com/theskumar/python-dotenv) - Loading environment variables from .env file

