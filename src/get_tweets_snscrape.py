import os
from datetime import datetime


def save_tweets_by_user_since(users, date, filepath, until=datetime.today().strftime('%Y-%m-%d')):
    for user in users:
        command = "snscrape twitter-search 'from:{0} since:{1} until:{2}' >{3}sns-{0}".format(
            user, date, until, filepath)
        os.system(command)


# tbc
# def save_tweets_by_term(terms):
#   for term in terms:
#     command = ("snscrape twitter-search 'from:{0} since:{1}' >{2}twitter-{0}".format(user, date, filepath))
#     os.system(command)
