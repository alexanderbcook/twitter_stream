#!/usr/bin/env python

#USAGE: python downloader.py -q portland -t db

import tweepy
import logging
import csv
import config
from httplib import IncompleteRead
from util import encode, connect_to_api, get_parser

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

parser = get_parser()
args = parser.parse_args()

logging.debug("Writing tweets to %s.csv" % args.query)

count = 0

class StreamListener(tweepy.StreamListener):
    
    def on_status(self, data):

        global count
        count += 1

        if count % 100 == 0:
            logging.debug('%s tweets gathered.' % str(count))

        csvFile = open('data/%s.csv' % args.query, 'a')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow([data.created_at, encode(data.text), encode(data.user.name), encode(data.user.location), encode(data.user.screen_name), encode(data.user.url)])


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



