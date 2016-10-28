# twitter_stream
A twitter stream which easily allows the user to gather tweets relating to a specific event or hashtag. Supports functionality to write to a csv or upload directly to a Postgres database.

Three command line arguments are available.

-t specifies the type of data output. 'csv' will output a CSV file, 'db' will upload directly to a database.
-d specifies a data directory for the CSV file. If this option is not set, the CSV will be written in the same directory as downloader.py
-q specifies the query. 'cubs' will filter out all tweets other than tweets related to either bear cubs or the Chicago cubs. 'cubs, portland' will filter out all tweets other than the two given terms.

Access Twitters' developer API here: https://dev.twitter.com/
You'll need application and developer keys.

Specify the connection string and table name in config.py
