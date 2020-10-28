import pandas as pd
import re
import tweepy as tp


class TwitterAPI:
    """
    Setup for Twitter API using tweepy
    :param STATUS_LIMIT: number of statuses that can be retrived in a batch
    :param _api: the api setup
    """

    STATUS_LIMIT = 100  # limit of statuses per tweepy request
    _api = None

    def __init__(self, api_key, api_secret, acc_token, acc_secret):
        self.set_api(api_key, api_secret, acc_token, acc_secret)

    @staticmethod
    def _remove_url_protocol(url):
        return re.sub(re.compile(r'^(?:https?://)?(?:www.)?'), "", url)

    @staticmethod
    def _chunk(lst, n):
        n = max(1, n)
        return [lst[i:i+n] for i in range(0, len(lst), n)]

    @staticmethod
    def _extract_entity_hashtags(hashtags):
        return "|".join([hashtags[n]['text'] for n in range(len(hashtags))])

    @staticmethod
    def _extract_entity_mentions(mentions, as_id=False):
        attribute = 'id_str' if as_id else 'screen_name'
        return "|".join([mentions[n][attribute] for n in range(len(mentions))])

    @staticmethod
    def _extract_entity_urls(urls, remove_protocol=False, unwound=False):
        # if unwound:
        #     return TwitterAPI._extract_entity_urls_unwound(urls, remove_protocol)
        if remove_protocol:
            return "|".join([TwitterAPI._remove_url_protocol(urls[n]['expanded_url']) for n in range(len(urls))])
        else:
            return "|".join([urls[n]['expanded_url'] for n in range(len(urls))])

    # extended entities exist, but unsure how to access via tweepy
    # @staticmethod
    # def _extract_entity_urls_unwound(urls, remove_protocol):
    #     if remove_protocol:
    #         return "|".join([TwitterAPI._remove_url_protocol(urls[n]['unwound']['url']) for n in range(len(urls))])
    #     else:
    #         return "|".join([urls[n]['unwound']['url'] for n in range(len(urls))])

    @ staticmethod
    def _extract_entity_media_urls(media, remove_protocol=False):
        if remove_protocol:
            return "|".join([TwitterAPI._remove_url_protocol(media[n]['media_url']) for n in range(len(media))])
        else:
            return "|".join([media[n]['media_url'] for n in range(len(media))])

    @ staticmethod
    def _extract_status_attributes(status, extended=False):
        text = status.full_text if extended else status.text
        hashtags = TwitterAPI._extract_entity_hashtags(
            status.entities['hashtags'])
        media_urls = (TwitterAPI._extract_entity_media_urls(
            status.entities['media'], remove_protocol=True)
            if 'media' in status.entities else "")
        urls = (TwitterAPI._extract_entity_urls(
            status.entities['urls'], remove_protocol=True, unwound=True)
            if extended else TwitterAPI._extract_entity_urls(
            status.entities['urls'], remove_protocol=True))
        user_mention = TwitterAPI._extract_entity_mentions(
            status.entities['user_mentions'])
        user_mention_id = str(TwitterAPI._extract_entity_mentions(
            status.entities['user_mentions'], as_id=True))
        return {
            # "id": status.id,  # just use id_str
            "id_str": str(status.id_str),
            "created_at": status.created_at,
            "text": text,
            "hashtags": hashtags,
            "media_urls": media_urls,
            "urls": urls,
            "user_mentions_screen_name": user_mention,
            "user_mentions_id_str": user_mention_id,
            "source": status.source,
            "source_url": status.source_url,
            # "in_reply_to_status_id": status.in_reply_to_status_id,  # just use id_str
            # "in_reply_to_user_id": status.in_reply_to_user_id,  # just use id_str
            "in_reply_to_status_id_str": str(status.in_reply_to_status_id_str),
            "in_reply_to_user_id_str": str(status.in_reply_to_user_id_str),
            "in_reply_to_screen_name": status.in_reply_to_screen_name,
            "user_id_str": str(status.user.id_str),
            "user_screen_name": status.user.screen_name,
            "user_name": status.user.name,
            "user_location": status.user.location,
            "user_created_at": status.user.created_at,
            "geo": status.geo,
            "coordinates": status.coordinates,
            "place": status.place,
            "contributors": status.contributors,
            "is_quote_status": status.is_quote_status,
            "retweet_count": status.retweet_count,
            "favorite_count": status.favorite_count,
            # "favorited": status.favorited,  # outdated metric
            # "retweeted": status.retweeted,  # outdated metric
            "lang": status.lang
        }

    def set_api(self, api_key, api_secret, acc_token, acc_secret):
        auth = tp.OAuthHandler(api_key, api_secret)
        auth.set_access_token(acc_token, acc_secret)
        self._api = tp.API(auth, wait_on_rate_limit=True,
                           wait_on_rate_limit_notify=True)

    def get_statuses(self, new_tweet_ids, is_extended=False, add_to_csv=True, filepath="./tp_statuses"):
        chunked_ids = TwitterAPI._chunk(new_tweet_ids, TwitterAPI.STATUS_LIMIT)
        ext = "extended" if is_extended else ""
        statuses = pd.DataFrame()
        first_run = True
        
        for l in chunked_ids:
            new_sta = self._api.statuses_lookup(l, tweet_mode=ext)
            raw_sta = self._extract_status_attributes(
                new_sta[0], extended=is_extended)
            chunked_statuses = pd.DataFrame(
                raw_sta, columns=raw_sta.keys(), index=[0])

            for x in range(1, len(new_sta)):
                chunked_statuses = chunked_statuses.append(self._extract_status_attributes(
                    new_sta[x], extended=is_extended), ignore_index=True)

            if add_to_csv:
                chunked_statuses.to_csv(filepath + ".csv",
                                        index=False, header=first_run, mode='a')

            if first_run: False

            statuses.append(chunked_statuses, ignore_index=True)
        return statuses

    def get_replies(self, users_and_tweets, date_since, date_until):
        users = users_and_tweets['user_screen_name'].unique()
        for user in users:
            user_tweets = users_and_tweets[users_and_tweets['user_screen_name'] == user]
            user_tweet_set = set(user_tweets['id_str'].unique())
            replies = []
            for tweet in tp.Cursor(self._api.search, q='to:'+user, since=date_since, until=date_until, timeout=999999).items():
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                    if tweet.in_reply_to_status_id_str in user_tweet_set:
                        replies.append(tweet)
        return replies
