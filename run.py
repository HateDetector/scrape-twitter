import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
from src.get_tweets_snscrape import get_tweets_by_user_since, merge_sns_files


def main():

    # setup
    load_dotenv()
    candidates = os.getenv('USERS').split(',')
    date_since = os.getenv('DATE_SINCE')
    date_until = os.getenv('DATE_UNTIL')
    filepath = "./temp-data/"

    # get past tweets with snscrape
    get_tweets_by_user_since(candidates, date_since,
                             filepath, until=date_until)
    merge_sns_files(filepath)

    # tweepy to get details


    # store in postgres


    # get replies (ongoing)


    # reset env
    # new_date_since = (datetime.today() - timedelta(days=1)
    #                   ).strftime('%Y-%m-%d')
    # new_date_until = datetime.today().strftime('%Y-%m-%d')
    # set_key('.env', 'DATE_SINCE', new_date_since)
    # set_key('.env', 'DATE_UNTIL', new_date_until)


"""
# update these for whatever tweet you want to process replies to
name = 'JoeBiden'
tweet_id = '1270923526690664448' # don't need, i'll check all of them
q = "to:"+name+ " since:2017-04-02 until:2017-04-03"
replies=[]
for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=999999).items(1000):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
        if (tweet.in_reply_to_status_id_str==tweet_id):
            replies.append(tweet)
"""


if __name__ == "__main__":
    main()
