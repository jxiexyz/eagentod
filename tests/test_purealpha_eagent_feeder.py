#!/usr/bin/env python3
"""
Unit test for purealpha_eagent_feeder.py.
Tests keyword matching, form URL detection, and timeline fetching.
"""

import sys
import os
import unittest

sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
import purealpha_eagent_feeder as pf


class TestPureAlphaEagentFeeder(unittest.TestCase):
    def test_match_actionable(self):
        text_hit = "Waitlist open for whitelist mint: https://t.co/xyz"
        matched = pf.match_actionable(text_hit)
        self.assertIn("waitlist", matched)
        self.assertIn("whitelist mint", matched)

        text_zec = "Drop address below for zec nft."
        matched_zec = pf.match_actionable(text_zec)
        self.assertIn("drop address", matched_zec)
        self.assertIn("zec nft", matched_zec)

        text_nft_wl = "Get GTD mint and WL mint spot for our upcoming freemint NFT!"
        matched_nft_wl = pf.match_actionable(text_nft_wl)
        self.assertIn("gtd mint", matched_nft_wl)
        self.assertIn("wl mint", matched_nft_wl)
        self.assertIn("freemint", matched_nft_wl)
        self.assertIn("freemint nft", matched_nft_wl)

        text_arc = "Join the Arc whitelist! Whitelist live for NFT."
        matched_arc = pf.match_actionable(text_arc)
        self.assertIn("arc whitelist", matched_arc)
        self.assertIn("whitelist", matched_arc)

        text_gtd = "🎁 SAGE × ARC TERMINAL GIVEAWAY: 10 GTD spots + FCFS allowlist for free mint!"
        matched_gtd = pf.match_actionable(text_gtd)
        self.assertIn("gtd", matched_gtd)
        self.assertIn("gtd spot", matched_gtd)
        self.assertIn("gtd spots", matched_gtd)
        self.assertIn("allowlist", matched_gtd)
        self.assertIn("free mint", matched_gtd)

        text_miss = "Just launched our main token on uniswap!"
        self.assertEqual(pf.match_actionable(text_miss), [])

    def test_has_form_url(self):
        self.assertTrue(pf.has_form_url("Please register at docs.google.com/forms/d/e/123/viewform"))
        self.assertTrue(pf.has_form_url("Check out tally.so/r/abc"))
        self.assertTrue(pf.has_form_url("Visit https://project.io/whitelist"))
        self.assertFalse(pf.has_form_url("https://dexscreener.com/token/123"))

    def test_fetch_recent_tweets_live(self):
        tweets = pf.fetch_recent_tweets("legsdotfun", user_id="2094468493223620608", count=3)
        self.assertIsInstance(tweets, list)

    def test_fetch_985_candidates_integration(self):
        cands = pf.fetch_985_candidates()
        self.assertIsInstance(cands, list)
        self.assertGreater(len(cands), 0)
        for k in ["handle", "name", "summary", "why", "fol", "kind", "signal", "source_feed", "smart_followers"]:
            self.assertIn(k, cands[0])


if __name__ == "__main__":
    unittest.main()
