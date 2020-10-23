import pandas as pd
import tweepy as tp

# limit for tweepy is 100 statuses per request


class TwitterAPI:
    """
    Setup for Twitter API using tweepy
    :param STATUS_LIMIT: number of statuses that can be retrived in a batch
    :param _api: the api setup
    :param new_tweet_ids: array of tweet ids to get statuses for
    """

    STATUS_LIMIT = 100
    _api = None
    all_tweet_ids = {}
    waiting = False  # maybe useful depends on tweepy settings
    replies = []  # not sure I needs

    def __init__(self, api_key, api_secret, acc_token, acc_secret):
        self.set_api(api_key, api_secret, acc_token, acc_secret)

    @staticmethod
    def _chunk(lst, n):
        n = max(1, n)
        return [lst[i:i+n] for i in range(0, len(lst), n)]

    def set_api(self, api_key, api_secret, acc_token, acc_secret):
        auth = tp.OAuthHandler(api_key, api_secret)
        auth.set_access_token(acc_token, acc_secret)
        self._api = tp.API(auth, wait_on_rate_limit=True,
                           wait_on_rate_limit_notify=True)

    def get_statuses(self, new_tweet_ids):
        self.new_tweet_ids = new_tweet_ids
        print(new_tweet_ids)
        chunked_ids = self._chunk(new_tweet_ids, self.STATUS_LIMIT)
        for l in chunked_ids:
            print(len(l))
        statuses = pd.DataFrame()
        return statuses
