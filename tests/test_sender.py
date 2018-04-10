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
        msg = builder.build_msg(u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', send_cc=None, send_bcc=None, plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        sender.send_msg(msg, SMTP_HOST, SMTP_PORT, username=SMTP_USER, password=SMTP_PASSWORD, is_tls=SMTP_IS_TLS)


if __name__ == u'__main__':
    unittest.main()
