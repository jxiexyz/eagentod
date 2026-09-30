import sys
import json
import urllib.error
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
import moni_client


def test_get_account_info_success():
    mock_payload = {
        "socialData": {
            "observedId": 24678,
            "username": "ethereum",
            "isProject": True,
            "smartFollowersCount": 2200,
            "usernameChangeCount": 0,
            "followersCount": 4500000,
        }
    }
    with patch("moni_client.req", return_value=mock_payload):
        info = moni_client.get_account_info("ethereum")
        assert info["username"] == "ethereum"
        assert info["smartFollowersCount"] == 2200
        assert info["usernameChangeCount"] == 0
        assert info["isProject"] is True


def test_get_account_info_unknown_handle():
    with patch("moni_client.req", return_value={}):
        info = moni_client.get_account_info("unknown_handle")
        assert info == {}


def test_get_smart_followers_success():
    mock_payload = {
        "items": [
            {"observedId": 1, "username": "sf_one", "smartFollowersCount": 100},
            {"observedId": 2, "username": "sf_two", "smartFollowersCount": 200},
        ],
        "totalCount": 2,
    }
    with patch("moni_client.req", return_value=mock_payload):
        res = moni_client.get_smart_followers(24678, limit=10, offset=0)
        assert len(res["items"]) == 2
        assert res["items"][0]["username"] == "sf_one"


def test_get_smart_followers_pagination():
    with patch("moni_client.req", return_value={"items": []}) as mock_req:
        moni_client.get_smart_followers(12345, limit=25, offset=50)
        mock_req.assert_called_once_with(
            "/observed/smart_followers/",
            params={
                "observedId": 12345,
                "observedType": "twitter_account",
                "limit": 25,
                "offset": 50,
            },
        )


def test_get_timeline_success():
    mock_payload = {
        "items": [
            {"id": 101, "type": "NEW_FOLLOWING_BY_SMART", "text": "New following by @kol"},
        ],
        "totalCount": 1,
    }
    with patch("moni_client.req", return_value=mock_payload):
        res = moni_client.get_timeline(24678, limit=5)
        assert len(res["items"]) == 1
        assert res["items"][0]["type"] == "NEW_FOLLOWING_BY_SMART"


def test_req_http_error():
    mock_http_error = urllib.error.HTTPError(
        url="https://api.moni.ai/api/v1/test",
        code=500,
        msg="Internal Server Error",
        hdrs={},
        fp=MagicMock(read=lambda: b'{"error":"crash"}'),
    )
    with patch("urllib.request.urlopen", side_effect=mock_http_error):
        res = moni_client.req("/test")
        assert res.get("error") == "HTTP 500"
        assert "crash" in res.get("detail", "")


def test_req_timeout():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("timed out")):
        res = moni_client.req("/test")
        assert "timed out" in res.get("error", "")


def test_handle_strip_at():
    with patch("moni_client.req", return_value={"socialData": {"username": "chiquast"}}) as mock_req:
        info = moni_client.get_account_info("@chiquast")
        mock_req.assert_called_once_with(
            "/observed/",
            params={"twitterUsername": "chiquast", "timeframe": "H24"},
        )
        assert info["username"] == "chiquast"


def test_handle_empty():
    assert moni_client.get_account_info("") == {}
    assert moni_client.get_account_info("   ") == {}


def test_live_get_account_info():
    """Live integration test against Moni API."""
    info = moni_client.get_account_info("ethereum")
    assert info.get("username") == "ethereum"
    assert info.get("smartFollowersCount", 0) > 1000
    assert info.get("isProject") is True
