#!/usr/bin/env python

#USAGE: python listener.py -q portland -m d

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
                    help="Specify the Twitter query terms.",
                    default='-')
parser.add_argument("-f",
                    "--follow",
                    dest="follow",
                    help="Specify user names to follow")

parser.add_argument("-m",
                    "--mode",
                    dest="mode",
                    help="Specify the mode. 'f' will configure for writing to a file, 'd' will configure for writing to a database.")
args = parser.parse_args()

default = ['1606472113', '1602852614']

count = 0

class StreamListener(tweepy.StreamListener):
    
    def on_status(self, data):
        global count
        count += 1

        if count % 100 == 0:
            logging.debug('%s tweets gathered.' % str(count))

        tweetID = data.id_str

        tweet = {}
        tweet['id'] = encode(data.id_str)
        tweet['created_at'] = dumps(data.created_at, default=json_serial)
        tweet['text'] = encode(data.text)
        tweet['username'] = encode(data.user.screen_name)
        tweet['url'] = encode(data.user.url)
        tweet['location'] = encode(data.user.location)
        json_tweet = json.dumps(tweet)
        
        redis.lpush(args.query, json_tweet)
        i = redis.llen(args.query)

        if args.follow == 'default':
            if i == 1:
                os.system('python upload-police-data.py -q %s' % args.query)
        if args.mode == 'f':
            if i % 50 == 0:
                os.system('python writer.py -q %s' % args.query)
        if args.mode == 'd':
            if i % 50 == 0:
                os.system('python upload.py -q %s' % args.query)
                

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
    if len(args.query) > 1:
        stream.filter(track=[str(args.query)], languages=['en'], async=True)
    elif args.follow == 'default':
        args.query = 'default'
        stream.filter(follow=default, languages=['en'], async=True)
    elif len(args.follow) > 1:
        args.query = args.follow
        stream.filter(follow=[str(args.follow)], languages=['en'], async=True)




