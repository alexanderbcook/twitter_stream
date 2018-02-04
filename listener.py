#!/usr/bin/env python

#USAGE: python downloader.py -q portland -m s

import tweepy
import logging
import csv
import config
import redis
import json
import os
import argparse
from json import dumps
from httplib import IncompleteRead
from util import encode, connect_to_api, json_serial

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("-q",
                    "--query",
                    dest="query",
                    help="Specify the Twitter filter terms.",
                    default='-')
parser.add_argument("-m",
                    "--mode",
                    dest="mode",
                    help="Specify the mode. 's' will configure for straeaming, 'o' will run a one off instance.")
args = parser.parse_args()

logging.debug("Writing tweets to %s.csv" % args.query)

count = 0

class StreamListener(tweepy.StreamListener):
    
    def on_status(self, data):
        global count
        count += 1

        if count % 100 == 0:
            logging.debug('%s tweets gathered.' % str(count))

        tweetID = data.id_str

        tweet = {}
        tweet['created_at'] = dumps(data.created_at, default=json_serial)
        tweet['text'] = encode(data.text)
        tweet['username'] = encode(data.user.screen_name)
        tweet['url'] = encode(data.user.url)
        tweet['location'] = encode(data.user.location)
        json_tweet = json.dumps(tweet)
        
        redis.lpush(args.query, json_tweet)
        
        if args.mode == 's':
            i = redis.llen(args.query)
            if i % 500 == 0:
                os.system('python writer.py -q %s' % args.query)
                

    def on_error(self, status_code):
        if IncompleteRead:
            return True
        if status_code == 420:
            logging.debug('Tweets are being rate-limited..')
            return False
        if KeyboardInterrupt:
            logging.debug('Stream disconnected..')
            stream.disconnect()

if __name__ == '__main__':
    api = connect_to_api(config)
    logging.debug('Connected to Twitter stream, filtering on "%s".' % args.query)
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=[str(args.query)], languages=['en'])



