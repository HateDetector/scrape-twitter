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


@pytest.fixture
def url_one():
    return [{"indices": [32, 52],
             "url": "http://t.co/IOwBrTZR",
             "display_url": "youtube.com/watch?v=oHg5SJ…",
             "expanded_url": "http://www.youtube.com/watch?v=oHg5SJYRHA0"}]


@pytest.fixture
def url_many():
    return [{"indices": [32, 52],
             "url": "http://t.co/IOwBrTZR",
             "display_url": "youtube.com/watch?v=oHg5SJ…",
             "expanded_url": "http://www.youtube.com/watch?v=oHg5SJYRHA0"},
            {"indices": [43, 56],
             "url": "http://t.co/IOwBrNdsfsdf",
             "display_url": "facebook.com/somewebterte...",
             "expanded_url": "https://www.facebook.com/somewebtertesite"}]


@pytest.fixture
def mentions_one():
    return [{"name": "Twitter API", "indices": [4, 15],
             "screen_name": "twitterapi", "id": 6253282, "id_str": "6253282"}]


@pytest.fixture
def mentions_many():
    return [{"name": "Twitter API", "indices": [4, 15],
             "screen_name": "twitterapi", "id": 6253282, "id_str": "6253282"},
            {"name": "some one", "indices": [4, 15],
             "screen_name": "somename", "id": 1234567, "id_str": "1234567"}]


def test_extract_hashtags_empty(tapi):
    assert tapi._extract_entity_hashtags([]) == ""


def test_extract_hashtags_one(tapi, hashtags_one):
    assert tapi._extract_entity_hashtags(hashtags_one) == "nodejs"


def test_extract_hashtags_many(tapi, hashtags_many):
    assert tapi._extract_entity_hashtags(hashtags_many) == "nodejs|java"


def test_extract_hashtags_more(tapi, hashtags_more):
    assert tapi._extract_entity_hashtags(hashtags_more) == "nodejs|java|go"


def test_extract_url_empty(tapi):
    assert tapi._extract_entity_urls([]) == ""


def test_extract_url_one(tapi, url_one):
    assert tapi._extract_entity_urls(
        url_one) == "http://www.youtube.com/watch?v=oHg5SJYRHA0"


def test_extract_url_one_protocol_removed(tapi, url_one):
    assert tapi._extract_entity_urls(
        url_one, remove_protocol=True) == "youtube.com/watch?v=oHg5SJYRHA0"


def test_extract_url_many(tapi, url_many):
    assert tapi._extract_entity_urls(
        url_many) == "http://www.youtube.com/watch?v=oHg5SJYRHA0|https://www.facebook.com/somewebtertesite"


def test_extract_url_many_protocol_removed(tapi, url_many):
    assert tapi._extract_entity_urls(
        url_many, remove_protocol=True) == "youtube.com/watch?v=oHg5SJYRHA0|facebook.com/somewebtertesite"


def test_extract_mentions_empty(tapi):
    assert tapi._extract_entity_mentions([]) == ""


def test_extract_mentions_one(tapi, mentions_one):
    assert tapi._extract_entity_mentions(mentions_one) == "twitterapi"


def test_extract_mentions_one_as_id(tapi, mentions_one):
    assert tapi._extract_entity_mentions(mentions_one, as_id=True) == "6253282"


def test_extract_mentions_many(tapi, mentions_many):
    assert tapi._extract_entity_mentions(mentions_many) == "twitterapi|somename"


def test_extract_mentions_many_as_id(tapi, mentions_many):
    assert tapi._extract_entity_mentions(mentions_many, as_id=True) == "6253282|1234567"
