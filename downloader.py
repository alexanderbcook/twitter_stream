#!/usr/bin/env python

#USAGE: python downloader.py -q portland -t db

import tweepy
import logging
import argparse
import csv
import config
from httplib import IncompleteRead
from util import encode

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query terms",
                        default='-')
    parser.add_argument("-t",
                        "--output",
                        dest="output",
                        help="Enter 'csv' to produce a csv file, or 'db' to upload to a database.",
                        default='csv')
    return parser

parser = get_parser()
args = parser.parse_args()

if args.output == 'db':
    logging.debug('Connected database and writing tweets to %s' % config.connection_string)

elif args.output == 'csv':
    logging.debug("Writing tweets to %s.csv" % args.query)


count = 0

class StreamListener(tweepy.StreamListener):
    
    def on_status(self, data):

        global count
        count += 1

        if count % 100 == 0:
            logging.debug('%s tweets gathered.' % str(count))

        if args.output == 'csv':
            csvFile = open('data/%s.csv' % args.query, 'a')
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow([data.created_at, encode(data.text), encode(data.user.name), encode(data.user.location), encode(data.user.screen_name), encode(data.user.url)])

            return True

        elif args.output == 'db':

            return True

    def on_error(self, status_code):
        if IncompleteRead:
            return True
        if status_code == 420:
            logging.debug('An error has occurred! This stream will now close.')
            return False
        if KeyboardInterrupt:
            stream.disconnect()

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
    logging.debug('Connected to Twitter stream, filtering on "%s".' % args.query)
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=[str(args.query)], languages=['en'])



