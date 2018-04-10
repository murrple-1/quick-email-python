import unittest

from quick_email import builder


class TestBuilder(unittest.TestCase):
    def test_build_msg(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'Example <example@example.com>', None, None, u'The Subject', u'Some Text', u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        self.assertIsNotNone(msg)


if __name__ == u'__main__':
    unittest.main()
