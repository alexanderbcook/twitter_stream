import redis
import json
import datetime
import argparse
import logging
import csv
import io
from util import encode

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

try:
    redis = redis.StrictRedis(host='localhost', port=6379, db=0)
except:
    print "Can't connect to Redis!"

parser = argparse.ArgumentParser()
parser.add_argument("-q",
                    "--queries",
                    dest="query",
                    help="Give names of queries stored in Redis.",
                    default='-')
args = parser.parse_args()

with io.open('data/%s.json' % args.query, 'a', encoding='utf-8') as outfile:
    i = redis.llen(args.query)
    logging.debug("Writing %s tweets to data/%s.csv" % (i, args.query))
    while i > 0:
        data = json.loads(redis.lpop(args.query)) 
        outfile.write(unicode(json.dumps(data, ensure_ascii=False,indent=4,sort_keys=True)))

        i = i - 1