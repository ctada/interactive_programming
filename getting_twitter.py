"""Modified from erichannel's getting_twitter repo at https://gist.github.com/erichannell/434689526acb85f52c36"""
from TwitterSearch import *
import csv

def get_tweets(query, max = 2000):
    # takes a search term (query) and a max number of tweets to find
    # gets content from twitter and writes it to a csv bearing the name of your query
    
    i = 0
    search = query

    with open(search+'.csv', 'wb') as outf:
        writer = csv.writer(outf)
        writer.writerow(['user','time','tweet','latitude','longitude'])
        try:
            tso = TwitterSearchOrder()
            tso.set_keywords([search])
            tso.set_language('en') # English tweets only

            ts = TwitterSearch(
                consumer_key='Kfrb1VZUZ4VnTeVSDDN35QHY0',
                consumer_secret='SL7uoE2TdOy8RH3RluHUiv44qNrU7kFUs6S47nQp37PommH5Bx',
                access_token='3070546828-38kCFOC3uXefqpRECYydBcXPDAzIlYEfsKceStu',
                access_token_secret='42KcNoPB6lrAQURlRo37OAmGAG4uUr8WwhWrZzKPLXERz'
            )

            for tweet in ts.search_tweets_iterable(tso):
                lat = None
                longi = None
                time = tweet['created_at'] # UTC time when Tweet was created.
                user = tweet['user']['screen_name']
                tweet_text = tweet['text'].strip().encode('ascii', 'ignore')
                tweet_text = ''.join(tweet_text.splitlines())
                print i,time,
                if tweet['geo'] != None and tweet['geo']['coordinates'][0] != 0.0: # avoiding bad values
                    lat = tweet['geo']['coordinates'][0]
                    longi = tweet['geo']['coordinates'][1]
                    print('@%s: %s' % (user, tweet_text)), lat, longi
                else:
                    print('@%s: %s' % (user, tweet_text))

                writer.writerow([user, time, tweet_text, lat, longi])
                i += 1
                if i > max:
                    return()

        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)

query = raw_input ("Search for: ")
max_tweets = 2000
get_tweets(query, max_tweets)