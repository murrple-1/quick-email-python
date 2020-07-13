import unittest
import time

from quick_email import send_email
import tests.smtp as smtp


class TestQuickEmail(unittest.TestCase):
    def run(self, *args, **kwargs):
        result = super().run(*args, **kwargs)

        time.sleep(smtp.SMTP_RATE_LIMIT_SECONDS)

        return result

    def test_send_email_auth(self):
        send_email(smtp.SMTP_HOST, smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>',
                   plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', username=smtp.SMTP_USERNAME, password=smtp.SMTP_PASSWORD)

    def test_send_email_starttls_auth(self):
        send_email(smtp.SMTP_HOST, smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>',
                   plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', username=smtp.SMTP_USERNAME, password=smtp.SMTP_PASSWORD, require_starttls=True)


if __name__ == u'__main__':
    unittest.main()
