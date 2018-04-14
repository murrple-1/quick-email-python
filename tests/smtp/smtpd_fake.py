import os
import time
import asyncore
import ssl
from six.moves import _thread

from tests.smtp.smtpd import SMTPServer

SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'8080'))


class FakeSMTPServer(SMTPServer):
    def __init__(self, localaddr, remoteaddr, ssl_ctx=None, starttls=True, auth=None):
        SMTPServer.__init__(self, localaddr, remoteaddr, ssl_ctx=ssl_ctx, starttls=starttls, auth=auth)

    def process_message(self, peer, mailfrom, rcpttos, data):
        pass


def _smtp_server_func():
    ssl_ctx = _create_default_ssl_context()

    ssl_ctx.load_cert_chain(certfile=u'tests/smtp/certs/cert.pem')

    smtp_server = FakeSMTPServer((u'localhost', SMTP_PORT), None, ssl_ctx=ssl_ctx, starttls=True, auth={
            'user': 'testuser',
            'password': 'password',
        })
    asyncore.loop()


_smtp_server_thead = None
def smtp_server_start():
    global _smtp_server_thead
    if _smtp_server_thead is None:
        _smtp_server_thead = _thread.start_new_thread(_smtp_server_func, ())
        time.sleep(1.0)

# based on `ssl.create_default_context()`
def _create_default_ssl_context():
    context = SSLContext(ssl.PROTOCOL_SSLv23)

    context.options |= ssl.OP_NO_SSLv2 | OP_NO_SSLv3

    return context
