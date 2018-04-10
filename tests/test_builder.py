import unittest

from quick_email import builder


class TestBuilder(unittest.TestCase):
    def test_to_address_string(self):
        self.assertEqual(builder.to_address_string(u'Test <test@test.com>'), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string((u'Test', u'test@test.com')), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string(u'test@test.com'), u'test@test.com')

    def test_to_address_string_list(self):
        self.assertEqual(builder.to_address_string_list(u'Test <test@test.com>'), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string_list((u'Test', u'test@test.com')), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string_list(u'test@test.com'), u'test@test.com')
        self.assertEqual(builder.to_address_string_list([u'test@test.com']), u'test@test.com')
        self.assertEqual(builder.to_address_string_list([u'test@test.com', u'test2@test.com']), u'test@test.com, test2@test.com')
        self.assertEqual(builder.to_address_string_list([u'Test <test@test.com>', u'test2@test.com']), u'Test <test@test.com>, test2@test.com')
        self.assertEqual(builder.to_address_string_list([(u'Test', u'test@test.com'), u'test2@test.com']), u'Test <test@test.com>, test2@test.com')
        self.assertEqual(builder.to_address_string_list([(u'Test', u'test@test.com'), (u'Test2', u'test2@test.com')]), u'Test <test@test.com>, Test2 <test2@test.com>')

    def test_minimal(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_cc(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_cc=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_cc(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_bcc=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_html_text(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', html_text=u'<b>Some Bold Text</b>')
        self.assertIsNotNone(msg)

    def test_both_texts(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        self.assertIsNotNone(msg)

    def test_multi_recipients(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', send_cc=u'Example2 <example2@example.com>', send_bcc=u'Example3 <example3@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)


if __name__ == u'__main__':
    unittest.main()
