# twitter_stream
A twitter stream which easily allows the user to gather tweets relating to a specific event or hashtag. Supports functionality to write to a csv or upload directly to a Postgres database.

Two command line options.

-q specifies the query. 'cubs' will filter out all tweets other than tweets related to either bear cubs or the Chicago cubs. 'cubs, portland' will filter out all tweets other than the two given terms.

-m specifies the mode. 's' will run streaming mode, which writes batches of tweets to a JSON file using Redis. Default is 'o' which is a one off run instance.

Access Twitters' developer API here: https://dev.twitter.com/
You'll need application and developer keys.
