import unittest

from quick_email import builder, sender

try:
    import tests.smtp.aiosmtpd_fake as smtp

    _can_run_auth_tests = True
    _can_run_ssl_tests = True
except (ImportError, SyntaxError):
    import tests.smtp.smtpd_fake as smtp
    _can_run_auth_tests = False
    _can_run_ssl_tests = False


class TestSender(unittest.TestCase):
    def test_minimal(self):
        smtp.smtp_server_start()
        msg = builder.build_msg(u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        sender.send_msg(msg, u'localhost', smtp.SMTP_PORT)

    def test_multiple_recipients(self):
        smtp.smtp_server_start()
        msg = builder.build_msg(u'Example <example@example.com>', u'The Subject', send_to=u'Test <test@test.com>', send_cc=[u'Example <example@example.com>', u'Example2 <example2@example.com>'], send_bcc=u'Example3 <example3@example.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        sender.send_msg(msg, u'localhost', smtp.SMTP_PORT)


if __name__ == u'__main__':
    unittest.main()
