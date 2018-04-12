import unittest

from quick_email import send_email
import smtpd_fake

try:
    import aiosmtpd
    del aiosmtpd

    _can_run_ssl_tests = True
    _can_run_auth_tests = True
except ImportError:
    _can_run_ssl_tests = False
    _can_run_auth_tests = False

class TestQuickEmail(unittest.TestCase):
    def test_send_email(self):
        smtpd_fake.smtp_server_thread()
        send_email(u'localhost', smtpd_fake.SMTP_PORT, u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', send_cc=None, send_bcc=None, plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)

    @unittest.skipUnless(_can_run_ssl_tests, 'SSL tests unsupported')
    def test_send_email_ssl(self):
        pass

    @unittest.skipUnless(_can_run_auth_tests, 'Auth tests unsupported')
    def test_send_email_auth(self):
        pass

    @unittest.skipUnless(_can_run_ssl_tests and _can_run_auth_tests, 'SSL or Auth tests unsupported')
    def test_send_email_ssl_auth(self):
        pass

if __name__ == u'__main__':
    unittest.main()
