import argparse
import tweepy

def encode(string):
    if string:
        string = string.encode('utf-8')
    return string

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

def connect_to_api(config):
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    return api