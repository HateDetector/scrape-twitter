import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
from pathlib import Path
from src.get_tweets_snscrape import save_tweets_by_user_since

if __name__ == "__main__":
    # args for search by users
    # args for search by term
    # args for limit
    # long term - output/ db connection

    # scrape
    # store in csv/ postgres

    # get past tweets then get last days tweets
    candidates = ['realDonaldTrump', 'Mike_Pence',
                  'JoeBiden', 'KamalaHarris']
    load_dotenv()
    date_since = os.getenv('DATE_SINCE')
    save_tweets_by_user_since(candidates, date_since, "./temp-data/")
    new_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    set_key('.env', 'DATE_SINCE', new_date)

    # use tweepy to get all the tweet info into a df then into postgres


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
