import unittest
import time

from quick_email import builder, sender
import tests.smtp as smtp


class TestSender(unittest.TestCase):
    def test_minimal(self):
        msg = builder.build_msg(u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        sender.send_msg(msg, smtp.SMTP_HOST, smtp.SMTP_PORT, username=smtp.SMTP_USERNAME, password=smtp.SMTP_PASSWORD, require_starttls=True)
        time.sleep(smtp.SMTP_RATE_LIMIT_SECONDS)

    def test_multiple_recipients(self):
        msg = builder.build_msg(u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', send_cc=[u'Example <example@example.com>', u'Example2 <example2@example.com>'], send_bcc=u'Example3 <example3@example.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        sender.send_msg(msg, smtp.SMTP_HOST, smtp.SMTP_PORT, username=smtp.SMTP_USERNAME, password=smtp.SMTP_PASSWORD, require_starttls=True)
        time.sleep(smtp.SMTP_RATE_LIMIT_SECONDS)


if __name__ == u'__main__':
    unittest.main()
