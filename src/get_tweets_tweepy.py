import pandas as pd
import tweepy as tp


class TwitterAPI:
    """
    Setup for Twitter API using tweepy
    :param STATUS_LIMIT: number of statuses that can be retrived in a batch
    :param _api: the api setup
    :param new_tweet_ids: array of tweet ids to get statuses for
    """

    STATUS_LIMIT = 100  # limit of statuses per tweepy request
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

    @staticmethod
    def _extract_entity_hashtags(hashtags):
        return ":".join([hashtags[n]['text'] for n in range(len(hashtags))])

    @staticmethod
    def _extract_entity_mentions(mentsions):
        pass

    @staticmethod
    def _extract_entity_urls(urls):
        pass

    @staticmethod
    def _extract_status_attributes(status):
        return {
            "created_at": status.created_at,
            "id": status.id,
            "id_str": status.id_str,
            "text": status.text,
            "hashtags": TwitterAPI._extract_entity_hashtags(status.entities['hashtags']),
            # "media_obj": str(status.entities['media']),
            # "urls": TwitterAPI._extract_entity_urls(status.entities.urls),
            # "user_mentions": TwitterAPI._extract_entity_mentions(status.entities.user_mentions),
            "source": status.source,
            "source_url": status.source_url,
            "in_reply_to_status_id": status.in_reply_to_status_id,
            "in_reply_to_status_id_str": status.in_reply_to_status_id_str,
            "in_reply_to_user_id": status.in_reply_to_user_id,
            "in_reply_to_user_id_str": status.in_reply_to_user_id_str,
            "in_reply_to_screen_name": status.in_reply_to_screen_name,
            "user": status.user,
            "geo": status.geo,
            "coordinates": status.coordinates,
            "place": status.place,
            "contributors": status.contributors,
            "is_quote_status": status.is_quote_status,
            "retweet_count": status.retweet_count,
            "favorite_count": status.favorite_count,
            "favorited": status.favorited,
            "retweeted": status.retweeted,
            "lang": status.lang
        }

    def set_api(self, api_key, api_secret, acc_token, acc_secret):
        auth = tp.OAuthHandler(api_key, api_secret)
        auth.set_access_token(acc_token, acc_secret)
        self._api = tp.API(auth, wait_on_rate_limit=True,
                           wait_on_rate_limit_notify=True)

    def get_statuses(self, new_tweet_ids):
        self.new_tweet_ids = new_tweet_ids
        chunked_ids = TwitterAPI._chunk(new_tweet_ids, TwitterAPI.STATUS_LIMIT)
        statuses = pd.DataFrame()
        for l in chunked_ids:
            new_statuses = self._api.statuses_lookup(l)
            for s in new_statuses:
                statuses = statuses.append(self._extract_status_attributes(s), ignore_index=True)
            break
        return statuses
