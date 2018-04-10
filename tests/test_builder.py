import unittest

from quick_email import builder


class TestBuilder(unittest.TestCase):
    def test_build_msg(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', send_cc=None, send_bcc=None, plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        self.assertIsNotNone(msg)


if __name__ == u'__main__':
    unittest.main()
