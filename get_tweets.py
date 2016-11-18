#! /usr/bin/env python

# Resources needed for getting tweets
import tweepy
import csv
import re

# Twitter authentication
consumer_key = "aznBK3jqgnI5ienvFYu1oIlZF"
consumer_secret = "bzpVZZ86SZ7LTI6KYGPmfgX378K1KCWFV45GRM8vhhO9HlDtt1"
access_key = "766386667359969280-VpCO3bD5igomslsqHr1EN6NGDahRYz9"
access_secret = "3aZqyJbHP7KtGOYUJGHl1Qkhg0emCLnLHtrvZxMe3YYgi"


def get_all_tweets(screen_name):
    all_tweets = []

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    client = tweepy.API(auth)
    new_tweets = client.user_timeline(screen_name=screen_name, count=200)  # maximum twitter allows at once

    while len(new_tweets) > 0:
        for tweet in new_tweets:
            #if tweet.source == 'Twitter for Android':
            all_tweets.append(tweet.text.encode("utf-8"))

        print("We've got %s tweets so far" % (len(all_tweets)))
        max_id = new_tweets[-1].id - 1
        new_tweets = client.user_timeline(screen_name=screen_name, count=200, max_id=max_id)

    return all_tweets


def clean_tweet(tweet):
    if type(tweet) is bytes:
        tweet = tweet.decode()
    tweet = re.sub(r"http\S+", "", tweet)  # links
    tweet = re.sub("#\S+", "", tweet)           # hashtags
    tweet = re.sub("\.?@", "", tweet)           # at mentions
    tweet = re.sub("RT.+", "", tweet)           # Retweets
    tweet = re.sub("Video\:", "", tweet)        # Videos
    tweet = re.sub("\n", "", tweet)             # new lines
    tweet = re.sub("^\.\s.", "", tweet)         # leading whitespace
    tweet = re.sub("\s+", " ", tweet)           # extra whitespace
    tweet = re.sub("&amp;", "and", tweet)       # encoded ampersands
    return tweet


def write_tweets_to_csv(tweets):
    with open('hillary_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        for tweet in tweets:
            tweet = clean_tweet(tweet)
            if tweet:
                writer.writerow([tweet])


if __name__ == "__main__":
    tweets = get_all_tweets("HillaryClinton")
    write_tweets_to_csv(tweets)
