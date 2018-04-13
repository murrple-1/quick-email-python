import os
import time
from smtpd import SMTPServer
import asyncore
from six.moves import _thread

SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'8080'))


class FakeSMTPServer(SMTPServer):
    def __init__(*args, **kwargs):
        SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):
        pass


def _smtp_server_func():
    smtp_server = FakeSMTPServer((u'localhost', SMTP_PORT), None)
    asyncore.loop()


_smtp_server_thead = None
def smtp_server_start():
    global _smtp_server_thead
    if _smtp_server_thead is None:
        _smtp_server_thead = _thread.start_new_thread(_smtp_server_func, ())
        time.sleep(1.0)
