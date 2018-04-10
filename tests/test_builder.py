import unittest

from quick_email import builder


class TestBuilder(unittest.TestCase):
    # TODO write test suite
    def test_build_msg(self):
        msg = builder.build_msg('Test <test@test.com>', 'Example <example@example.com>', None, None, 'The Subject', 'Some Text', '<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        self.assertIsNotNone(msg)


if __name__ == '__main__':
    unittest.main()
