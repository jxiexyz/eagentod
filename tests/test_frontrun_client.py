import os
import sys
import json
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
import frontrun_client


def test_load_cookie_header(tmp_path):
    cookie_file = tmp_path / "cookies.json"
    cookie_file.write_text(json.dumps([
        {"name": "foo", "value": "bar"},
        {"name": "baz", "value": "qux"}
    ]))
    with patch("frontrun_client.COOKIE_PATH", str(cookie_file)):
        header = frontrun_client.load_cookie_header()
        assert "foo=bar" in header
        assert "baz=qux" in header


def test_req_mocked():
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"data": {"status": "ok"}}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = frontrun_client.req("/api/test")
        assert res.get("data", {}).get("status") == "ok"


def test_get_trending_accounts_mocked():
    sample = [{"handle": "alice", "smartFollowerGainCount": 10}]
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"data": {"accounts": sample}}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        accounts = frontrun_client.get_trending_accounts("24h")
        assert len(accounts) == 1
        assert accounts[0]["handle"] == "alice"


def test_get_twitter_info_mocked():
    sample = {"name": "Alice", "twitterUsername": "alice"}
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"data": sample}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        info = frontrun_client.get_twitter_info("@alice")
        assert info["twitterUsername"] == "alice"


def test_live_frontrun_client():
    # Live integration test against loadbalance.frontrun.pro using active session cookie
    trending = frontrun_client.get_trending_accounts("24h")
    assert isinstance(trending, list)
    assert len(trending) > 0
    assert "handle" in trending[0]

    info = frontrun_client.get_twitter_info("chiquast")
    assert info.get("twitterUsername") == "chiquast"

    wallets = frontrun_client.get_wallets("chiquast")
    assert isinstance(wallets, list)
    assert any(w.get("address", "").lower() == "0x444b38c15ccc46db22b9590497023d91e506b2ff" for w in wallets)

    history = frontrun_client.get_username_history("chiquast")
    assert isinstance(history, list)
    assert any(h.get("oldTwitterUsername") == "vulleybaret" for h in history)

    credit = frontrun_client.get_credit_status()
    assert "plan" in credit
