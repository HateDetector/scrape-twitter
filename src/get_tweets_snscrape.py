import os
import glob
from datetime import datetime


def save_tweets_by_user_since(users, date, filepath, until=datetime.today().strftime('%Y-%m-%d')):
    for user in users:
        command = "snscrape twitter-search 'from:{0} since:{1} until:{2}' >{3}sns-{0}.txt".format(
            user, date, until, filepath)
        os.system(command)


def merge_sns_files(filepath):
    read_files = glob.glob(filepath+"*.txt")
    with open(filepath + "sns-merged.txt", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())


# tbc
# def save_tweets_by_term(terms):
#   for term in terms:
#     command = ("snscrape twitter-search 'from:{0} since:{1}' >{2}twitter-{0}".format(user, date, filepath))
#     os.system(command)
