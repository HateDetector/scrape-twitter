import glob
import os
from datetime import datetime
from pathlib import Path


def get_tweets_by_user_since(users, date, filepath, until=datetime.today().strftime('%Y-%m-%d')):
    Path(filepath).mkdir(parents=True, exist_ok=True)
    for user in users:
        command = "snscrape twitter-search 'from:{0} since:{1} until:{2}' >{3}sns-user-{0}.txt".format(
            user, date, until, filepath)
        os.system(command)


def get_tweets_by_term_since(terms, date, filepath, until=datetime.today().strftime('%Y-%m-%d')):
    Path(filepath).mkdir(parents=True, exist_ok=True)
    for term in terms:
        command = "snscrape twitter-search '{0} since:{1} until:{2}' >{3}sns-term-{0}.txt".format(
            term, date, until, filepath)
        os.system(command)


def merge_sns_files(filepath, id_only=True):
    read_files = glob.glob(filepath+"*.txt")
    ids = []
    with open(filepath + "sns-merged.txt", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                if not id_only:
                    outfile.write(infile.read())
                else:
                    for l in infile.read().splitlines():
                        tw_id = str(l).split("'")[1].split("/")[-1]
                        ids.append(tw_id)
                        outfile.write((tw_id + "\n").encode('utf-8'))
    return ids
