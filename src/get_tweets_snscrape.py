import os
import glob
from pathlib import Path
from datetime import datetime


def get_tweets_by_user_since(users, date, filepath, until=datetime.today().strftime('%Y-%m-%d')):
    Path(filepath).mkdir(parents=True, exist_ok=True)
    for user in users:
        command = "snscrape twitter-search 'from:{0} since:{1} until:{2}' >{3}sns-{0}.txt".format(
            user, date, until, filepath)
        os.system(command)


def merge_sns_files(filepath, id_only=True):
    read_files = glob.glob(filepath+"*.txt")
    with open(filepath + "sns-merged.txt", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                if not id_only:
                    outfile.write(infile.read())
                else:
                    for l in infile.read().splitlines():
                        print(str(l).split("'")[1].split("/")[-1])
                        outfile.write((str(l).split("'")[1].split(
                            "/")[-1] + "\n").encode('utf-8'))


# tbc
# def save_tweets_by_term(terms):
#   for term in terms:
#     command = ("snscrape twitter-search 'from:{0} since:{1}' >{2}twitter-{0}".format(user, date, filepath))
#     os.system(command)
