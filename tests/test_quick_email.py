import unittest
import os

from quick_email import send_email

SMTP_HOST = os.environ.get(u'SMTP_HOST', u'localhost')
SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'25'))
SMTP_USER = os.environ.get(u'SMTP_USER')
SMTP_PASSWORD = os.environ.get(u'SMTP_PASSWORD')
SMTP_IS_TLS = os.environ.get(u'SMTP_IS_TLS') == u'true'


class TestQuickEmail(unittest.TestCase):
    def test_send_email(self):
        send_email(SMTP_HOST, SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', send_cc=None, send_bcc=None, plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None, username=SMTP_USER, password=SMTP_PASSWORD, is_tls=SMTP_IS_TLS)


if __name__ == u'__main__':
    unittest.main()
