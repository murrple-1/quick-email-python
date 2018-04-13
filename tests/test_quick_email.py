import unittest

from quick_email import send_email
import tests.smtp.smtpd_fake as smtp

class TestQuickEmail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        smtp.smtp_server_start()

    def test_send_email(self):
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')

    @unittest.skip('not working yet')
    def test_send_email_auth(self):
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', username=u'testuser', password=u'password')

    @unittest.skip('not working yet')
    def test_send_email_starttls(self):
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', require_starttls=True)

    @unittest.skip('not working yet')
    def test_send_email_starttls_auth(self):
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', username=u'testuser', password=u'password', require_starttls=True)

if __name__ == u'__main__':
    unittest.main()
