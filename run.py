import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
from src.get_tweets_snscrape import get_tweets_by_term_since, get_tweets_by_user_since, merge_sns_files
from src.get_tweets_tweepy import TwitterAPI


def main():

    # setup
    load_dotenv()
    date_since = os.getenv('DATE_SINCE')
    date_until = os.getenv('DATE_UNTIL')
    temp_data_path = "./temp-data/"

    # get past tweets with snscrape
    # Users included in terms
    # candidates = os.getenv('USERS').split(',')
    # get_tweets_by_user_since(candidates, date_since,
    #                          temp_data_path, until=date_until)

    # get tweets by terms
    terms = os.getenv('TERMS').split(',')
    get_tweets_by_term_since(terms, date_since,
                             temp_data_path, until=date_until)
    new_ids = merge_sns_files(temp_data_path)

    # need to remove duplicates first to save on tweepy limit
    new_ids = list(dict.fromkeys(new_ids))

    # tweepy to get details from snscrape tweet ids
    TP = TwitterAPI(api_key=os.getenv('CONS_API_KEY'),
                    api_secret=os.getenv('CONS_API_SEC'),
                    acc_token=os.getenv('ACCESS_TOKEN'),
                    acc_secret=os.getenv('ACCESS_SECRET'))
    statuses_df = TP.get_statuses(new_ids, is_extended=True, add_to_csv=True,
                                  filepath=temp_data_path + "tp-statuses-" + date_since)

    print(statuses_df)
    
    # temporary store in csv
    # statuses_df.to_csv(temp_data_path + "tp_statuses-" + date_since + ".csv",
    #                    index=False, header=True)

    # store in postgres
    # does the table exist, create if not, use dataframe column names
    # loop INSERT and catch duplicate primary keys (id_str)

    # reset env
    # new_date_since = (datetime.today() - timedelta(days=1)
    #                   ).strftime('%Y-%m-%d')
    # new_date_until = datetime.today().strftime('%Y-%m-%d')
    # set_key('.env', 'DATE_SINCE', new_date_since)
    # set_key('.env', 'DATE_UNTIL', new_date_until)


if __name__ == "__main__":
    main()
