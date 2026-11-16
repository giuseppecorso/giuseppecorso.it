"""Tests for the contact endpoint. Run: python deploy/contact/test_app.py

Starts the real HTTP handler on a free local port with a fake mail sender,
so no email leaves the machine.
"""
import os
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer

os.environ.update(SMTP_HOST="localhost", SMTP_USER="info@example.test", SMTP_PASS="x")
import app  # noqa: E402

sent = []
app.send = lambda name, email, topic, message: sent.append((name, email, topic, message))

VALID = {"name": "Mario Rossi", "email": "mario@example.com", "topic": "sito",
         "message": "Vorrei un sito per il mio B&B", "consent": "on"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


opener = urllib.request.build_opener(NoRedirect)


class ContactTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def setUp(self):
        sent.clear()
        app.recent.clear()

    def post(self, fields, path="/api/contact"):
        data = urllib.parse.urlencode(fields).encode()
        try:
            opener.open(urllib.request.Request(self.base + path, data=data))
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Location")
        self.fail("expected a redirect or an error")

    def test_health(self):
        with urllib.request.urlopen(self.base + "/health") as r:
            self.assertEqual(r.read(), b"ok")

    def test_valid_message_is_sent(self):
        self.assertEqual(self.post(VALID), (303, app.OK_URL))
        self.assertEqual(sent, [("Mario Rossi", "mario@example.com", "Un sito web nuovo", "Vorrei un sito per il mio B&B")])

    def test_honeypot_pretends_success_but_sends_nothing(self):
        self.assertEqual(self.post({**VALID, "website": "http://spam"}), (303, app.OK_URL))
        self.assertEqual(sent, [])

    def test_missing_consent_is_rejected(self):
        fields = {k: v for k, v in VALID.items() if k != "consent"}
        self.assertEqual(self.post(fields), (303, app.ERROR_URL))
        self.assertEqual(sent, [])

    def test_bad_email_and_short_message_are_rejected(self):
        self.assertEqual(self.post({**VALID, "email": "nope"})[1], app.ERROR_URL)
        self.assertEqual(self.post({**VALID, "message": "ciao"})[1], app.ERROR_URL)
        self.assertEqual(sent, [])

    def test_header_injection_is_flattened(self):
        self.post({**VALID, "name": "Mario\r\nBcc: victim@example.com"})
        self.assertEqual(sent[0][0], "Mario Bcc: victim@example.com")
        self.assertNotIn("\n", sent[0][0])

    def test_unknown_topic_falls_back(self):
        self.post({**VALID, "topic": "<script>"})
        self.assertEqual(sent[0][2], "Altro")

    def test_rate_limit_per_ip(self):
        for _ in range(app.MAX_PER_HOUR):
            self.assertEqual(self.post(VALID)[1], app.OK_URL)
        self.assertEqual(self.post(VALID)[1], app.ERROR_URL)
        self.assertEqual(len(sent), app.MAX_PER_HOUR)

    def test_oversized_body_is_rejected(self):
        self.assertEqual(self.post({**VALID, "message": "x" * 30_000})[1], app.ERROR_URL)

    def test_smtp_failure_shows_error_page(self):
        def boom(*a):
            raise OSError("smtp down")
        original, app.send = app.send, boom
        try:
            self.assertEqual(self.post(VALID)[1], app.ERROR_URL)
        finally:
            app.send = original

    def test_other_paths_are_404(self):
        self.assertEqual(self.post(VALID, path="/other")[0], 404)


if __name__ == "__main__":
    unittest.main(verbosity=1)
