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

    def test_from_tuple(self):
        msg = builder.build_msg(('Test', 'test@test.com'), u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)


if __name__ == u'__main__':
    unittest.main()
