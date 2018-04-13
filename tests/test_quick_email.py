import unittest

from quick_email import send_email

try:
    import tests.smtp.aiosmtpd_fake as smtp

    _can_run_auth_tests = True
    _can_run_ssl_tests = True
except (ImportError, SyntaxError):
    import tests.smtp.smtpd_fake as smtp
    _can_run_auth_tests = False
    _can_run_ssl_tests = False

class TestQuickEmail(unittest.TestCase):
    def test_send_email(self):
        smtp.smtp_server_start()
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')

    @unittest.skipUnless(_can_run_auth_tests, 'Auth tests unsupported')
    def test_send_email_auth(self):
        smtp.smtp_server_start()
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', username=u'testuser', password=u'password')

    @unittest.skipUnless(_can_run_ssl_tests, 'SSL tests unsupported')
    def test_send_email_starttls(self):
        smtp.smtp_server_start()
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', require_starttls=True)

    @unittest.skipUnless(_can_run_auth_tests and _can_run_ssl_tests, 'Auth or SSL tests unsupported')
    def test_send_email_starttls_auth(self):
        smtp.smtp_server_start()
        send_email(u'localhost', smtp.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', username=u'testuser', password=u'password', require_starttls=True)

if __name__ == u'__main__':
    unittest.main()
