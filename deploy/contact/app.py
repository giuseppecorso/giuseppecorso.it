"""Contact form endpoint for giuseppecorso.it.

A tiny HTTP service (Python standard library only, no dependencies):
it receives the form POST, validates it, and emails the message to the
site owner through the domain mailbox. Nothing is stored on disk.

Runs behind nginx (see deploy/nginx/giuseppecorso.it.conf), which also
rate-limits the endpoint. Configuration comes from environment variables.
"""
import os
import re
import smtplib
import ssl
import sys
import time
from collections import defaultdict, deque
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
MAIL_TO = os.environ.get("MAIL_TO", SMTP_USER)

OK_URL = "/contatti/grazie/"
ERROR_URL = "/contatti/errore/"

MAX_BODY = 20_000          # bytes
MAX_PER_HOUR = 5           # messages per IP address
EMAIL_RE = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,190}\.[^@\s.]{2,24}$")
TOPICS = {
    "sito": "Un sito web nuovo",
    "riparazione": "Sistemare un sito esistente",
    "lavoro": "Una proposta di lavoro",
    "altro": "Altro",
}

recent = defaultdict(deque)  # ip -> timestamps of accepted messages


def log(outcome: str) -> None:
    # No personal data in the log: only the time and what happened.
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {outcome}", file=sys.stderr, flush=True)


def one_line(value: str, limit: int) -> str:
    """Collapse to a single line: blocks email header injection."""
    return " ".join(value.split())[:limit]


def too_many(ip: str) -> bool:
    now = time.time()
    q = recent[ip]
    while q and now - q[0] > 3600:
        q.popleft()
    if len(q) >= MAX_PER_HOUR:
        return True
    q.append(now)
    return False


def send(name: str, email: str, topic: str, message: str) -> None:
    msg = EmailMessage()
    msg["From"] = f"Sito giuseppecorso.it <{SMTP_USER}>"
    msg["To"] = MAIL_TO
    msg["Reply-To"] = email
    msg["Subject"] = f"[Sito] {topic} - {name}"
    msg.set_content(f"Nome: {name}\nEmail: {email}\nRichiesta: {topic}\n\n{message}\n")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20, context=ssl.create_default_context()) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


class Handler(BaseHTTPRequestHandler):
    server_version = "contact"
    sys_version = ""

    def log_message(self, *args) -> None:  # silence the default access log (it prints IPs)
        pass

    def redirect(self, url: str) -> None:
        # 303: the browser follows with a GET, so a page refresh does not resend the form.
        self.send_response(303)
        self.send_header("Location", url)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/health":
            body = b"ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        if self.path != "/api/contact":
            return self.send_error(404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            log("rejected: body size")
            return self.redirect(ERROR_URL)

        form = parse_qs(self.rfile.read(length).decode("utf-8", "replace"), keep_blank_values=True)
        field = lambda k: (form.get(k) or [""])[0].strip()

        # Honeypot: humans never see this field. Pretend success so bots learn nothing.
        if field("website"):
            log("dropped: honeypot")
            return self.redirect(OK_URL)

        name = one_line(field("name"), 100)
        email = one_line(field("email"), 254)
        topic = TOPICS.get(field("topic"), TOPICS["altro"])
        message = field("message")[:5000]

        if len(name) < 2 or not EMAIL_RE.match(email) or len(message) < 10 or field("consent") != "on":
            log("rejected: validation")
            return self.redirect(ERROR_URL)

        ip = self.headers.get("X-Real-IP", self.client_address[0])
        if too_many(ip):
            log("rejected: rate limit")
            return self.redirect(ERROR_URL)

        try:
            send(name, email, topic, message)
        except Exception as exc:  # SMTP down, wrong password, ...
            log(f"error: {type(exc).__name__}")
            return self.redirect(ERROR_URL)

        log("sent")
        self.redirect(OK_URL)


if __name__ == "__main__":
    if not (SMTP_HOST and SMTP_USER and SMTP_PASS):
        log("warning: SMTP settings incomplete, messages cannot be sent")
    log("listening on :8080")
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
