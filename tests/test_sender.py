import unittest
import os

from quick_email import builder, sender

SMTP_HOST = os.environ.get(u'SMTP_HOST', u'localhost')
SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'25'))
SMTP_USER = os.environ.get(u'SMTP_USER')
SMTP_PASSWORD = os.environ.get(u'SMTP_PASSWORD')
SMTP_IS_TLS = os.environ.get(u'SMTP_IS_TLS') == u'true'


class TestSender(unittest.TestCase):
    def test_send_msg(self):
        msg = builder.build_msg(u'Example <example@example.com>', u'Test <test@test.com>', None, None, u'The Subject', u'Some Text', u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        sender.send_msg(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_IS_TLS, u'Example <example@example.com>', msg)


if __name__ == u'__main__':
    unittest.main()
