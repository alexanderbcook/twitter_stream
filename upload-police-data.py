import redis
import json
import datetime
import argparse
import logging
import csv
import io
import psycopg2
from psycopg2 import sql
from util import encode

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


try:
    conn = psycopg2.connect("dbname='postgres' host ='localhost'")
except:
    print "Can't connect to PSQL!"
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

tablename = args.query

cur = conn.cursor()
cur.execute(sql.SQL("CREATE TABLE IF NOT EXISTS twitter.{} (id BIGINT, createdate TIMESTAMP, body VARCHAR, username VARCHAR, url VARCHAR, location VARCHAR, address VARCHAR, incident_type VARCHAR)").format(sql.Identifier(tablename)))

i = redis.llen(tablename)

logging.debug("Writing %s tweets to database twitter.%s" % (i, tablename))

while i > 0:

    data = json.loads(redis.lpop(tablename)) 

    tweetBody = data['text']

    at = 'at'
    startBracket = '['

    atIndex  = tweetBody.find(at)
    startBracketIndex = tweetBody.find(startBracket)

    address = tweetBody[atIndex + 2:startBracketIndex].strip()
    incidentType = tweetBody[:atIndex - 1 ].strip()

    cur.execute(sql.SQL("INSERT INTO twitter.{} (id, createdate, body, username, url, location, address, incident_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier(tablename)),
                    (data['id'], data['created_at'], tweetBody, data['username'], data['url'], data['location'], address, incidentType))
    i = i - 1

conn.commit()

conn.close()

