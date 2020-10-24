import pytest
from src.get_tweets_tweepy import TwitterAPI


@pytest.fixture
def tapi():
    return TwitterAPI


@pytest.fixture
def hashtags_one():
    return [{"indices": [32, 38], "text": "nodejs"}]


@pytest.fixture
def hashtags_many():
    return [{"indices": [32, 38], "text": "nodejs"},
            {"indices": [12, 16], "text": "java"}]


@pytest.fixture
def hashtags_more():
    return [{"indices": [32, 38], "text": "nodejs"},
            {"indices": [12, 16], "text": "java"},
            {"indices": [30, 32], "text": "go"}]


def test_extract_hashtags_empty(tapi):
    assert tapi._extract_entity_hashtags([]) == ""


def test_extract_hashtags_one(tapi, hashtags_one):
    assert tapi._extract_entity_hashtags(hashtags_one) == "nodejs"


def test_extract_hashtags_many(tapi, hashtags_many):
    assert tapi._extract_entity_hashtags(hashtags_many) == "nodejs:java"


def test_extract_hashtags_more(tapi, hashtags_more):
    assert tapi._extract_entity_hashtags(hashtags_more) == "nodejs:java:go"
