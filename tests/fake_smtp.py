#!/usr/bin/env python

import os
import smtpd
import asyncore

SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'25'))


class FakeSMTPServer(smtpd.SMTPServer):
    def __init__(*args, **kwargs):
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):
        pass

if __name__ == u'__main__':
    smtp_server = FakeSMTPServer((u'localhost', SMTP_PORT), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()
