#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, '/home/ubuntu/.hermes/scripts')
import post_eagent_report

class TestPostEagentReport(unittest.TestCase):
    @patch('post_eagent_report.requests.post')
    def test_post_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"ok": True, "result": {"message_id": 9999}}
        mock_post.return_value = mock_resp

        res = post_eagent_report.post_eagent("<b>Test</b>")
        self.assertTrue(res)
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['chat_id'], "-1003818905785")
        self.assertEqual(kwargs['json']['message_thread_id'], 3602)
        self.assertEqual(kwargs['json']['text'], "<b>Test</b>")

    @patch('post_eagent_report.requests.post')
    def test_post_failure_http(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = "Bad Request"
        mock_resp.json.return_value = {"ok": False}
        mock_post.return_value = mock_resp

        res = post_eagent_report.post_eagent("fail")
        self.assertFalse(res)

    @patch('post_eagent_report.requests.post')
    def test_post_exception(self, mock_post):
        mock_post.side_effect = Exception("Network timeout")
        res = post_eagent_report.post_eagent("fail")
        self.assertFalse(res)

if __name__ == '__main__':
    unittest.main()
