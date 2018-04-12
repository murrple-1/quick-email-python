import unittest

from quick_email import send_email
import smtpd_fake


class TestQuickEmail(unittest.TestCase):
    def test_send_email(self):
        smtpd_fake.smtp_server_thread()
        send_email(u'localhost', smtpd_fake.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', send_cc=None, send_bcc=None, plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)


if __name__ == u'__main__':
    unittest.main()
