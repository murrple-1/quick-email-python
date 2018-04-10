import unittest

from quick_email import builder


class TestBuilder(unittest.TestCase):
    def test_minimal(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_from_tuple(self):
        msg = builder.build_msg(('Test', 'test@test.com'), u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)


if __name__ == u'__main__':
    unittest.main()
