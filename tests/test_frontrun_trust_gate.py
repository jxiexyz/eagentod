import sys
import json
import time
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
import frontrun_trust_gate


def _mock_history(changes):
    return [{"oldTwitterUsername": n} for n in changes]


def _mock_sf(count):
    return [{"twitter": f"kol_{i}", "name": f"KOL {i}"} for i in range(count)]


def test_reject_rebrand():
    with patch("frontrun_client.get_username_history", return_value=_mock_history(["old_name"])), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(10)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("scammer")
        assert not r["trusted"]
        assert "rebrand" in r["reject_reason"]


def test_reject_low_sf():
    with patch("frontrun_client.get_username_history", return_value=[]), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(3)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("lowsf")
        assert not r["trusted"]
        assert "low_smart_followers" in r["reject_reason"]


def test_pass_clean_account():
    with patch("frontrun_client.get_username_history", return_value=[]), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(8)), \
         patch("frontrun_client.get_wallets", return_value=[{"chain": "SOL", "address": "abc123"}]):
        r = frontrun_trust_gate.validate_handle("goodproject")
        assert r["trusted"]
        assert r["reject_reason"] is None
        assert r["smart_follower_count"] == 8
        assert r["wallets"].get("SOL") == "abc123"


def test_pass_exactly_5_sf():
    with patch("frontrun_client.get_username_history", return_value=[]), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(5)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("borderline")
        assert r["trusted"]


def test_project_under_1k_fol_passes_with_3_sf():
    with patch("frontrun_client.get_username_history", return_value=[]), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(3)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("earlyproj", followers=500, is_project=True)
        assert r["trusted"]
        assert r["reject_reason"] is None


def test_project_under_1k_fol_fails_under_3_sf():
    with patch("frontrun_client.get_username_history", return_value=[]), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(2)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("earlyproj_scam", followers=500, is_project=True)
        assert not r["trusted"]
        assert "low_smart_followers:2/3" in r["reject_reason"]


def test_project_over_1k_fol_requires_5_sf():
    with patch("frontrun_client.get_username_history", return_value=[]), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(4)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("midproj", followers=2000, is_project=True)
        assert not r["trusted"]
        assert "low_smart_followers:4/5" in r["reject_reason"]


def test_project_rejects_any_rebrand():
    with patch("frontrun_client.get_username_history", return_value=_mock_history(["old_name"])), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(10)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("rebranded_proj", followers=500, is_project=True)
        assert not r["trusted"]
        assert "rebrand" in r["reject_reason"]


def test_ct_giveaway_requires_100_sf():
    with patch("frontrun_client.get_username_history", return_value=[]), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(99)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("ct_kol_small", is_ct_giveaway=True)
        assert not r["trusted"]
        assert "low_smart_followers:99/100" in r["reject_reason"]


def test_ct_giveaway_passes_with_100_sf_and_1_rename():
    with patch("frontrun_client.get_username_history", return_value=_mock_history(["old_handle_once"])), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(100)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("ct_kol_good", is_ct_giveaway=True)
        assert r["trusted"]
        assert r["reject_reason"] is None


def test_ct_giveaway_fails_with_more_than_1_rename():
    with patch("frontrun_client.get_username_history", return_value=_mock_history(["name1", "name2"])), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(150)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("ct_kol_serial_rebrander", is_ct_giveaway=True)
        assert not r["trusted"]
        assert "rebrand" in r["reject_reason"]


def test_fail_open_on_error():
    with patch("frontrun_client.get_username_history", side_effect=Exception("timeout")), \
         patch("frontrun_client.get_smart_followers", return_value=_mock_sf(10)), \
         patch("frontrun_client.get_wallets", return_value=[]):
        r = frontrun_trust_gate.validate_handle("errhandle")
        # History check failed but non-fatal — should proceed to SF check
        assert r["trusted"]


def test_cache_hit(tmp_path):
    cache_file = tmp_path / "cache.json"
    cached = {"testcache": {"ts": time.time(), "result": {
        "trusted": True, "reject_reason": None, "smart_follower_count": 15,
        "smart_followers": ["a", "b"], "username_changes": 0,
        "old_usernames": [], "wallets": {},
    }}}
    cache_file.write_text(json.dumps(cached))
    with patch("frontrun_trust_gate.CACHE_PATH", str(cache_file)):
        r = frontrun_trust_gate.validate_handle("testcache")
        assert r["cached"] is True
        assert r["trusted"] is True


def test_empty_handle():
    r = frontrun_trust_gate.validate_handle("")
    assert not r["trusted"]
    assert r["reject_reason"] == "empty_handle"


def test_live_validation():
    """Live integration: validate a known-good trending account."""
    from frontrun_client import get_trending_accounts
    trending = get_trending_accounts("24h")
    assert len(trending) > 0
    # Pick first that has >5 SF gain (likely trusted)
    for acc in trending[:3]:
        h = acc.get("handle", "")
        if not h:
            continue
        r = frontrun_trust_gate.validate_handle(h)
        # Should at least return a valid result structure
        assert "trusted" in r
        assert "smart_follower_count" in r
        assert isinstance(r["wallets"], dict)
        break
