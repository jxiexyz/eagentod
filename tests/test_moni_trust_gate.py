import sys
import json
import time
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
import moni_trust_gate


def _mock_info(sf_count=10, changes=0, followers=5000, old_names=None, observed_id=123):
    old_names = old_names or []
    return {
        "observedId": observed_id,
        "username": "testhandle",
        "smartFollowersCount": sf_count,
        "usernameChangeCount": changes,
        "followersCount": followers,
        "usernameChanges": [{"oldUsername": n} for n in old_names],
    }


def test_reject_rebrand():
    info = _mock_info(sf_count=10, changes=1, old_names=["old_name"])
    with patch("moni_client.get_account_info", return_value=info):
        r = moni_trust_gate.validate_handle("scammer")
        assert not r["trusted"]
        assert "rebrand" in r["reject_reason"]


def test_reject_low_sf():
    info = _mock_info(sf_count=3, changes=0, followers=2000)
    with patch("moni_client.get_account_info", return_value=info):
        r = moni_trust_gate.validate_handle("lowsf")
        assert not r["trusted"]
        assert "low_smart_followers:3/5" in r["reject_reason"]


def test_pass_clean_account():
    info = _mock_info(sf_count=8, changes=0, followers=5000)
    sf_items = {"items": [{"username": "kol1"}, {"username": "kol2"}]}
    with patch("moni_client.get_account_info", return_value=info), \
         patch("moni_client.get_smart_followers", return_value=sf_items):
        r = moni_trust_gate.validate_handle("goodproject")
        assert r["trusted"]
        assert r["reject_reason"] is None
        assert r["smart_follower_count"] == 8
        assert r["smart_followers"] == ["kol1", "kol2"]


def test_pass_exactly_5_sf():
    info = _mock_info(sf_count=5, changes=0, followers=5000)
    with patch("moni_client.get_account_info", return_value=info), \
         patch("moni_client.get_smart_followers", return_value={"items": []}):
        r = moni_trust_gate.validate_handle("borderline")
        assert r["trusted"]


def test_project_under_1k_passes_3sf():
    info = _mock_info(sf_count=3, changes=0, followers=500)
    with patch("moni_client.get_account_info", return_value=info), \
         patch("moni_client.get_smart_followers", return_value={"items": []}):
        r = moni_trust_gate.validate_handle("earlyproj", followers=500, is_project=True)
        assert r["trusted"]
        assert r["reject_reason"] is None


def test_project_under_1k_fails_2sf():
    info = _mock_info(sf_count=2, changes=0, followers=500)
    with patch("moni_client.get_account_info", return_value=info):
        r = moni_trust_gate.validate_handle("earlyproj_scam", followers=500, is_project=True)
        assert not r["trusted"]
        assert "low_smart_followers:2/3" in r["reject_reason"]


def test_project_over_1k_requires_5sf():
    info = _mock_info(sf_count=4, changes=0, followers=2000)
    with patch("moni_client.get_account_info", return_value=info):
        r = moni_trust_gate.validate_handle("midproj", followers=2000, is_project=True)
        assert not r["trusted"]
        assert "low_smart_followers:4/5" in r["reject_reason"]


def test_project_rejects_any_rebrand():
    info = _mock_info(sf_count=10, changes=1, followers=500, old_names=["old_proj"])
    with patch("moni_client.get_account_info", return_value=info):
        r = moni_trust_gate.validate_handle("rebranded_proj", followers=500, is_project=True)
        assert not r["trusted"]
        assert "rebrand" in r["reject_reason"]


def test_ct_giveaway_requires_100sf():
    info = _mock_info(sf_count=99, changes=0, followers=10000)
    with patch("moni_client.get_account_info", return_value=info):
        r = moni_trust_gate.validate_handle("ct_kol_small", is_ct_giveaway=True)
        assert not r["trusted"]
        assert "low_smart_followers:99/100" in r["reject_reason"]


def test_ct_giveaway_passes_100sf_1rename():
    info = _mock_info(sf_count=100, changes=1, followers=10000, old_names=["old_name_once"])
    with patch("moni_client.get_account_info", return_value=info), \
         patch("moni_client.get_smart_followers", return_value={"items": []}):
        r = moni_trust_gate.validate_handle("ct_kol_good", is_ct_giveaway=True)
        assert r["trusted"]
        assert r["reject_reason"] is None


def test_ct_giveaway_fails_2rename():
    info = _mock_info(sf_count=150, changes=2, followers=10000, old_names=["n1", "n2"])
    with patch("moni_client.get_account_info", return_value=info):
        r = moni_trust_gate.validate_handle("ct_kol_serial_rebrander", is_ct_giveaway=True)
        assert not r["trusted"]
        assert "rebrand" in r["reject_reason"]


def test_fail_open_on_error():
    with patch("moni_client.get_account_info", side_effect=Exception("moni_down")):
        r = moni_trust_gate.validate_handle("errhandle")
        assert r["trusted"]
        assert "moni_error" in r["reject_reason"]


def test_cache_hit(tmp_path):
    cache_file = tmp_path / "cache.json"
    cached = {"testcache": {"ts": time.time(), "result": {
        "trusted": True, "reject_reason": None, "smart_follower_count": 15,
        "smart_followers": ["a", "b"], "username_changes": 0,
        "old_usernames": [], "wallets": {}, "followers": 2000,
    }}}
    cache_file.write_text(json.dumps(cached))
    with patch("moni_trust_gate.CACHE_PATH", str(cache_file)):
        r = moni_trust_gate.validate_handle("testcache")
        assert r["cached"] is True
        assert r["trusted"] is True


def test_empty_handle():
    r = moni_trust_gate.validate_handle("")
    assert not r["trusted"]
    assert r["reject_reason"] == "empty_handle"


def test_auto_followers_from_moni():
    info = _mock_info(sf_count=3, changes=0, followers=800)
    with patch("moni_client.get_account_info", return_value=info), \
         patch("moni_client.get_smart_followers", return_value={"items": []}):
        # followers param omitted -> uses 800 from Moni -> project < 1k tier (min 3 SF) passes!
        r = moni_trust_gate.validate_handle("early_autodetect", is_project=True)
        assert r["trusted"]
        assert r["reject_reason"] is None


def test_live_validation():
    """Live integration: validate @ethereum via Moni API."""
    r = moni_trust_gate.validate_handle("ethereum")
    assert r["trusted"] is True
    assert r["smart_follower_count"] > 100
    assert r["reject_reason"] is None
