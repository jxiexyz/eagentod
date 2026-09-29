import unittest
import os
import json
import tempfile
import sys
from unittest.mock import patch

sys.path.insert(0, '/home/ubuntu/.hermes/scripts')
import eagent_precheck

class TestEagentPrecheck(unittest.TestCase):
    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_file.close()
        self.patcher = patch('eagent_precheck.STATE_FILE', self.tmp_file.name)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.tmp_file.name):
            os.remove(self.tmp_file.name)

    def test_load_and_save_state(self):
        state = eagent_precheck.load_state()
        self.assertIn("processed_users", state)
        
        eagent_precheck.mark_done(tweet_id="12345", username="TestUser", domain="test.xyz", note="unit test")
        
        new_state = eagent_precheck.load_state()
        self.assertIn("12345", new_state["processed_tweet_ids"])
        self.assertIn("testuser", [u.lower() for u in new_state["processed_users"]])
        self.assertIn("test.xyz", [d.lower() for d in new_state["processed_domains"]])
        self.assertEqual(len(new_state["history"]), 1)

    def test_dedup_case_insensitivity(self):
        eagent_precheck.mark_done(username="Kaleido_Finance")
        eagent_precheck.mark_done(username="kaleido_finance")
        state = eagent_precheck.load_state()
        matching = [u for u in state["processed_users"] if u.lower() == "kaleido_finance"]
        self.assertEqual(len(matching), 1)

if __name__ == '__main__':
    unittest.main()
