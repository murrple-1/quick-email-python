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
        send_email(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_IS_TLS, u'Example <example@example.com>', u'Test <test@test.com>', None, None, u'The Subject', u'Some Text', u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)


if __name__ == u'__main__':
    unittest.main()
