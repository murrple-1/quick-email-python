import unittest

from quick_email import builder, sender
import smtpd_fake


class TestSender(unittest.TestCase):
    def test_minimal(self):
        smtpd_fake.smtp_server_thread()
        msg = builder.build_msg(u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        sender.send_msg(msg, u'localhost', smtpd_fake.SMTP_PORT)

    def test_multiple_recipients(self):
        smtpd_fake.smtp_server_thread()
        msg = builder.build_msg(u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', send_cc=[u'Example <example@example.com>', u'Example2 <example2@example.com>'], send_bcc=u'Example3 <example3@example.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        sender.send_msg(msg, u'localhost', smtpd_fake.SMTP_PORT)


if __name__ == u'__main__':
    unittest.main()
