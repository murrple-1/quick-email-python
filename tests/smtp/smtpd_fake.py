import os
import time
import asyncore
import ssl
from six.moves import _thread

from tests.smtp.smtpd import SMTPServer

SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'8080'))


class FakeSMTPServer(SMTPServer):
    def __init__(*args, **kwargs):
        SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):
        pass


def _smtp_server_func():
    ssl_context = ssl.create_default_context()
    smtp_server = FakeSMTPServer((u'localhost', SMTP_PORT), ssl_ctx=ssl_context, starttls=True, auth={
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
